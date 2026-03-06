import unittest
from datetime import datetime
from lib_code.TimeHelper import TimeHelper


class TestTimeHelper(unittest.TestCase):
    def setUp(self):
        self.obj = TimeHelper()

    def test_get_ms_time(self):
        result1 = self.obj.get_ms_time(datetime(2020, 4, 1, 18, 0, 10))
        self.assertEqual(132302376100000000, result1.get_long())
        result2 = self.obj.get_ms_time(datetime(2020, 4, 15, 18, 0, 10))
        self.assertEqual(132314472100000000, result2.get_long())
        result3 = self.obj.get_ms_time(datetime(2030, 4, 1, 18, 0, 10))
        self.assertEqual(135457704100000000, result3.get_long())


if __name__ == '__main__':
    unittest.main()
