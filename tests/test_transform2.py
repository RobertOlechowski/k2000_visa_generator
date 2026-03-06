import unittest
from lib_code.Transform import Transform2
from lib_code.Uint32 import Uint32


class TestTransform2(unittest.TestCase):
    def setUp(self):
        self.obj = Transform2()

    def test_forward(self):
        self.assertEqual(0x2000211, self.obj.forward(Uint32.create(0xaa99448a)).get_long())
        self.assertEqual(0x20002c5, self.obj.forward(Uint32.create(0xddf811df)).get_long())
        self.assertEqual(0x200029f, self.obj.forward(Uint32.create(0x249ce4fb)).get_long())


if __name__ == '__main__':
    unittest.main()
