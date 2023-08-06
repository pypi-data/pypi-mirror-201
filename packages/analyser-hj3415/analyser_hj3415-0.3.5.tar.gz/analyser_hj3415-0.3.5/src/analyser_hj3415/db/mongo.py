import pymongo
import sys

import copy
from pymongo import errors, MongoClient
import math
import random
import datetime
from typing import List, Tuple
from collections import OrderedDict
from abc import *
from util_hj3415 import utils
import pandas as pd


import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.WARNING)

"""
몽고db구조
RDBMS :     database    / tables        / rows      / columns
MongoDB :   database    / collections   / documents / fields
"""


class UnableConnectServerException(Exception):
    """
    몽고 서버 연결 에러를 처리하기 위한 커스텀 익셉션
    """
    pass


def connect_mongo(addr: str, timeout=5) -> MongoClient:
    """
    몽고 클라이언트를 만들어주는 함수.
    필요할 때마다 클라이언트를 생성하는 것보다 클라이언트 한개로 데이터베이스를 다루는게 효율적이라 함수를 따로 뺐음.
    resolve conn error - https://stackoverflow.com/questions/54484890/ssl-handshake-issue-with-pymongo-on-python3
    :param addr:
    :param timeout:
    :return:
    """
    import certifi
    ca = certifi.where()
    if addr.startswith('mongodb://'):
        # set a some-second connection timeout
        client = pymongo.MongoClient(addr, serverSelectionTimeoutMS=timeout * 1000)
    elif addr.startswith('mongodb+srv://'):
        client = pymongo.MongoClient(addr, serverSelectionTimeoutMS=timeout * 1000, tlsCAFile=ca)
    else:
        raise Exception(f"Invalid address: {addr}")
    try:
        srv_info = client.server_info()
        conn_str = f"Connect to Mongo Atlas v{srv_info['version']}..."
        print(conn_str, f"Server Addr : {addr}")
        return client
    except:
        raise UnableConnectServerException()


def extract_addr_from_client(client: MongoClient) -> str:
    """
    scaraper는 클라이언트를 인자로 받지않고 주소를 받아서 사용하기 때문에 사용하는 주소 추출함수
    """
    # client에서 mongodb주소 추출
    ip = str(list(client.nodes)[0][0])
    port = str(list(client.nodes)[0][1])
    return 'mongodb://' + ip + ':' + port


class MongoBase:
    def __init__(self, client: MongoClient, db_name: str, col_name: str):
        self._db_name = "test"
        self._col_name = "test"
        self.client = client
        self.db_name = db_name
        self.col_name = col_name

    @property
    def db_name(self):
        return self._db_name

    @db_name.setter
    def db_name(self, db_name):
        if self.client is None:
            raise Exception("You should set server connection first")
        else:
            self._db_name = db_name
            self.my_db = self.client[self.db_name]
            self.my_col = self.my_db[self.col_name]

    @property
    def col_name(self):
        return self._col_name

    @col_name.setter
    def col_name(self, col_name):
        if self.db_name is None:
            raise Exception("You should set database first.")
        else:
            self._col_name = col_name
            self.my_col = self.my_db[self.col_name]

    # ========================End Properties=======================

    @staticmethod
    def get_all_db_name(client: MongoClient) -> list:
        return sorted(client.list_database_names())

    @staticmethod
    def validate_db(client: MongoClient, db_name: str) -> bool:
        """
        db_name 이 실제로 몽고db 안에 있는지 확인한다.
        """
        if db_name in client.list_database_names():
            return True
        else:
            return False

    @staticmethod
    def del_db(client: MongoClient, db_name: str):
        if MongoBase.validate_db(client, db_name):
            client.drop_database(db_name)
            print(f"Drop '{db_name}' database..")
        else:
            print(f"Invalid db name : {db_name}", file=sys.stderr)

    def validate_col(self) -> bool:
        """
        col_name 이 실제로 db 안에 있는지 확인한다.
        """
        if self.validate_db(self.client, self.db_name):
            if self.col_name in self.my_db.list_collection_names():
                return True
            else:
                return False

    def get_all_docs(self, remove_id=True) -> list:
        """
        현재 설정된 컬렉션 안의 도큐먼트 전부를 리스트로 반환한다.
        """
        items = []
        if remove_id:
            for doc in self.my_col.find({}):
                del doc['_id']
                items.append(doc)
        else:
            items = list(self.my_col.find({}))
        return items

    def count_docs_in_col(self) -> int:
        """
        현재 설정된 컬렉션 안의 도큐먼트의 갯수를 반환한다.
        """
        return self.my_col.count_documents({})

    def clear_docs_in_col(self):
        """
        현재 설정된 컬렉션 안의 도큐먼트를 전부 삭제한다.
        (컬렉션 자체를 삭제하지는 않는다.)
        """
        self.my_col.delete_many({})
        print(f"Delete all doccument in {self.col_name} collection..")

    def del_col(self):
        """
        현재 설정된 컬렉션을 삭제한다.
        """
        self.my_db.drop_collection(self.col_name)
        print(f"Drop {self.col_name} collection..")

    def list_collection_names(self) -> list:
        return self.my_db.list_collection_names()

    def del_doc(self, del_query: dict):
        """
        del_query에 해당하는 도큐먼트를 삭제한다.
        """
        self.my_col.delete_one(del_query)


