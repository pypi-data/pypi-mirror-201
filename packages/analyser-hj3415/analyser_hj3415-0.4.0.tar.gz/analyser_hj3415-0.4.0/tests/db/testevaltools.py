import unittest
from src.analyser_hj3415.db import evaltools
from src.analyser_hj3415.db import mongo

addr = "mongodb://192.168.0.173:27017"
client = mongo.connect_mongo(addr)


class EvalToolsTests(unittest.TestCase):
    def setUp(self):
        self.codes_all = mongo.Corps.get_all_codes(client)

    def test_calc비유동부채(self):
        # 예수부채를 사용하는 보험사계열
        code = '000370'
        print(code, evaltools.calc비유동부채(client, code))

    def test_calc비유동부채_all(self):
        for code in self.codes_all:
            print(code, evaltools.calc비유동부채(client, code))

    def test_calc유동부채_all(self):
        for code in self.codes_all:
            print(code, evaltools.calc유동부채(client, code))

    def test_calc유동자산_all(self):
        for code in self.codes_all:
            print(code, evaltools.calc유동자산(client, code))

    def test_calc당기순이익_all(self):
        for code in self.codes_all:
            print(code, evaltools.calc당기순이익(client, code))

    def test_calc유동비율_all(self):
        for code in self.codes_all:
            print(code, evaltools.calc유동비율(client, code, 2))

    def test_findFCF_all(self):
        for code in self.codes_all:
            fcf_dict = evaltools.findFCF(client, code)
            print(code, fcf_dict, mongo.Corps.latest_value(fcf_dict))

    def test_getmarketcap_all(self):
        for code in self.codes_all:
            print(code, evaltools.get_marketcap(client, code))

    def test_findPFCF_all(self):
        for code in self.codes_all:
            pfcf_dict = evaltools.findPFCF(client, code)
            print(code, pfcf_dict, mongo.Corps.latest_value(pfcf_dict))

