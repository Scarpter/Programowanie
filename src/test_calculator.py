import unittest
from src.unittest.calculator import add, divide

# assertGreater; assertLess ...
# assertNotEqual
# assertTrue, assertFalse
# assertIn


class TestCalculator(unittest.TestCase):

    def test_add(self):
        cases = [((2, 3), 5), ((-2, 3), 1), ((5, -1), 4), ((-2, -4), -6)]

        for num, ((x, y), expected_result) in enumerate(cases):
            with self.subTest(msg=f'Case {num}'):
                self.assertEqual(add(x, y), expected_result)

    def test_divide_by_zero(self):

        with self.assertRaises(ValueError):
            divide(2, 0)


if __name__ == "__main__":
    unittest.main()