class Corps(MongoBase):
    """
    mongodb의 데이터 중 기업 코드로 된 데이터 베이스를 다루는 클래스
    """
    COLLECTIONS = ('c101', 'c104y', 'c104q', 'c106y', 'c106q', 'c108',
                   'c103손익계산서q', 'c103재무상태표q', 'c103현금흐름표q',
                   'c103손익계산서y', 'c103재무상태표y', 'c103현금흐름표y',
                   'dart', 'etc')

    def __init__(self, client: MongoClient, code: str, page: str):
        if utils.is_6digit(code) and page in self.COLLECTIONS:
            super().__init__(client=client, db_name=code, col_name=page)
        else:
            raise Exception(f'Invalid value - code: {code} / {page}({self.COLLECTIONS})')

    @property
    def code(self):
        return self.db_name

    @code.setter
    def code(self, code: str):
        if utils.is_6digit(code):
            self.db_name = code
        else:
            raise Exception(f'Invalid value : {code}')

    @property
    def page(self):
        return self.col_name

    @page.setter
    def page(self, page: str):
        if page in self.COLLECTIONS:
            self.col_name = page
        else:
            raise Exception(f'Invalid value : {page}({self.COLLECTIONS})')

    # ========================End Properties=======================

    @staticmethod
    def latest_value(data: dict, pop_count=2, nan_to_zero=False, allow_empty=False) -> Tuple[str, float]:
        """
        가장 최근 년/분기 값 - evaltools에서도 사용할수 있도록 staticmethod로 뺐음.

        해당 타이틀의 가장 최근의 년/분기 값을 튜플 형식으로 반환한다.

        Args:
            data (dict): 찾고자하는 딕셔너리 데이터
            pop_count: 유효성 확인을 몇번할 것인가
            nan_to_zero: nan의 값을 0으로 바꿀것인가
            allow_empty: title 항목이 없을경우에도 에러를 발생시키지 않을 것인가

        Returns:
            tuple: ex - ('2020/09', 39617.5) or ('', 0)

        Note:
            만약 최근 값이 nan 이면 찾은 값 바로 직전 것을 한번 더 찾아 본다.\n
            데이터가 없는 경우 ('', nan) 반환한다.\n
        """
        def is_valid_value(value) -> bool:
            """
            숫자가 아닌 문자열이나 nan 또는 None의 경우 유효한 형식이 아님을 알려 리턴한다.
            """
            if isinstance(value, str):
                # value : ('Unnamed: 1', '데이터가 없습니다.') 인 경우
                is_valid = False
            elif math.isnan(value):
                # value : float('nan') 인 경우
                is_valid = False
            elif value is None:
                # value : None 인 경우
                is_valid = False
            else:
                is_valid = True
            """
            elif value == 0:
                is_valid = False
            """
            return is_valid

        logger.debug(f'Corps.latest_value raw data : {data}')

        # 데이터를 추출해서 사용하기 때문에 원본 데이터는 보존하기 위해서 카피해서 사용
        data_copied = copy.deepcopy(data)

        for i in range(pop_count):
            try:
                d, v = data_copied.popitem()
            except KeyError:
                # when dictionary is empty
                return '', 0 if nan_to_zero else float('nan')
            if str(d).startswith('20') and is_valid_value(v):
                logger.debug(f'last_one : {v}')
                return d, v

        return '', 0 if nan_to_zero else float('nan')

    @staticmethod
    def refine_data(data: dict, refine_words: list) -> dict:
        """
        주어진 딕셔너리에서 refine_words에 해당하는 키를 삭제해서 반환하는 유틸함수.
        c10346에서 사용
        refine_words : 정규표현식 가능
        """
        copy_data = data.copy()
        import re
        for regex_refine_word in refine_words:
            # refine_word에 해당하는지 정규표현식으로 검사하고 매치되면 삭제한다.
            p = re.compile(regex_refine_word)
            for title, _ in copy_data.items():
                # data 내부의 타이틀을 하나하나 조사한다.
                m = p.match(title)
                if m:
                    del data[title]
        return data

    @staticmethod
    def get_all_codes(client: MongoClient) -> list:
        """
        기업 코드를 데이터베이스명으로 가지는 모든 6자리 숫자 코드의 db 명 반환
        """
        corp_list = []
        for db in MongoBase.get_all_db_name(client):
            if utils.is_6digit(db):
                corp_list.append(db)
        return sorted(corp_list)

    @staticmethod
    def del_all_codes(client: MongoClient):
        corp_list = Corps.get_all_codes(client)
        for corp_db_name in corp_list:
            MongoBase.del_db(client, corp_db_name)

    @staticmethod
    def pick_rnd_x_code(client: MongoClient, count: int) -> list:
        """
        임의의 갯수의 종목코드를 뽑아서 반환한다.
        """
        return random.sample(Corps.get_all_codes(client), count)

    @staticmethod
    def get_name(client: MongoClient, code: str):
        c101 = C101(client, code)
        try:
            name = c101.get_recent()['종목명']
        except KeyError:
            name = None
        return name

    def _save_df(self, df: pd.DataFrame) -> bool:
        # c103, c104, c106, c108에서 주로 사용하는 저장방식
        if df.empty:
            print('Dataframe is empty..So we will skip saving db..')
            return False
        result = self.my_col.insert_many(df.to_dict('records'))
        return result.acknowledged

    def _load_df(self) -> pd.DataFrame:
        # cdart와 c106, c103에서 주로 사용
        try:
            df = pd.DataFrame(self.get_all_docs())
        except KeyError:
            df = pd.DataFrame()
        return df

    def _save_dict(self, dict_data: dict, del_query: dict) -> bool:
        # c101, cdart에서 주로 사용하는 저장방식
        try:
            result = self.my_col.insert_one(dict_data)
        except errors.DuplicateKeyError:
            self.my_col.delete_many(del_query)
            result = self.my_col.insert_one(dict_data)
        return result.acknowledged


