import math
from typing import Tuple

from .mongo import C101, C103, C104

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.WARNING)


def extract_valid_one(*args):
    """
    유틸함수
    딕셔너리 데이터를 입력받아 하나씩 pop 하여 빈데이터가 아닌 첫번째것을 반환한다.
    """
    logger.debug("In extract_valid_one func...")
    # 입력받은 데이터를 중복되는 것을 제하기 위해 집합으로 변환한다.
    d_set = {i for i in args}
    for i in d_set:
        logger.debug(i)
        # 하나씩 꺼내서 빈문자가 아니면 반환한다.
        if i != "" and i is not math.nan and i is not None:
            return i
    else:
        return None


def calc당기순이익(client, code: str) -> Tuple[str, float]:
    """지배지분 당기순이익 계산

    일반적인 경우로는 직전 지배주주지분 당기순이익을 찾아서 반환한다.\n
    금융기관의 경우는 지배당기순이익이 없기 때문에\n
    계산을 통해서 간접적으로 구한다.\n
    """
    logger.debug(f'In the calc당기순이익... code:{code}')
    c103q = C103(client, code, 'c103재무상태표q')
    try:
        profit_dict = c103q.find(title='*(지배)당기순이익')
        logger.info(f'*(지배)당기순이익 : {profit_dict}')
        return c103q.latest_value('*(지배)당기순이익', nan_to_zero=True)
    except:
        # 금융관련은 재무상태표에 지배당기순이익이 없어서 손익계산서의 당기순이익에서 비지배당기순이익을 빼서 간접적으로 구한다.
        c103q.page = 'c103손익계산서q'
        최근당기순이익date, 최근당기순이익value = c103q.sum_recent_4q('당기순이익', nan_to_zero=True)
        c103q.page = 'c103재무상태표q'
        비지배당기순이익date, 비지배당기순이익value= c103q.latest_value('*(비지배)당기순이익', nan_to_zero=True, allow_empty=True)

        date = extract_valid_one(최근당기순이익date, 비지배당기순이익date)
        계산된지배당기순이익value = 최근당기순이익value - 비지배당기순이익value

        return date, 계산된지배당기순이익value


def calc유동자산(client, code: str) -> Tuple[str, float]:
    """유효한 유동자산 계산

    일반적인 경우로 유동자산을 찾아서 반환한다.\n
    금융기관의 경우는 간접적으로 계산한다.\n
    Red와 Blue에서 사용한다.\n
    """
    logger.debug(f'In the calc유동자산... code:{code}')
    c103q = C103(client, code, 'c103재무상태표q')
    try:
        asset_dict = c103q.find(title='유동자산')
        logger.info(f'유동자산 : {asset_dict}')
        return c103q.sum_recent_4q('유동자산', nan_to_zero=True)
    except:
        # 금융관련업종...
        d1, v1 = c103q.latest_value('현금및예치금', nan_to_zero=True, allow_empty=True)
        d2, v2 = c103q.latest_value('단기매매금융자산', nan_to_zero=True, allow_empty=True)
        d3, v3 = c103q.latest_value('매도가능금융자산', nan_to_zero=True, allow_empty=True)
        d4, v4 = c103q.latest_value('만기보유금융자산', nan_to_zero=True, allow_empty=True)
        logger.debug(f'현금및예치금 : {d1}, {v1}')
        logger.debug(f'단기매매금융자산 : {d2}, {v2}')
        logger.debug(f'매도가능금융자산 : {d3}, {v3}')
        logger.debug(f'만기보유금융자산 : {d4}, {v4}')

        date = extract_valid_one(d1, d2, d3, d4)
        계산된유동자산value = v1 + v2 + v3 + v4

        return date, 계산된유동자산value


