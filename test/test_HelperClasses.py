import unittest
from HelperClasses import *
from mock import patch, Mock, MagicMock, call
from patch_wrapper import PatchWrapper as pw


class TestHelperClasses(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_square_dimensions_from_code(self):
        A1_dimensions = Converter.get_square_dimensions_from_code("A1")
        H8_dimensions = Converter.get_square_dimensions_from_code("H8")
        E3_dimensions = Converter.get_square_dimensions_from_code("E3")
        self.assertEqual(A1_dimensions, (7, 0))
        self.assertEqual(H8_dimensions, (0, 7))
        self.assertEqual(E3_dimensions, (5, 4))

    def test_get_square_code_from_dimensions(self):
        A1_code = Converter.get_square_code_from_dimensions(7, 0)
        H8_code = Converter.get_square_code_from_dimensions(0, 7)
        E3_code = Converter.get_square_code_from_dimensions(5, 4)
        self.assertEqual(A1_code, "A1")
        self.assertEqual(H8_code, "H8")
        self.assertEqual(E3_code, "E3")

if __name__ == '__main__':
    unittest.main()