class C1034(Corps, metaclass=ABCMeta):
    def __init__(self, client: MongoClient, db_name: str, col_name: str):
        super().__init__(client=client, code=db_name, page=col_name)

    def get_all_titles(self) -> list:
        titles = []
        for item in self.get_all_docs():
            titles.append(item['항목'])
        return list(set(titles))

    @staticmethod
    def sum_each_data(data_list: List[dict]) -> dict:
        """
        검색된 딕셔너리를 모은 리스트를 인자로 받아서 각각의 기간에 맞춰 합을 구해 하나의 딕셔너리로 반환한다.
        """
        sum_dict = {}
        periods = list(data_list[0].keys())
        # 여러딕셔너리를 가진 리스트의 합 구하기
        for period in periods:
            sum_dict[period] = sum(utils.nan_to_zero(data[period]) for data in data_list)
        return sum_dict

    def _find(self, title: str, refine_words: list) -> Tuple[List[dict], int]:
        """
        refine_words 에 해당하는 딕셔너리 키를 삭제하고
        title 인자에 해당하는 항목을 검색하여 반환한다.
        c103의 경우는 중복되는 이름의 항목이 있기 때문에
        이 함수는 반환되는 딕셔너리 리스트와 갯수로 구성되는 튜플을 반환한다.
        """
        titles = self.get_all_titles()
        if title in titles:
            count = 0
            data_list = []
            for data in self.my_col.find({'항목': {'$eq': title}}):
                # 도큐먼트에서 title과 일치하는 항목을 찾아낸다.
                count += 1
                # refine_data함수를 통해 삭제를 원하는 필드를 제거하고 data_list에 추가한다.
                data_list.append(self.refine_data(data, refine_words))
            return data_list, count
        else:
            raise Exception(f'{title} is not in {titles}')

    def latest_value(self, title: str, pop_count=2, nan_to_zero=False, allow_empty=False) -> Tuple[str, float]:
        od = OrderedDict(sorted(self.find(title, allow_empty=allow_empty).items(), reverse=False))
        logger.debug(f'{title} : {od}')
        return Corps.latest_value(od, pop_count, nan_to_zero, allow_empty)

    @abstractmethod
    def find(self, title: str, allow_empty=False) -> dict:
        pass

    def sum_recent_4q(self, title: str, nan_to_zero: bool = False) -> Tuple[str, float]:
        """최근 4분기 합

        분기 페이지 한정 해당 타이틀의 최근 4분기의 합을 튜플 형식으로 반환한다.

        Args:
            title (str): 찾고자 하는 타이틀
            nan_to_zero: nan 값의 경우 zero로 반환한다.

        Returns:
            tuple: (계산된 4분기 중 최근분기, 총합)

        Raises:
            TypeError: 페이지가 q가 아닌 경우 발생

        Note:
            분기 데이터가 4개 이하인 경우 그냥 최근 연도의 값을 찾아 반환한다.
        """
        if self.col_name.endswith('q'):
            # 딕셔너리 정렬 - https://kkamikoon.tistory.com/138
            # reverse = False 이면 오래된것부터 최근순으로 정렬한다.
            od_q = OrderedDict(sorted(self.find(title, allow_empty=True).items(), reverse=False))
            logger.debug(f'{title} : {od_q}')

            if len(od_q) < 4:
                # od_q의 값이 4개 이하이면 그냥 최근 연도의 값으로 반환한다.
                if self.page.startswith('c103'):
                    y = C103(self.client, self.db_name, self.col_name[:-1] + 'y')
                elif self.page.startswith('c104'):
                    y = C104(self.client, self.db_name, self.col_name[:-1] + 'y')
                else:
                    Exception(f'Error on sum_recent_4q func...')
                return y.latest_value(title, nan_to_zero=nan_to_zero, allow_empty=True)
            else:
                q_sum = 0
                date_list = list(od_q.keys())
                while True:
                    try:
                        latest_period = date_list.pop()
                    except IndexError:
                        latest_period = ""
                        break
                    else:
                        if str(latest_period).startswith('20'):
                            break

                for i in range(4):
                    # last = True 이면 최근의 값부터 꺼낸다.
                    d, v = od_q.popitem(last=True)
                    logger.debug(f'd:{d} v:{v}')
                    q_sum += 0 if math.isnan(v) else v
                return str(latest_period), round(q_sum, 2)
        else:
            raise TypeError(f'Not support year data..{self.col_name}')

    def find_증감율(self, title: str) -> dict:
        """

        타이틀에 해당하는 전년/분기대비 값을 반환한다.\n

        Args:
            title (str): 찾고자 하는 타이틀

        Returns:
            float: 전년/분기대비 증감율

        Note:
            중복되는 title 은 취급하지 않기로함.\n
        """
        try:
            data_list, count = self._find(title, ['_id', '항목'])
        except:
            # title을 조회할 수 없는 경우
            if self.col_name.endswith('q'):
                r = {'전분기대비': math.nan}
            else:
                r = {'전년대비': math.nan, '전년대비 1': math.nan}
            return r
        logger.info(data_list)
        cmp_dict = {}
        if count > 1:
            # 중복된 타이틀을 가지는 페이지의 경우 경고 메시지를 보낸다.
            logger.warning(f'Not single data..{self.code}/{self.page}/{title}')
            logger.warning(data_list)
        # 첫번째 데이터를 사용한다.
        data_dict = data_list[0]
        for k, v in data_dict.items():
            if str(k).startswith('전'):
                cmp_dict[k] = v
        return cmp_dict