def calc유동부채(client, code: str) -> Tuple[str, float]:
    """유효한 유동부채 계산

    일반적인 경우로 유동부채를 찾아서 반환한다.\n
    금융기관의 경우는 간접적으로 계산한다.\n
    Red와 Blue에서 사용한다.\n
    """
    logger.debug(f'In the calc유동부채... code:{code}')
    c103q = C103(client, code, 'c103재무상태표q')
    try:
        debt_dict = c103q.find(title='유동부채')
        logger.debug(f'유동부채 : {debt_dict}')
        return c103q.sum_recent_4q('유동부채', nan_to_zero=True)
    except:
        # 금융관련업종...
        d1, v1 = c103q.latest_value('당기손익인식(지정)금융부채', nan_to_zero=True, allow_empty=True)
        d2, v2 = c103q.latest_value('당기손익-공정가치측정금융부채', nan_to_zero=True, allow_empty=True)
        d3, v3 = c103q.latest_value('매도파생결합증권', nan_to_zero=True, allow_empty=True)
        d4, v4 = c103q.latest_value('단기매매금융부채', nan_to_zero=True, allow_empty=True)
        logger.debug(f'당기손익인식(지정)금융부채 : {d1}, {v1}')
        logger.debug(f'당기손익-공정가치측정금융부채 : {d2}, {v2}')
        logger.debug(f'매도파생결합증권 : {d3}, {v3}')
        logger.debug(f'단기매매금융부채 : {d4}, {v4}')

        date = extract_valid_one(d1, d2, d3, d4)
        계산된유동부채value = v1 + v2 + v3 + v4

        return date, 계산된유동부채value


def calc비유동부채(client, code: str) -> Tuple[str, float]:
    """유효한 비유동부채 계산

    일반적인 경우로 비유동부채를 찾아서 반환한다.\n
    금융기관의 경우는 간접적으로 계산한다.\n
    Red와 Blue에서 사용한다.\n
    """
    logger.debug(f'In the calc비유동부채... code:{code}')
    c103q = C103(client, code, 'c103재무상태표q')
    try:
        debt_dict = c103q.find(title='비유동부채')
        logger.debug(f'비유동부채 : {debt_dict}')
        return c103q.sum_recent_4q('비유동부채', nan_to_zero=True)
    except:
        # 금융관련업종...
        # 보험관련업종은 예수부채가 없는대신 보험계약부채가 있다...
        d1, v1 = c103q.latest_value('예수부채', nan_to_zero=True, allow_empty=True)
        d2, v2 = c103q.latest_value('보험계약부채(책임준비금)', nan_to_zero=True, allow_empty=True)
        d3, v3 = c103q.latest_value('차입부채', nan_to_zero=True, allow_empty=True)
        d4, v4 = c103q.latest_value('기타부채', nan_to_zero=True, allow_empty=True)
        logger.debug(f'예수부채 : {d1}, {v1}')
        logger.debug(f'보험계약부채(책임준비금) : {d2}, {v2}')
        logger.debug(f'차입부채 : {d3}, {v3}')
        logger.debug(f'기타부채 : {d4}, {v4}')

        date = extract_valid_one(d1, d2, d3, d4)
        계산된비유동부채value = v1 + v2 + v3 + v4

        return date, 계산된비유동부채value


def calc유동비율(client, code: str, pop_count: int) -> Tuple[str, float]:
    """유동비율계산 - Blue에서 사용

    c104q에서 최근유동비율 찾아보고 유효하지 않거나 \n
    100이하인 경우에는수동으로 계산해서 다시 한번 평가해 본다.\n
    """
    logger.debug(f'In the calc유동비율... code:{code}')
    c104q = C104(client, code, 'c104q')
    유동비율date, 유동비율value = c104q.latest_value('유동비율', pop_count=pop_count, allow_empty=True)
    logger.debug(f'{code} 유동비율 : {유동비율value}({유동비율date})')

    if math.isnan(유동비율value) or 유동비율value < 100:
        logger.warning('유동비율 is under 100 or nan..so we will recalculate..')
        유동자산date, 유동자산value = calc유동자산(client, code)
        유동부채date, 유동부채value = calc유동부채(client, code)

        c103q = C103(client, code, 'c103현금흐름표q')
        추정영업현금흐름date, 추정영업현금흐름value = c103q.sum_recent_4q('영업활동으로인한현금흐름')
        logger.debug(f'{code} 계산전 유동비율 : {유동비율value}({유동비율date})')

        계산된유동비율 = 0
        try:
            계산된유동비율 = round(((유동자산value + 추정영업현금흐름value) / 유동부채value) * 100, 2)
        except ZeroDivisionError:
            logger.debug(f'유동자산: {유동자산value} + 추정영업현금흐름: {추정영업현금흐름value} / 유동부채: {유동부채value}')
            계산된유동비율 = float('inf')
        finally:
            logger.debug(f'{code} 계산된 유동비율 : {계산된유동비율}')
            return extract_valid_one(유동자산date, 유동부채date, 추정영업현금흐름date), 계산된유동비율
    else:
        return 유동비율date, 유동비율value


