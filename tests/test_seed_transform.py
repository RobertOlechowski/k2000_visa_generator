import unittest
from lib_code.Transform import SeedTransform
from lib_code.Uint32 import Uint32


class TestSeedTransform(unittest.TestCase):
    def setUp(self):
        self.obj = SeedTransform()

    def test_transform(self):
        result1 = self.obj.forward(Uint32.create(0xbc942bb7))
        self.assertEqual(0x5140028a673c79cc, result1.get_long())

        result2 = self.obj.forward(Uint32.create(0xAB760871))
        self.assertEqual(0x256666A4B756D5DA, result2.get_long())


if __name__ == '__main__':
    unittest.main()
