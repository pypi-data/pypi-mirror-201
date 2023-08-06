import unittest
import pprint
from src.analyser_hj3415 import eval
from src.analyser_hj3415.db import mongo


addr = "mongodb://192.168.0.173:27017"
client = mongo.connect_mongo(addr)
all_codes = mongo.Corps.get_all_codes(client)


class EvalTests(unittest.TestCase):
    def setUp(self):
        self.test_code = '282720'

    def tearDown(self):
        """테스트 종료 후 파일 삭제 """
        pass

    def test_red(self):
        # 특정 한 종목
        print(self.test_code, '/', mongo.Corps.get_name(client, self.test_code))
        pprint.pprint(eval.red(client, self.test_code))

    def test_red_all(self):
        # 디비 안 전체 종목
        print(f'Totol {len(all_codes)} items')
        for i, code in enumerate(all_codes):
            print(i, '/', code, '/', mongo.Corps.get_name(client, code))
            print(eval.red(client, code))

    def test_blue(self):
        # 특정 한 종목
        print(self.test_code, '/', mongo.Corps.get_name(client, self.test_code))
        pprint.pprint(eval.blue(client, self.test_code))

    def test_blue_all(self):
        # 디비 안 전체 종목
        print(f'Totol {len(all_codes)} items')
        for i, code in enumerate(all_codes):
            print(i, '/', code, '/', mongo.Corps.get_name(client, code))
            print(eval.blue(client, code))

    def test_mil(self):
        # 특정 한 종목
        print(self.test_code, '/', mongo.Corps.get_name(client, self.test_code))
        pprint.pprint(eval.mil(client, self.test_code))

    def test_mil_all(self):
        # 디비 안 전체 종목
        print(f'Totol {len(all_codes)} items')
        for i, code in enumerate(all_codes):
            print(i, '/', code, '/', mongo.Corps.get_name(client, code))
            print(eval.mil(client, code))

    def test_growth_all(self):
        # 디비 안 전체 종목
        print(f'Totol {len(all_codes)} items')
        for i, code in enumerate(all_codes):
            print(i, '/', code, '/', mongo.Corps.get_name(client, code))
            print(eval.growth(client, code))

    def test_eval_all(self):
        import pprint
        pp = pprint.PrettyPrinter(width=200)
        print(f'Totol {len(all_codes)} items')
        for i, code in enumerate(all_codes):
            print(i, '/', code, '/', mongo.Corps.get_name(client, code))
            print(eval.red(client, code))
            pp.pprint(eval.mil(client, code))
            pp.pprint(eval.blue(client, code))
            pprint.pprint(eval.growth(client, code), width=150)


class GetDFTest(unittest.TestCase):
    def test_make_df_part(self):
        codes = ['025320', '000040', '060280', '003240']
        from multiprocessing import Queue
        q = Queue()
        eval._make_df_part(addr, codes, q)

    def test_get_df(self):
        print(eval.make_today_eval_df(client, refresh=True))
        print(eval.make_today_eval_df(client, refresh=False))


class SpacTest(unittest.TestCase):
    def test_valid_spac(self):
        for code, name, price in eval.yield_valid_spac(client):
            print(code, name, price)
