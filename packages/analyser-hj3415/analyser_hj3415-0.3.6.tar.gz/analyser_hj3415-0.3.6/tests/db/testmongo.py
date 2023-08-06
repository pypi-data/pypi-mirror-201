import unittest
import pprint
import pandas as pd

from scraper2_hj3415.krx import krx
from src.analyser_hj3415.db import mongo

addr = "mongodb://192.168.0.173:27017"
client = mongo.connect_mongo(addr)

n = 10
rnd_codes = krx.pick_rnd_x_code(n)
print('rnd_codes: ', rnd_codes)

# 테스트에서 nfscrapy.run 이 필요없는 기타 mongo클래스를 테스트하는 모듈


class ConnectTest(unittest.TestCase):
    def test_client(self):
        print(client)

        # client에서 호스트주소얻는법
        ip = str(list(client.nodes)[0][0])
        port = str(list(client.nodes)[0][1])
        addr = 'mongodb://' + ip + ':' + port
        print(addr)


class MongoBaseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.mongodb = mongo.MongoBase(client, '005930', 'c101')

    def test_db_name(self):
        print(self.mongodb.db_name)
        self.mongodb.client = None
        with self.assertRaises(Exception):
            self.mongodb.db_name = "005490"

    def test_get_all_db_name(self):
        l = mongo.MongoBase.get_all_db_name(client)
        print(len(l), l)

    def test_validate_db(self):
        self.assertTrue(mongo.MongoBase.validate_db(client, "005930"))
        self.assertFalse(mongo.MongoBase.validate_db(client, "123456"))

    def test_validate_col(self):
        self.assertTrue(self.mongodb.validate_col())
        self.mongodb.col_name = 'ddfadaf'
        self.assertFalse(self.mongodb.validate_col())

    def test_get_all_docs(self):
        pprint.pprint(self.mongodb.get_all_docs())

    def test_count_docs_in_col(self):
        for col in self.mongodb.list_collection_names():
            self.mongodb.col_name = col
            print('/'.join([self.mongodb.db_name, self.mongodb.col_name, str(self.mongodb.count_docs_in_col())]))

    def test_del_doc(self):
        client['test_db']['test_col'].insert_one({'test1': "test1-1"})
        self.mongodb.db_name = 'test_db'
        self.mongodb.col_name = 'test_col'
        self.mongodb.del_doc({'test1': "test1-1"})

    def test_list_collections_names(self):
        print(self.mongodb.list_collection_names())

    def test_del_db(self):
        mongo.MongoBase.del_db(client, '000000')


class CorpsTests(unittest.TestCase):
    def test_get_name(self):
        print(mongo.Corps.get_name(client, '005930'))

        # 올바르지 않은 종목을 조회하는 경우
        print(mongo.Corps.get_name(client, '000000'))