class C104(C1034):
    def __init__(self, client: MongoClient, code: str, page: str):
        if page in ('c104y', 'c104q'):
            super().__init__(client=client, db_name=code, col_name=page)
        else:
            raise Exception

    def get_all_titles(self) -> list:
        """
        상위 C1034클래스에서 c104는 stamp항목이 있기 때문에 삭제하고 리스트로 반환한다.
        """
        titles = super().get_all_titles()
        titles.remove('stamp')
        return titles

    def find(self, title: str, allow_empty=False) -> dict:
        """
        title에 해당하는 항목을 딕셔너리로 반환한다.
        allow_empty를 true로 하면 에러를 발생시키지 않고 빈딕셔너리를 리턴한다.
        """
        try:
            l, c = super(C104, self)._find(title, ['_id', '항목', '^전.+대비.*'])
            return_dict = l[0]
        except Exception as e:
            if allow_empty:
                return_dict = {}
            else:
                raise Exception(e)
        return return_dict

    def save_df(self, c104_df: pd.DataFrame) -> bool:
        """데이터베이스에 저장

        c104는 4페이지의 자료를 한 컬렉션에 모으는 것이기 때문에
        stamp 를 검사하여 12시간 전보다 이전에 저장된 자료가 있으면
        삭제한 후 저장하고 12시간 이내의 자료는 삭제하지 않고
        데이터를 추가하는 형식으로 저장한다.

        Example:
            c104_data 예시\n
            [{'항목': '매출액증가율',...'2020/12': 2.78, '2021/12': 14.9, '전년대비': 8.27, '전년대비1': 12.12},
            {'항목': '영업이익증가율',...'2020/12': 29.62, '2021/12': 43.86, '전년대비': 82.47, '전년대비1': 14.24}]

        Note:
            항목이 중복되는 경우가 있기 때문에 c104처럼 각 항목을 키로하는 딕셔너리로 만들지 않는다.
        """
        self.my_col.create_index('항목', unique=True)
        time_now = datetime.datetime.now()
        try:
            stamp = self.my_col.find_one({'항목': 'stamp'})['time']
            if stamp < (time_now - datetime.timedelta(days=.1)):
                # 스템프가 1시간 이전이라면..연속데이터가 아니라는 뜻이므로 컬렉션을 초기화한다.
                print("Before save data, cleaning the collection...", end='')
                self.clear_docs_in_col()
        except TypeError:
            # 스템프가 없다면...
            pass
        # 항목 stamp를 찾아 time을 업데이트하고 stamp가 없으면 insert한다.
        self.my_col.update_one({'항목': 'stamp'}, {"$set": {'time': time_now}}, upsert=True)
        return super(C104, self)._save_df(c104_df)

    def get_stamp(self) -> datetime.datetime:
        """
        c104y, c104q가 작성된 시간이 기록된 stamp 항목을 datetime 형식으로 리턴한다.
        """
        return self.my_col.find_one({"항목": "stamp"})['time']

    def modify_stamp(self, days_ago: int):
        """
        인위적으로 타임스템프를 수정한다 - 주로 테스트 용도
        """
        try:
            before = self.my_col.find_one({'항목': 'stamp'})['time']
        except TypeError:
            # 이전에 타임스템프가 없는 경우
            before = None
        time_2da = datetime.datetime.now() - datetime.timedelta(days=days_ago)
        self.my_col.update_one({'항목': 'stamp'}, {"$set": {'time': time_2da}}, upsert=True)
        after = self.my_col.find_one({'항목': 'stamp'})['time']
        logger.info(f"Stamp changed: {before} -> {after}")


