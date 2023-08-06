import unittest
import random
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
n = 10
rnd_codes = krx.pick_rnd_x_code(n)
print(rnd_codes)
nfscrapy.run.c104(rnd_codes, addr)


class C104Test(unittest.TestCase):
    def setUp(self):
        # 데이터베이스를 설정한다.
        self.pages = ('c104q', 'c104y')
        self.c104 = mongo.C104(client, rnd_codes[0], self.pages[0])

    def test_get_stamp(self):
        print('stamp: ', self.c104.get_stamp())

    def test_modify_stamp(self):
        print('original stamp: ', self.c104.get_stamp())
        self.c104.modify_stamp(days_ago=4)
        print('modified stamp: ', self.c104.get_stamp())

    def test_save_df(self):
        temp_db = '000000'
        temp_col = random.choice(self.pages)
        self.c104 = mongo.C104(client, temp_db, temp_col)
        data1 = [
            {'항목': '매출액증가율', '2016/12': 0.6, '2017/12': 18.68, '2018/12': 1.75, '2019/12': -5.49, '2020/12': 2.78, '2021/12': 14.9, '전년대비': 8.27, '전년대비1': 12.12},
            {'항목': '영업이익증가율', '2016/12': 10.7, '2017/12': 83.46, '2018/12': 9.77, '2019/12': -52.84, '2020/12': 29.62, '2021/12': 43.86, '전년대비': 82.47, '전년대비1': 14.24},
            {'항목': '순이익증가율', '2016/12': 19.23, '2017/12': 85.63, '2018/12': 5.12, '2019/12': -50.98, '2020/12': 21.48, '2021/12': 48.01, '전년대비': 72.46, '전년대비1': 26.53},
        ]

        data2 = [
            {'항목': '총자산증가율', '2016/12': 8.26, '2017/12': 15.1, '2018/12': 12.46, '2019/12': 3.89, '2020/12': 7.28,'2021/12': 7.48, '전년대비': 3.39, '전년대비1': 0.2},
            {'항목': '유동자산증가율', '2016/12': 13.31, '2017/12': 3.93, '2018/12': 18.86, '2019/12': 3.83, '2020/12': 9.28,'2021/12': 8.62, '전년대비': 5.45, '전년대비1': -0.66},
            {'항목': '유형자산증가율', '2016/12': 5.78, '2017/12': 22.07, '2018/12': 3.36, '2019/12': 3.82, '2020/12': 7.62,'2021/12': float('nan'), '전년대비': 3.8, '전년대비1': float('nan')},
            {'항목': '자기자본증가율', '2016/12': 7.76, '2017/12': 11.16, '2018/12': 15.51, '2019/12': 6.11, '2020/12': 4.97,'2021/12': 7.05, '전년대비': -1.13, '전년대비1': 2.08}
        ]
        df1 = pd.DataFrame(data1)
        df2 = pd.DataFrame(data2)
        print(f'code: {temp_db}')

        # save test - serial data
        self.c104.save_df(df1)
        self.c104.save_df(df2)

        # save test - duplcate data
        with self.assertRaises(Exception):
            self.c104.save_df(df1)

        # save test - 2DA ago
        self.c104.modify_stamp(days_ago=2)
        self.c104.save_df(df1)
        self.c104.save_df(df2)

        mongo.MongoBase.del_db(client, temp_db)

    def test_get_all_titles(self):
        print(self.c104.get_all_titles())

    def test_find(self):
        # 임의의 종목의 모든 페이지의 모든 타이틀을 출력한다.
        for col in self.pages:
            print('#'*10, col, '#'*10)
            self.c104.page = col
            for title in self.c104.get_all_titles():
                d = self.c104.find(title)
                print(title, d)

    def test_find_증감율(self):
        # 임의 종목의 모든 타이틀의 증감율 값을 반환한다.
        for col in self.pages:
            print('#' * 10, col, '#' * 10)
            self.c104.page = col
            for title in self.c104.get_all_titles():
                print(title, self.c104.find_증감율(title))

    def test_latest_value(self):
        # 임의 종목의 모든 타이틀의 최근 값을 반환한다.
        for col in self.pages:
            print('#' * 10, col, '#' * 10)
            self.c104.page = col
            for title in self.c104.get_all_titles():
                print(title, self.c104.latest_value(title))


class C104TestHardLoading(unittest.TestCase):
    """
    좀더 많은 종목을 테스트하기 위해서 만든 테스트함수. n으로 종목의 개수를 설정한다.
    """
    def setUp(self):
        # 데이터베이스를 설정한다.
        self.pages = ('c104q', 'c104y')
        self.c104 = mongo.C104(client, rnd_codes[0], self.pages[0])

    def test_find_hard_loading(self):
        # 임의의 종목의 모든 페이지의 모든 타이틀을 출력한다.
        for code in rnd_codes:
            print(code, '=' * 20)
            self.c104.code = code
            for col in self.pages:
                print('#'*10, col, '#'*10)
                self.c104.page = col
                for title in self.c104.get_all_titles():
                    d = self.c104.find(title)
                    print(title, d)

    def test_latest_value_hard_loading(self):
        # 임의 종목의 모든 타이틀의 최근 값을 반환한다.
        for code in rnd_codes:
            print(code, '=' * 20)
            self.c104.code = code
            for col in self.pages:
                print('#' * 10, col, '#' * 10)
                self.c104.page = col
                for title in self.c104.get_all_titles():
                    print(title, self.c104.latest_value(title))

    def test_find_증감율_hard_loading(self):
        # 임의 종목의 모든 타이틀의 증감율 값을 반환한다.
        for code in rnd_codes:
            print(code, '=' * 20)
            self.c104.code = code
            for col in self.pages:
                print('#' * 10, col, '#' * 10)
                self.c104.page = col
                for title in self.c104.get_all_titles():
                    print(title, self.c104.find_증감율(title))
