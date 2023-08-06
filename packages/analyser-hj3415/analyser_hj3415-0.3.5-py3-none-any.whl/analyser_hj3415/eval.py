"""red, mil, blue 3가지 분야에서 자료를 계산하여 리턴하는 함수 모음
"""
import math
import time
import datetime
import pandas as pd
from multiprocessing import Process, Queue

from .db import mongo, evaltools
from util_hj3415 import utils

import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.WARNING)

# 주식을 통한 기대수익률 - 금리가 3%일 경우 두배인 6% 정도로 잡는다.
EXPECT_EARN = 0.04


def red(client, code: str) -> dict:
    c101 = mongo.C101(client, code)
    c103q = mongo.C103(client, code, 'c103재무상태표q')

    d1, 지배주주당기순이익 = evaltools.calc당기순이익(client, code)
    d2, 유동자산 = evaltools.calc유동자산(client, code)
    d3, 유동부채 = evaltools.calc유동부채(client, code)
    d4, 부채평가 = evaltools.calc비유동부채(client, code)

    c103q.page = 'c103재무상태표q'
    d5, 투자자산 = c103q.latest_value('투자자산', nan_to_zero=True, allow_empty=True)
    d6, 투자부동산 = c103q.latest_value('투자부동산', nan_to_zero=True, allow_empty=True)

    # 사업가치 계산 - 지배주주지분 당기순이익 / 기대수익률
    사업가치 = round(지배주주당기순이익 / EXPECT_EARN, 2)

    # 재산가치 계산 - 유동자산 - (유동부채*1.2) + 고정자산중 투자자산
    재산가치 = round(유동자산 - (유동부채 * 1.2) + 투자자산 + 투자부동산, 2)
    if math.isnan(재산가치):
        logger.warning(f'유동자산: {유동자산} - 유동부채: {유동부채} * 1.2 + 투자자산: {투자자산} + 투자부동산: {투자부동산}')

    d, 발행주식수 = c103q.latest_value('발행주식수', allow_empty=True)
    if math.isnan(발행주식수):
        rc101 = c101.get_recent()
        logger.error(rc101)
        발행주식수 = utils.to_int(rc101.get('발행주식'))
    else:
        발행주식수 = 발행주식수 * 1000

    try:
        red_price = round(((사업가치 + 재산가치 - 부채평가) * 100000000) / 발행주식수)
    except (ZeroDivisionError, ValueError) as e:
        logger.error(f'In calc red price... {e} : {code}')
        red_price = math.nan

    logger.debug(f'Red Price : {red_price}원')
    return {
        'red_price': red_price,
        '사업가치': 사업가치,
        '재산가치': 재산가치,
        '부채평가': 부채평가,
        '발행주식수': 발행주식수,
        'date': [i for i in {d1, d2, d3, d4, d5, d6} if i != ''],  # ''값을 제거하고 리스트로 바꾼다.
    }