class C101Tests(unittest.TestCase):
    def setUp(self):
        self.test_code = '000000'
        self.c101 = mongo.C101(client, code=self.test_code)

    def test_save(self):
        ex_c101 = {'date': '2021.08.09',
                   '코드': '000000',
                   '종목명': '삼성전자',
                   '업종': '반도체와반도체장비',
                   '주가': '81500',
                   '거래량': '15522600',
                   'EPS': 4165.0,
                   'BPS': 39126.0,
                   'PER': 19.57,
                   '업종PER': '17.06',
                   'PBR': 2.08,
                   '배당수익률': '3.67',
                   '최고52주': '96800',
                   '최저52주': '54000',
                   '거래대금': '1267700000000',
                   '시가총액': '486537300000000',
                   '베타52주': '0.92',
                   '발행주식': '5969782550',
                   '유통비율': '74.60',
                   'intro1': '한국 및 CE... DP사업으로 구성됨.',
                   'intro2': '한국 및 CE... DP사업으로 구성됨.'}

        self.c101.save_dict(ex_c101)

        ex_c101 = {'date': '2021.08.09',
                   '코드': '000000',
                   '종목명': '삼성전자',
                   '업종': '반도체와반도체장비',
                   '주가': '81500',
                   '거래량': '15522600',
                   'EPS': 4165.0,
                   'BPS': 39126.0,
                   'PER': 19.57,
                   '업종PER': '17.06',
                   'PBR': 2.08,
                   '배당수익률': '3.67',
                   '최고52주': '96800',
                   '최저52주': '54000',
                   '거래대금': '1267700000000',
                   '시가총액': '486537300000000',
                   '베타52주': '0.92',
                   '발행주식': '5969782550',
                   '유통비율': '74.60',
                   'intro1': '한국 및 CE... DP사업으로 구성됨.',
                   'intro2': '한국 및 CE... DP사업으로 구성됨.'}

        self.c101.save_dict(ex_c101)

        print(self.c101.get_all())

        mongo.MongoBase.del_db(client, self.test_code)

    def test_find(self):
        ex_c101 = {'date': '2021.08.09',
                   '코드': '000000',
                   '종목명': '삼성전자',
                   '업종': '반도체와반도체장비',
                   '주가': '81500',
                   '거래량': '15522600',
                   'EPS': 4165.0,
                   'BPS': 39126.0,
                   'PER': 19.57,
                   '업종PER': '17.06',
                   'PBR': 2.08,
                   '배당수익률': '3.67',
                   '최고52주': '96800',
                   '최저52주': '54000',
                   '거래대금': '1267700000000',
                   '시가총액': '486537300000000',
                   '베타52주': '0.92',
                   '발행주식': '5969782550',
                   '유통비율': '74.60',
                   'intro1': '한국 및 CE... DP사업으로 구성됨.',
                   'intro2': '한국 및 CE... DP사업으로 구성됨.'}

        self.c101.save_dict(ex_c101)

        print(self.c101.find('20210809'))

        # 날짜가 없는 경우
        print(self.c101.find('20210709'))

        mongo.MongoBase.del_db(client, self.test_code)

    def test_get_all(self):
        ex_c101_1 = {'date': '2021.08.08',
                     '코드': '000000',
                     '종목명': '삼성전자',
                     '업종': '반도체와반도체장비',
                     '주가': '81500',
                     '거래량': '15522600',
                     'EPS': 4165.0,
                     'BPS': 39126.0,
                     'PER': 19.57,
                     '업종PER': '17.06',
                     'PBR': 2.08,
                     '배당수익률': '3.67',
                     '최고52주': '96800',
                     '최저52주': '54000',
                     '거래대금': '1267700000000',
                     '시가총액': '486537300000000',
                     '베타52주': '0.92',
                     '발행주식': '5969782550',
                     '유통비율': '74.60',
                     'intro': '한국 및 CE... DP사업으로 구성됨.'}

        ex_c101_2 = {'date': '2021.08.09',
                     '코드': '000000',
                     '종목명': '삼성전자',
                     '업종': '반도체와반도체장비',
                     '주가': '81500',
                     '거래량': '15522600',
                     'EPS': 4165.0,
                     'BPS': 39126.0,
                     'PER': 19.57,
                     '업종PER': '17.06',
                     'PBR': 2.08,
                     '배당수익률': '3.67',
                     '최고52주': '96800',
                     '최저52주': '54000',
                     '거래대금': '1267700000000',
                     '시가총액': '486537300000000',
                     '베타52주': '0.92',
                     '발행주식': '5969782550',
                     '유통비율': '74.60',
                     'intro': '한국 및 CE... DP사업으로 구성됨.'}

        self.c101.save_dict(ex_c101_1)
        self.c101.save_dict(ex_c101_2)

        import pprint
        pprint.pprint(self.c101.get_all())

        mongo.MongoBase.del_db(client, self.test_code)

    def test_get_recent(self):
        ex_c101_1 = {'date': '2021.08.08',
                     '코드': '000000',
                     '종목명': '삼성전자',
                     '업종': '반도체와반도체장비',
                     '주가': '81500',
                     '거래량': '15522600',
                     'EPS': 4165.0,
                     'BPS': 39126.0,
                     'PER': 19.57,
                     '업종PER': '17.06',
                     'PBR': 2.08,
                     '배당수익률': '3.67',
                     '최고52주': '96800',
                     '최저52주': '54000',
                     '거래대금': '1267700000000',
                     '시가총액': '486537300000000',
                     '베타52주': '0.92',
                     '발행주식': '5969782550',
                     '유통비율': '74.60',
                     'intro': '한국 및 CE... DP사업으로 구성됨.'}

        ex_c101_2 = {'date': '2021.08.09',
                     '코드': '000000',
                     '종목명': '삼성전자',
                     '업종': '반도체와반도체장비',
                     '주가': '81500',
                     '거래량': '15522600',
                     'EPS': 4165.0,
                     'BPS': 39126.0,
                     'PER': 19.57,
                     '업종PER': '17.06',
                     'PBR': 2.08,
                     '배당수익률': '3.67',
                     '최고52주': '96800',
                     '최저52주': '54000',
                     '거래대금': '1267700000000',
                     '시가총액': '486537300000000',
                     '베타52주': '0.92',
                     '발행주식': '5969782550',
                     '유통비율': '74.60',
                     'intro': '한국 및 CE... DP사업으로 구성됨.'}

        self.c101.save_dict(ex_c101_1)
        self.c101.save_dict(ex_c101_2)

        print(self.c101.get_recent())

        mongo.MongoBase.del_db(client, self.test_code)


class C103Tests(unittest.TestCase):
    def setUp(self):
        self.test_code = '005930'
        self.c103 = mongo.C103(client, code=self.test_code, page='c103손익계산서y')

    def test_load_df(self):
        print(self.c103.load_df())


class C106Tests(unittest.TestCase):
    def setUp(self):
        self.test_code = '000000'
        self.c106y = mongo.C106(client, self.test_code, 'c106y')
        self.c106q = mongo.C106(client, self.test_code, 'c106q')

    def test_save_load_find(self):
        data = [{'항목': '전일종가', '린드먼아시아': '6500', '삼성스팩2호': '8280', '큐캐피탈': '4085', '엠벤처투자': '305', '나우IB': '14100'},
                {'항목': '시가총액', '린드먼아시아': '877.5', '삼성스팩2호': '854.1', '큐캐피탈': '885.5', '엠벤처투자': '835.0', '나우IB': '890.3'}]
        df = pd.DataFrame(data)
        print(f'code: {self.test_code}')
        self.c106y.save_df(df)
        self.c106q.save_df(df)

        print(self.c106y.load_df())
        print(self.c106q.load_df())

        for title in self.c106y.get_all_titles():
            d = self.c106y.find(title)
            print(d)

        mongo.MongoBase.del_db(client, self.test_code)


class MITests(unittest.TestCase):
    indexes = ('aud', 'chf', 'gbond3y', 'gold', 'silver', 'kosdaq', 'kospi',
               'sp500', 'usdkrw', 'wti', 'avgper', 'yieldgap', 'usdidx')

    def setUp(self):
        self.mi = mongo.MI(client=client, index='aud')

    def test_save_and_load(self):
        dict_data = {'date': '2021.07.21', 'value': '1154.50'}
        for index in self.indexes:
            self.mi.index = index
            self.mi.save_dict(dict_data)

        for index in self.indexes:
            self.mi.index = index
            print(self.mi.index, self.mi.get_recent())

        for index in self.indexes:
            self.mi.index = index
            self.mi.del_doc({'date': '2021.07.21'})