class C103(C1034):
    def __init__(self, client: MongoClient, code: str, page: str):
        if page in ('c103손익계산서q', 'c103재무상태표q', 'c103현금흐름표q',
                    'c103손익계산서y', 'c103재무상태표y', 'c103현금흐름표y',):
            super().__init__(client=client, db_name=code, col_name=page)
        else:
            raise Exception

    def save_df(self, c103_df: pd.DataFrame) -> bool:
        """데이터베이스에 저장

        Example:
            c103_list 예시\n
            [{'항목': '자산총계', '2020/03': 3574575.4, ... '전분기대비': 3.9},
            {'항목': '유동자산', '2020/03': 1867397.5, ... '전분기대비': 5.5}]

        Note:
            항목이 중복되는 경우가 있기 때문에 c104처럼 각 항목을 키로하는 딕셔너리로 만들지 않는다.
        """
        self.my_col.create_index('항목', unique=False)
        print("Before save data, cleaning the collection...", end='')
        self.clear_docs_in_col()
        return super(C103, self)._save_df(c103_df)

    def load_df(self) -> pd.DataFrame:
        """
        데이터베이스에 저장된 페이지를 데이터프레임으로 반환한다.
        """
        return super(C103, self)._load_df()

    def find(self, title: str, allow_empty=False) -> dict:
        """
        title에 해당하는 항목을 딕셔너리로 반환한다.
        allow_empty를 true로 하면 에러를 발생시키지 않고 빈딕셔너리를 리턴한다.
        c103의 경우는 중복된 타이틀을 가지는 항목이 있어 합쳐서 한개의 딕셔너리로 반환한다.
        """
        try:
            l, c = super(C103, self)._find(title, ['_id', '항목', '^전.+대비.*'])
            sum_dict = self.sum_each_data(l)
        except Exception as e:
            if allow_empty:
                sum_dict = {}
            else:
                raise Exception(e)
        return sum_dict


