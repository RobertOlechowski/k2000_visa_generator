import unittest
from lib_code.Transform import Transform1
from lib_code.Uint32 import Uint32


class TestTransform1(unittest.TestCase):
    def setUp(self):
        self.obj = Transform1()

    def test_forward(self):
        self.assertEqual(0x249ce4fb, self.obj.forward(Uint32.create(0xAAAABBBB), Uint32.create(0x71c9938e)).get_long())
        self.assertEqual(0x55a13f60, self.obj.forward(Uint32.create(0x12345678), Uint32.create(0x71c9938e)).get_long())
        self.assertEqual(0x71cb938e, self.obj.forward(Uint32.create(0x00010001), Uint32.create(0x71c9938e)).get_long())
        self.assertEqual(0x8e366c73, self.obj.forward(Uint32.create(0xFFFFFFFF), Uint32.create(0x71c9938e)).get_long())
        self.assertEqual(0x8e366c71, self.obj.forward(Uint32.create(0x00000000), Uint32.create(0x71c9938e)).get_long())
        self.assertEqual(0x5E84BA8A, self.obj.forward(Uint32.create(0x3DF16E18), Uint32.create(0x256666A4)).get_long())
        self.assertEqual(0x02000226, self.obj.forward(Uint32.create(0x5AAB6BFF), Uint32.create(0xB756D5DA)).get_long())

    def test_reward(self):
        self.assertEqual(0xAAAABBBB, self.obj.reward(Uint32.create(0x249ce4fb), Uint32.create(0x71c9938e)).get_long())
        self.assertEqual(0x12345678, self.obj.reward(Uint32.create(0x55a13f60), Uint32.create(0x71c9938e)).get_long())
        self.assertEqual(0x00010001, self.obj.reward(Uint32.create(0x71cb938e), Uint32.create(0x71c9938e)).get_long())
        self.assertEqual(0xFFFFFFFF, self.obj.reward(Uint32.create(0x8e366c73), Uint32.create(0x71c9938e)).get_long())
        self.assertEqual(0x00000000, self.obj.reward(Uint32.create(0x8e366c71), Uint32.create(0x71c9938e)).get_long())
        self.assertEqual(0x3DF16E18, self.obj.reward(Uint32.create(0x5E84BA8A), Uint32.create(0x256666A4)).get_long())
        self.assertEqual(0x5AAB6BFF, self.obj.reward(Uint32.create(0x02000226), Uint32.create(0xB756D5DA)).get_long())


if __name__ == '__main__':
    unittest.main()