def mil(client, code: str) -> dict:
    c103 = mongo.C103(client, code, 'c103현금흐름표q')
    c104 = mongo.C104(client, code, 'c104q')

    marketcap억 = evaltools.get_marketcap(client, code, nan_to_zero=False) / 100000000
    logger.debug(f'{code} market cap: {marketcap억}')
    fcf_dict = evaltools.findFCF(client, code)
    pfcf_dict = evaltools.findPFCF(client, code)
    d1, 지배주주당기순이익 = evaltools.calc당기순이익(client, code)

    d2, 재무활동현금흐름 = c103.sum_recent_4q(title='재무활동으로인한현금흐름', nan_to_zero=False)
    d3, 영업활동현금흐름 = c103.sum_recent_4q(title='영업활동으로인한현금흐름', nan_to_zero=False)

    d4, roic = c104.sum_recent_4q('ROIC', nan_to_zero=False)
    d5, roe = c104.latest_value('ROE', nan_to_zero=False, allow_empty=True)
    pcr_dict = c104.find('PCR', allow_empty=True)

    try:
        주주수익률 = round((재무활동현금흐름 / marketcap억 * -100), 2)
        이익지표 = round((지배주주당기순이익 - 영업활동현금흐름) / marketcap억, 5)
    except ZeroDivisionError:
        주주수익률 = math.nan
        이익지표 = math.nan

    if math.isnan(주주수익률) or math.isnan(이익지표):
        logger.warning(f'주주수익률: {주주수익률} 이익지표: {이익지표}')
        logger.warning(f'재무활동현금흐름: {재무활동현금흐름}지배주주당기순이익: {지배주주당기순이익}영업활동현금흐름: {영업활동현금흐름}')

    logger.debug(f'{code} fcf_dict : {fcf_dict}')
    logger.debug(f"{code} market_cap : {marketcap억}")
    logger.debug(f'{code} pfcf_dict : {pfcf_dict}')
    logger.debug(f'{code} pcr_dict : {pcr_dict}')

    return {
        '주주수익률': 주주수익률,
        '이익지표': 이익지표,
        '투자수익률': {'ROIC': roic, 'ROE': roe},
        '가치지표': {'FCF': fcf_dict, 'PFCF': pfcf_dict, 'PCR': pcr_dict},
        'date': [i for i in {d1, d2, d3, d4, d5} if i != ''],  # ''값을 제거하고 리스트로 바꾼다.
    }


def blue(client, code: str) -> dict:
    """
    <유동비율>
    100미만이면 주의하나 현금흐름창출력이 좋으면 괜찮을수 있다.
    만약 100%이하면 유동자산에 추정영업현금흐름을 더해서 다시계산해보아 기회를 준다.
    <이자보상배율>
    이자보상배율 영업이익/이자비용으로 1이면 자금사정빡빡 5이상이면 양호
    <순운전자금회전율>
    순운전자금 => 기업활동을 하기 위해 필요한 자금 (매출채권 + 재고자산 - 매입채무)
    순운전자본회전율은 매출액/순운전자본으로 일정비율이 유지되는것이 좋으며 너무 작아지면 순운전자본이 많아졌다는 의미로 재고나 외상이 쌓인다는 뜻
    <재고자산회전율>
    재고자산회전율은 매출액/재고자산으로 회전율이 낮을수록 재고가 많다는 이야기이므로 불리 전년도등과 비교해서 큰차이 발생하면 알람.
    재고자산회전율이 작아지면 재고가 쌓인다는뜻
    <순부채비율>
    부채비율은 업종마다 달라 일괄비교 어려우나 순부채 비율이 20%이하인것이 좋고 꾸준히 늘어나지 않는것이 좋다.
    순부채 비율이 30%이상이면 좋치 않다.
    <매출액>
    매출액은 어떤경우에도 성장하는 기업이 좋다.매출이 20%씩 늘어나는 종목은 유망한 종목
    <영업이익률>
    영업이익률은 기업의 경쟁력척도로 경쟁사에 비해 높으면 경제적해자를 갖춘셈
    """

    d1, 유동비율 = evaltools.calc유동비율(client, code, pop_count=3)
    logger.debug(f'유동비율 {유동비율} / [{d1}]')

    c104y = mongo.C104(client, code, 'c104y')
    dict이자보상배율y = c104y.find('이자보상배율', allow_empty=True)
    dict순운전자본회전율y = c104y.find('순운전자본회전율', allow_empty=True)
    dict재고자산회전율y = c104y.find('재고자산회전율', allow_empty=True)
    dict순부채비율y = c104y.find('순부채비율', allow_empty=True)

    c104q = mongo.C104(client, code, 'c104q')
    d2, 이자보상배율q = c104q.latest_value('이자보상배율', allow_empty=True)
    d3, 순운전자본회전율q = c104q.latest_value('순운전자본회전율', allow_empty=True)
    d4, 재고자산회전율q = c104q.latest_value('재고자산회전율', allow_empty=True)
    d5, 순부채비율q = c104q.latest_value('순부채비율', allow_empty=True)

    if len(dict이자보상배율y) == 0:
        logger.warning(f'empty dict - 이자보상배율 : {이자보상배율q} {dict이자보상배율y}')

    if len(dict순운전자본회전율y) == 0:
        logger.warning(f'empty dict - 순운전자본회전율 : {순운전자본회전율q} {dict순운전자본회전율y}')

    if len(dict재고자산회전율y) == 0:
        logger.warning(f'empty dict - 재고자산회전율 : {재고자산회전율q} {dict재고자산회전율y}')

    if len(dict순부채비율y) == 0:
        logger.warning(f'empty dict - 순부채비율 : {순부채비율q} {dict순부채비율y}')

    ################################################################

    return {
        '유동비율': 유동비율,
        '이자보상배율': (이자보상배율q, dict이자보상배율y),
        '순운전자본회전율': (순운전자본회전율q, dict순운전자본회전율y),
        '재고자산회전율': (재고자산회전율q, dict재고자산회전율y),
        '순부채비율': (순부채비율q, dict순부채비율y),
        'date': [i for i in {d1, d2, d3, d4, d5} if i != ''],  # ''값을 제거하고 리스트로 바꾼다.
    }