class C101(Corps):
    def __init__(self, client: MongoClient, code: str):
        super().__init__(client=client, code=code, page='c101')
        self.my_col.create_index('date', unique=True)

    def save_dict(self, c101_dict: dict) -> bool:
        """
        c101의 구조에 맞는 딕셔너리값을 받아서 구조가 맞는지 확인하고 맞으면 저장한다.

        Note:
            <c101_struc>\n
            'date', '코드', '종목명',\n
            '업종', '주가', '거래량',\n
            'EPS', 'BPS', 'PER',\n
            '업종PER', 'PBR', '배당수익률',\n
            '최고52주', '최저52주', '거래대금',\n
            '시가총액', '베타52주', '발행주식',\n
            '유통비율', 'intro'\n
        """
        c101_template = ['date', '코드', '종목명', '업종', '주가', '거래량', 'EPS', 'BPS', 'PER', '업종PER', 'PBR',
                         '배당수익률', '최고52주', '최저52주', '거래대금', '시가총액', '베타52주', '발행주식', '유통비율']
        # 리스트 비교하기
        # reference from https://codetorial.net/tips_and_examples/compare_two_lists.html
        if c101_dict['코드'] != self.db_name:
            raise Exception("Code isn't equal input data and db data..")
        logger.debug(c101_dict.keys())
        # c101 데이터가 c101_template의 내용을 포함하는가 확인하는 if문
        # refered from https://appia.tistory.com/101
        if (set(c101_template) - set(c101_dict.keys())) == set():
            # 스크랩한 날짜 이후의 데이터는 조회해서 먼저 삭제한다.
            del_query = {'date': {"$gte": c101_dict['date']}}
            return super(C101, self)._save_dict(c101_dict, del_query)
        else:
            raise Exception('Invalid c101 dictionary structure..')

    def find(self, date: str) -> dict:
        """

        해당 날짜의 데이터를 반환한다.
        만약 리턴값이 없으면 {} 을 반환한다.

        Args:
            date (str): 예 - 20201011(6자리숫자)
        """
        if utils.isYmd(date):
            converted_date = date[:4] + '.' + date[4:6] + '.' + date[6:]
        else:
            raise Exception(f'Invalid date format : {date}(ex-20201011(8자리숫자))')
        d = self.my_col.find_one({'date': converted_date})
        if d is None:
            return {}
        else:
            del d['_id']
            return d

    def get_recent(self) -> dict:
        """저장된 데이터에서 가장 최근 날짜의 딕셔너리를 반환한다.

        Examples:
            {'date': '2021.08.09',\n
            '코드': '005930',\n
            '종목명': '삼성전자',\n
            '업종': '반도체와반도체장비',\n
            '주가': '81500',\n
            '거래량': '15522600',\n
            'EPS': 4165.0,\n
            'BPS': 39126.0,\n
            'PER': 19.57,\n
            '업종PER': '17.06',\n
            'PBR': 2.08,\n
            '배당수익률': '3.67',\n
            '최고52주': '96800',\n
            '최저52주': '54000',\n
            '거래대금': '1267700000000',\n
            '시가총액': '486537300000000',\n
            '베타52주': '0.92',\n
            '발행주식': '5969782550',\n
            '유통비율': '74.60',\n
            'intro': '한국 및 CE... DP사업으로 구성됨.'}\n
        """
        try:
            d = self.my_col.find({'date': {'$exists': True}}).sort('date', pymongo.DESCENDING).next()
            del d['_id']
        except StopIteration:
            d = {}
        return d

    def get_all(self) -> list:
        """

        저장된 모든 데이터를 딕셔너리로 가져와서 리스트로 포장하여 반환한다.
        """
        items = []
        for doc in self.my_col.find({'date': {'$exists': True}}).sort('date', pymongo.ASCENDING):
            del doc['_id']
            items.append(doc)
        return items


