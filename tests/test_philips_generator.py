import unittest
from datetime import datetime
from lib_code.PhilipsGenerator import PhilipsGenerator


class TestPhilipsGenerator(unittest.TestCase):
    def test_generate(self):
        current_time = datetime(2019, 4, 1, 18, 0, 10)
        gen = PhilipsGenerator()
        result = gen.generate(dev_id="AB76-0871", days=4, current_time=current_time)
        self.assertEqual("3CE0-C553-DAAB-6A1B", result['code'])
        expected_valid_until = datetime(2019, 4, 6, 0, 0, 0)
        self.assertEqual(expected_valid_until, result['valid_until'])


if __name__ == '__main__':
    unittest.main()
