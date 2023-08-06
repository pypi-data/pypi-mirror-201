import unittest
import random
from src.eval_hj3415.score import red, mil, blue, growth
from db_hj3415 import mongo2, dbpath
from krx_hj3415 import krx

dbpath.save(dbpath.make_path(('hj3415', 'piyrw421'))['OUTER'])
# dbpath.save(dbpath.make_path()['LOCAL'])
# dbpath.save(dbpath.make_path(('hj3415', 'piyrw421'))['ATLAS'])


class ScoreTest(unittest.TestCase):
    def setUp(self):
        self.client = mongo2.connect_mongo(dbpath.load())
        self.codes = mongo2.Corps(self.client).get_all_corps()

    def test_random_one(self):
        rndcode = random.choice(self.codes)
        rndcode = '352700'
        #rndcode = '005930'
        name = krx.get_name(code=rndcode)
        print('/'.join([str(1), str(rndcode), str(name)]))
        print('red', red(self.client, rndcode))
        print('mil', mil(self.client, rndcode))
        print('blue', blue(self.client, rndcode))
        print('growth', growth(self.client, rndcode))

    def test_red(self):
        for i, code in enumerate(self.codes):
            p, q = red(self.client, code)
            if p > 0:
                print(i, '/'.join([str(q), str(code)]))
                print(p, q)

    def test_mil(self):
        for i, code in enumerate(self.codes):
            print(i, '/'.join([str(i), str(code), str(mil(self.client, code))]))

    def test_blue(self):
        for i, code in enumerate(self.codes):
            print(i, '/'.join([str(i), str(code), str(blue(self.client, code))]))

    def test_growth(self):
        for i, code in enumerate(self.codes):
            print(i, '/'.join([str(i), str(code), str(growth(self.client, code))]))
