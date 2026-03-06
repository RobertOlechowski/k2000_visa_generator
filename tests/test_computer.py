import unittest
from datetime import datetime
from lib_code.Computer import Computer
from lib_code.Uint32 import Uint32


class TestComputer(unittest.TestCase):
    def setUp(self):
        self.obj = Computer()

    def test_compute_code(self):
        dev_id = Uint32.create(0xAB760871)
        result1 = self.obj.compute_code(dev_id, datetime(2020, 4, 1, 18, 0, 10))
        self.assertEqual(0x3DF158085AAB6BDD, result1.get_long())
        result2 = self.obj.compute_code(dev_id, datetime(2030, 4, 1, 18, 0, 10))
        self.assertEqual(0x2A1A8D085AAB6A19, result2.get_long())
        result3 = self.obj.compute_code(dev_id, datetime(2020, 4, 15, 18, 0, 10))
        self.assertEqual(0x3DF896885AAB6A19, result3.get_long())


if __name__ == '__main__':
    unittest.main()
