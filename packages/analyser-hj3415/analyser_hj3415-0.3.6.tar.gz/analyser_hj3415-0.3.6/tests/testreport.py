import pprint
import unittest
import random
from krx_hj3415 import krx
from src.eval_hj3415.report import MakeStr, for_console, for_telegram, for_django
from db_hj3415 import dbpath, mongo2


dbpath.save(dbpath.make_path(('hj3415', 'piyrw421'))['OUTER'])
# dbpath.save(dbpath.make_path()['LOCAL'])
# dbpath.save(dbpath.make_path(('hj3415', 'piyrw421'))['ATLAS'])


class ReportTest(unittest.TestCase):
    def setUp(self):
        self.codes = krx.get_codes()
        self.rndcode = random.choice(self.codes)
        self.client = mongo2.connect_mongo(dbpath.load())

    def test_make_str(self):
        ms = MakeStr(self.client, self.rndcode)
        print(ms.c101())
        print(ms.c101(full=False))
        print(ms.red())
        print(ms.red(full=False))
        print(ms.mil())
        print(ms.blue())
        print(ms.blue(full=False))
        print(ms.growth())
        print(ms.growth(full=False))
        print(ms.c108())
        print(ms.c108(full=False))

    def test_for_console(self):
        print(for_console(self.client, self.rndcode))
        #print(for_console(code=self.rndcode))

    def test_for_telegram(self):
        #print(for_telegram(code='005490'))
        print(for_telegram(self.client, self.rndcode))

    def test_for_django(self):
        #pprint.pprint(for_django(code='005490'), width=200)
        pprint.pprint(for_django(self.client, self.rndcode), width=200)

