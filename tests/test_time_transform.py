import unittest
from app.Transform import TimeTransform
from app.Uint64 import Uint64


class TestTimeTransform(unittest.TestCase):
    def setUp(self):
        self.obj = TimeTransform()

    def test_transform(self):
        result = self.obj.forward(Uint64.create(0x1D3BE0AAC1A6D16))
        self.assertEqual(0x5aad3e4d, result.get_long())


if __name__ == '__main__':
    unittest.main()