class C106(Corps):
    def __init__(self, client: MongoClient, code: str, page: str):
        if page in ('c106y', 'c106q'):
            super().__init__(client=client, code=code, page=page)
        else:
            raise Exception

    def save_df(self, c106_df: pd.DataFrame) -> bool:
        self.my_col.create_index('항목', unique=True)
        self.clear_docs_in_col()
        return super(C106, self)._save_df(c106_df)

    def load_df(self) -> pd.DataFrame:
        return super(C106, self)._load_df()

    def get_all_titles(self) -> list:
        titles = []
        for item in self.get_all_docs():
            titles.append(item['항목'])
        return list(set(titles))

    def find(self, title: str, allow_empty=False) -> dict:
        """
        title에 해당하는 항목을 딕셔너리로 반환한다.
        """
        titles = self.get_all_titles()
        if title in titles:
            data = self.my_col.find_one({'항목': {'$eq': title}})
            return self.refine_data(data, ['_id', '항목'])
        else:
            if allow_empty:
                return {}
            else:
                raise Exception(f'{title} is not in {titles}')


class DateBase(MongoBase):
    """
    날짜를 컬렉션으로 가지는 데이터베이스를 위한 기반클래스
    """
    def __init__(self, client: MongoClient, db_name: str, date: str):
        if utils.isYmd(date):
            super().__init__(client=client, db_name=db_name, col_name=date)
        else:
            raise Exception(f"Invalid date : {date}(%Y%m%d)")

    @property
    def date(self):
        return self.col_name

    @date.setter
    def date(self, date: str):
        if utils.isYmd(date):
            self.col_name = date
        else:
            raise Exception(f"Invalid date : {date}(%Y%m%d)")

    # ========================End Properties=======================

    def save_df(self, df: pd.DataFrame) -> bool:
        if df.empty:
            print('Dataframe is empty..So we will skip saving db..')
            return False

        self.clear_docs_in_col()
        print(f"Save new data to '{self.db_name}' / '{self.col_name}'")
        result = self.my_col.insert_many(df.to_dict('records'))
        return result.acknowledged

    def load_df(self) -> pd.DataFrame:
        try:
            df = pd.DataFrame(list(self.my_col.find({}))).drop(columns=['_id'])
        except KeyError:
            df = pd.DataFrame()
        return df


class EvalByDate(DateBase):
    """
    각 날짜별로 만들어진 eval-report 데이터프레임을 관리하는 클래스
    DB_NAME : eval
    COL_NAME : Ymd형식 날짜
    """
    EVAL_DB = 'eval'

    def __init__(self, client: MongoClient, date: str):
        super().__init__(client, self.EVAL_DB, date)
        # 인덱스 설정
        self.my_col.create_index('code', unique=True)


class MI(MongoBase):
    """mi 데이터베이스 클래스

    Note:
        db - mi\n
        col - 'aud', 'chf', 'gbond3y', 'gold', 'silver', 'kosdaq', 'kospi', 'sp500', 'usdkrw', 'wti', 'avgper', 'yieldgap', 'usdidx' - 총 13개\n
        doc - date, value\n
    """
    MI_DB = 'mi'
    COL_TITLE = ('aud', 'chf', 'gbond3y', 'gold', 'silver', 'kosdaq', 'kospi',
                 'sp500', 'usdkrw', 'wti', 'avgper', 'yieldgap', 'usdidx')

    def __init__(self, client: MongoClient, index: str):
        if index in self.COL_TITLE:
            super().__init__(client=client, db_name=self.MI_DB, col_name=index)
        else:
            raise Exception(f'Invalid index : {index}({self.COL_TITLE})')

    @property
    def index(self):
        return self.col_name

    @index.setter
    def index(self, index: str):
        if index in self.COL_TITLE:
            self.col_name = index
        else:
            raise Exception(f'Invalid index : {index}({self.COL_TITLE})')

    # ========================End Properties=======================

    def get_recent(self) -> Tuple[str, float]:
        """저장된 가장 최근의 값을 반환하는 함수
        """
        if self.validate_col():
            d = self.my_col.find({'date': {'$exists': True}}).sort('date', pymongo.DESCENDING).next()
            del d['_id']
            return d['date'], d['value']

    def save_dict(self, mi_dict: dict) -> bool:
        """MI 데이터 저장

        Args:
            mi_dict (dict): ex - {'date': '2021.07.21', 'value': '1154.50'}
        """
        self.my_col.create_index('date', unique=True)
        result = self.my_col.update_one({'date': mi_dict['date']}, {"$set": {'value': mi_dict['value']}}, upsert=True)
        return result.acknowledged
