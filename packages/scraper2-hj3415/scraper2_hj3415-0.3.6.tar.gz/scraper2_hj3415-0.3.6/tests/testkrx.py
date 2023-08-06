import unittest
import shutil
from src.scraper2_hj3415.krx import krx


class KrxTests(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        shutil.rmtree(krx._TEMP_DIR, ignore_errors=True)

    def test_get_tablename(self):
        print(krx._get_tablename())

    def test_make_db(self):
        self.assertTrue(krx._save_html_from_krx())
        self.assertTrue(krx._save_db_from_html())

    def test_get_createdate(self):
        self.assertRegex(krx._get_tablename(), '^_\d\d\d\d\d\d$')

    def test_runs(self):
        print(krx.get_codes())
        print(krx.get_name_codes())
        print(krx.get_name('005930'))

    def test_get_df(self):
        print(krx._get_df())

    def test_make_parts(self):
        print(krx.make_parts(30))

    def test_get_codes(self):
        print(krx.get_codes())