def growth(client, code: str) -> dict:
    """
    <매출액>
    매출액은 어떤경우에도 성장하는 기업이 좋다.매출이 20%씩 늘어나는 종목은 유망한 종목
    <영업이익률>
    영업이익률은 기업의 경쟁력척도로 경쟁사에 비해 높으면 경제적해자를 갖춘셈
    """
    c104y = mongo.C104(client, code, 'c104y')
    c106y = mongo.C106(client, code, 'c106y')

    dict매출액증가율y = c104y.find('매출액증가율', allow_empty=True)

    c104q = mongo.C104(client, code, 'c104q')
    d1, 매출액증가율q = c104q.latest_value('매출액증가율', nan_to_zero=False, allow_empty=True)

    logger.debug(f'매출액증가율 : {매출액증가율q} {dict매출액증가율y}')

    ################################################################

    # c106 에서 타 기업과 영업이익률 비교
    dict영업이익률 = c106y.find('영업이익률', allow_empty=True)

    return {
        '매출액증가율': (매출액증가율q, dict매출액증가율y),
        '영업이익률': dict영업이익률,
        'date': [d1, ]}


"""
- 각분기의 합이 연이 아닌 타이틀(즉 sum_4q를 사용하면 안됨)
'*(지배)당기순이익'
'*(비지배)당기순이익'
'장기차입금'
'현금및예치금'
'매도가능금융자산'
'매도파생결합증권'
'만기보유금융자산'
'당기손익-공정가치측정금융부채'
'당기손익인식(지정)금융부채'
'단기매매금융자산'
'단기매매금융부채'
'예수부채'
'차입부채'
'기타부채'
'보험계약부채(책임준비금)'
'*CAPEX'
'ROE'
"""

"""
- sum_4q를 사용해도 되는 타이틀
'자산총계'
'당기순이익'
'유동자산'
'유동부채'
'비유동부채'

'영업활동으로인한현금흐름'
'재무활동으로인한현금흐름'
'ROIC'
"""


