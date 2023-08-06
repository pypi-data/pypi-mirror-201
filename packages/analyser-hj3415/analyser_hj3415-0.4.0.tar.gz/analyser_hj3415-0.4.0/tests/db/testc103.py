import unittest
import random
import pprint
import pandas as pd

import scraper2_hj3415.nfscrapy.run
from scraper2_hj3415 import nfscrapy
from scraper2_hj3415.krx import krx

from src.analyser_hj3415.db import mongo


addr = "mongodb://192.168.0.173:27017"
client = mongo.connect_mongo(addr)

"""
테스트 하는법
n을 정하여 테스트하고자 하는 종목갯수를 정하고 테스트를 돌린다.
nfscrapy.run함수가 setUpClass에서는 작동하지 않아 어쩔수없이 모듈에서 한번은 무조건실행되도록 밖으로 뺐음.
"""

n = 1
rnd_codes = krx.pick_rnd_x_code(n)
print(rnd_codes)
# nfscrapy.run.c103(rnd_codes, addr)


class C103Test(unittest.TestCase):
    def setUp(self):
        # 데이터베이스를 설정한다.
        self.pages = ('c103손익계산서q', 'c103재무상태표q', 'c103현금흐름표q',
                      'c103손익계산서y', 'c103재무상태표y', 'c103현금흐름표y',)
        self.c103 = mongo.C103(client, rnd_codes[0], self.pages[0])

    def test_save_df(self):
        # 000000 데이터베이스에 임의의 데이터를 저장하고 완료후 삭제한다.
        temp_db = '000000'
        temp_col = random.choice(self.pages)
        self.c103 = mongo.C103(client, temp_db, temp_col)
        data = [
            {'항목': '자산총계', '2020/09': 3757887.4, '2020/12': 3782357.2, '2021/03': 3928262.7, '2021/06': 3847776.7, '2021/09': 4104207.2, '전분기대비': 6.7},
            {'항목': '유동자산', '2020/09': 2036349.1, '2020/12': 1982155.8, '2021/03': 2091553.5, '2021/06': 1911185.2, '2021/09': 2127930.2, '전분기대비': 11.3},
            {'항목': '재고자산', '2020/09': 324428.6, '2020/12': 320431.5, '2021/03': 306199.8, '2021/06': 335923.9, '2021/09': 378017.0, '전분기대비': 12.5}
        ]
        df = pd.DataFrame(data)
        print(f'code: {temp_db}')
        self.c103.save_df(df)

        mongo.MongoBase.del_db(client, temp_db)

    def test_find(self):
        # 임의의 종목의 모든 페이지의 모든 타이틀을 출력한다.
        for col in self.pages:
            print('#'*10, col, '#'*10)
            self.c103.page = col
            for title in self.c103.get_all_titles():
                d = self.c103.find(title)
                print(title, d)

    def test_latest_value(self):
        c103q = mongo.C103(client, '426550', 'c103재무상태표q')
        # date가 Unnamed: 1인경우
        title = '비유동부채'
        print(title, c103q.latest_value(title))

    def test_latest_value_all(self):
        # 임의 종목의 모든 타이틀의 최근 값을 반환한다.
        for col in self.pages:
            print('#' * 10, col, '#' * 10)
            self.c103.page = col
            for title in self.c103.get_all_titles():
                print(title, self.c103.latest_value(title))

    def test_sum_recent_4q(self):
        c103q = mongo.C103(client, '426550', 'c103재무상태표q')
        # date에 Unnamed: 1가 있는 경우
        title = '비유동부채'
        print(title, c103q.sum_recent_4q(title))

        # 타이틀 항목이 없는 경우
        c103q.code = '437780'
        title = '당기순이익'
        print(title, c103q.sum_recent_4q(title))

    def test_sum_recent_4q_all(self):
        # 임의 종목의 모든 타이틀 최근 4분기합을 반환한다. 비교를 위해서 년도의 최근값도 첨가하였다.
        result_dict = {}
        for col in self.pages:
            self.c103.page = col
            for title in self.c103.get_all_titles():
                result_dict[title] = []

        for col in self.pages:
            self.c103.page = col
            if col.endswith('q'):
                for title in self.c103.get_all_titles():
                    result_dict[title] += list(self.c103.sum_recent_4q(title))
            elif col.endswith('y'):
                for title in self.c103.get_all_titles():
                    result_dict[title] += list(self.c103.latest_value(title))

        print('#' * 20)
        pprint.pprint(result_dict)

    def test_find_증감율(self):
        # 임의 종목의 모든 타이틀의 증감율 값을 반환한다.
        for col in self.pages:
            print('#' * 10, col, '#' * 10)
            self.c103.page = col
            for title in self.c103.get_all_titles():
                print(title, self.c103.find_증감율(title))


class C103TestHardLoading(unittest.TestCase):
    """
    좀더 많은 종목을 테스트하기 위해서 만든 테스트함수. n으로 종목의 개수를 설정한다.
    """

    def setUp(self):
        # 데이터베이스를 설정한다.
        self.pages = ('c103손익계산서q', 'c103재무상태표q', 'c103현금흐름표q',
                      'c103손익계산서y', 'c103재무상태표y', 'c103현금흐름표y',)
        self.c103 = mongo.C103(client, rnd_codes[0], self.pages[0])

    def test_find_hard_loading(self):
        for code in rnd_codes:
            print(code, '=' * 20)
            self.c103.code = code
            for col in self.pages:
                print('#'*10, col, '#'*10)
                self.c103.page = col
                for title in self.c103.get_all_titles():
                    d = self.c103.find(title)
                    print(title, d)

    def test_latest_value_hard_loading(self):
        for code in rnd_codes:
            print(code, '=' * 20)
            self.c103.code = code
            for col in self.pages:
                print('#' * 10, col, '#' * 10)
                self.c103.page = col
                for title in self.c103.get_all_titles():
                    print(title, self.c103.latest_value(title))

    def test_sum_recent_4q_hard_loading(self):
        for code in rnd_codes:
            print(code, '=' * 20)
            self.c103.code = code
            result_dict = {}
            for col in self.pages:
                self.c103.page = col
                for title in self.c103.get_all_titles():
                    result_dict[title] = []

            for col in self.pages:
                self.c103.page = col
                if col.endswith('q'):
                    for title in self.c103.get_all_titles():
                        result_dict[title] += list(self.c103.sum_recent_4q(title))
                elif col.endswith('y'):
                    for title in self.c103.get_all_titles():
                        result_dict[title] += list(self.c103.latest_value(title))
            pprint.pprint(result_dict)

    def test_find_증감율(self):
        for code in rnd_codes:
            print(code, '=' * 20)
            self.c103.code = code
            for col in self.pages:
                print('#' * 10, col, '#' * 10)
                self.c103.page = col
                for title in self.c103.get_all_titles():
                    print(title, self.c103.find_증감율(title))