def findFCF(client, code: str) -> dict:
    """FCF 계산

    FCF = 영업활동현금흐름 - CAPEX\n
    영업활동현금흐름에서 CAPEX 를 각 연도별로 빼주어 fcf 를 구하고 딕셔너리로 반환한다.\n

    Returns:
        dict: 계산된 fcf 딕셔너리 또는 영업현금흐름 없는 경우 - {}

    Note:
        CAPEX 가 없는 업종은 영업활동현금흐름을 그대로 사용한다.\n

    """
    c103y = C103(client, code, 'c103현금흐름표y')
    영업활동현금흐름_dict = c103y.find(title='영업활동으로인한현금흐름', allow_empty=True)
    c103y.page = 'c103재무상태표y'
    capex = c103y.find(title='*CAPEX', allow_empty=True)

    logger.debug(f'영업활동현금흐름 {영업활동현금흐름_dict}')
    logger.debug(f'CAPEX {capex}')

    if len(영업활동현금흐름_dict) == 0:
        return {}

    if len(capex) == 0:
        # CAPEX 가 없는 업종은 영업활동현금흐름을 그대로 사용한다.
        return 영업활동현금흐름_dict

    # 영업 활동으로 인한 현금 흐름에서 CAPEX 를 각 연도별로 빼주어 fcf 를 구하고 리턴값으로 fcf 딕셔너리를 반환한다.
    r_dict = {}
    for i in range(len(영업활동현금흐름_dict)):
        # 영업활동현금흐름에서 아이템을 하나씩 꺼내서 CAPEX 전체와 비교하여 같으면 차를 구해서 r_dict 에 추가한다.
        영업활동현금흐름date, 영업활동현금흐름value = 영업활동현금흐름_dict.popitem()
        # 해당 연도의 capex 가 없는 경우도 있어 일단 capex를 0으로 치고 먼저 추가한다.
        r_dict[영업활동현금흐름date] = 영업활동현금흐름value
        for CAPEXdate, CAPEXvalue in capex.items():
            if 영업활동현금흐름date == CAPEXdate:
                r_dict[영업활동현금흐름date] = round(영업활동현금흐름value - CAPEXvalue, 2)
    logger.debug(f'r_dict {r_dict}')
    # 연도순으로 정렬해서 딕셔너리로 반환한다.
    return dict(sorted(r_dict.items(), reverse=False))


def findPFCF(client, code: str) -> dict:
    """Price to Free Cash Flow Ratio 계산

    PFCF = 시가총액 / FCF

    Note:
        https://www.investopedia.com/terms/p/pricetofreecashflow.asp
    """
    # marketcap 계산 (fcf가 억 단위라 시가총액을 억으로 나눠서 단위를 맞춰 준다)
    marketcap억 = get_marketcap(client, code) / 100000000
    if math.isnan(marketcap억):
        return {}

    # pfcf 계산
    fcf_dict = findFCF(client, code)
    logger.debug(f'fcf_dict : {fcf_dict}')
    pfcf_dict = {}
    for FCFdate, FCFvalue in fcf_dict.items():
        if FCFvalue == 0:
            pfcf_dict[FCFdate] = math.nan
        else:
            pfcf_dict[FCFdate] = round(marketcap억 / FCFvalue, 2)
    logger.debug(f'pfcf_dict : {pfcf_dict}')
    return pfcf_dict


def get_marketcap(client, code: str, nan_to_zero: bool = False) -> int:
    c101 = C101(client, code)
    try:
        return int(c101.get_recent()['시가총액'])
    except KeyError:
        return 0 if nan_to_zero else math.nan