def _make_df_part(db_addr, codes: list, q):
    def make_record(my_client, my_code: str) -> dict:
        # 장고에서 사용할 eval 테이블을 만들기 위해 각각의 레코드를 구성하는 함수
        c101 = mongo.C101(my_client, my_code).get_recent()

        red_dict = red(my_client, my_code)
        mil_dict = mil(my_client, my_code)
        growth_dict = growth(my_client, my_code)

        mil_date = mil_dict['date']
        red_date = red_dict['date']
        growth_date = growth_dict['date']

        return {
            'code': c101['코드'],
            '종목명': c101['종목명'],
            '주가': utils.to_int(c101['주가']),
            'PER': utils.to_float(c101['PER']),
            'PBR': utils.to_float(c101['PBR']),
            '시가총액': utils.to_float(c101['시가총액']),
            'RED': utils.to_int(red_dict['red_price']),
            '주주수익률': utils.to_float(mil_dict['주주수익률']),
            '이익지표': utils.to_float(mil_dict['이익지표']),
            'ROIC': utils.to_float(mil_dict['투자수익률']['ROIC']),
            'ROE': utils.to_float(mil_dict['투자수익률']['ROE']),
            'PFCF': utils.to_float(mongo.Corps.latest_value(mil_dict['가치지표']['PFCF'])[1]),
            'PCR': utils.to_float(mongo.Corps.latest_value(mil_dict['가치지표']['PCR'])[1]),
            '매출액증가율': utils.to_float(growth_dict['매출액증가율'][0]),
            'date': list(set(mil_date + red_date + growth_date))
        }
    # 각 코어별로 디비 클라이언트를 만들어야만 한다. 안그러면 에러발생
    client = mongo.connect_mongo(db_addr)
    t = len(codes)
    d = []
    for i, code in enumerate(codes):
        print(f'{i+1}/{t} {code}')
        try:
            d.append(make_record(client, code))
        except:
            logger.error(f'error on {code}')
            continue
    df = pd.DataFrame(d)
    logger.info(df)
    q.put(df)


def make_today_eval_df(client, refresh: bool = False) -> pd.DataFrame:
    """ 멀티프로세싱을 사용하여 전체 종목의 eval 을 데이터프레임으로 만들어 반환

    기본값으로 refresh 는 False 로 설정되어 당일자의 저장된 데이터프레임이 있으면 새로 생성하지 않고 mongo DB를 이용한다.
    """
    today_str = datetime.datetime.today().strftime('%Y%m%d')
    df = mongo.EvalByDate(client, today_str).load_df()
    if refresh or len(df) == 0:
        codes_in_db = mongo.Corps.get_all_codes(client)

        print('*' * 25, f"Eval all using multiprocess(refresh={refresh})", '*' * 25)
        print(f'Total {len(codes_in_db)} items..')
        logger.debug(codes_in_db)
        n, divided_list = utils.code_divider_by_cpu_core(codes_in_db)

        addr = mongo.extract_addr_from_client(client)

        start_time = time.time()
        q = Queue()
        ths = []
        for i in range(n):
            ths.append(Process(target=_make_df_part, args=(addr, divided_list[i], q)))
        for i in range(n):
            ths[i].start()

        df_list = []
        for i in range(n):
            df_list.append(q.get())
        # 부분데이터프레임들을 하나로 합침
        final_df = pd.concat(df_list, ignore_index=True)

        for i in range(n):
            ths[i].join()

        print(f'Total spent time : {round(time.time() - start_time, 2)} sec.')
        logger.debug(final_df)
        print(f"Save to mongo db(db: eval col: {today_str})")
        mongo.EvalByDate(client, today_str).save_df(final_df)
    else:
        print(f"Use saved dataframe from mongo db..")
        final_df = df
    return final_df


def yield_valid_spac(client) -> tuple:
    """
    전체 스팩주의 현재가를 평가하여 2000원 이하인 경우 yield한다.

    Returns:
        tuple: (code, name, price)
    """
    codes = mongo.Corps.get_all_codes(client)
    logger.debug(f'len(codes) : {len(codes)}')
    print('<<< Finding valuable SPAC >>>')
    for i, code in enumerate(codes):
        name = mongo.Corps.get_name(client, code)
        logger.debug(f'code : {code} name : {name}')
        if '스팩' in str(name):
            logger.debug(f'>>> spac - code : {code} name : {name}')
            price, _, _ = utils.get_price_now(code=code)
            if price <= 2000:
                logger.warning(f'현재가:{price}')
                print(f"code: {code} name: {name}, price: {price}")
                yield code, name, price
