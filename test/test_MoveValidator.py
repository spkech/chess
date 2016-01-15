import unittest
from Square import Square
from MoveValidator import MoveValidator
from HelperClasses import *
from Piece import *
from Board import Board
from mock import patch, Mock, MagicMock, call
from patch_wrapper import PatchWrapper as pw


class TestMoveValidator(unittest.TestCase):

    def setUp(self):
        pass

    def test_that_pawn_moving_backwards_is_not_allowed(self):
        board = Board().board
        # white
        white_pawn = Pawn("white")
        from_square = Square("white", "E2", True, white_pawn, 6, 4)
        to_square = Square("black", "E1", False, None, 7, 4)
        validator = MoveValidator.get_instance(white_pawn)
        is_move_valid = validator.is_move_valid(from_square, to_square, board)
        self.assertEqual(is_move_valid, False)
        # black
        black_pawn = Pawn("black")
        from_square = Square("black", "E7", True, black_pawn, 1, 4)
        to_square = Square("white", "E8", False, None, 0, 4)
        validator = MoveValidator.get_instance(black_pawn)
        is_move_valid = validator.is_move_valid(from_square, to_square, board)
        self.assertEqual(is_move_valid, False)

    def test_that_pawn_moving_to_the_same_square_it_is_located_on_is_not_allowed(self):
        board = Board().board
        # white
        white_pawn = Pawn("white")
        from_square = Square("white", "E2", True, white_pawn, 6, 4)
        to_square = Square("white", "E2", True, white_pawn, 6, 4)
        validator = MoveValidator.get_instance(white_pawn)
        is_move_valid = validator.is_move_valid(from_square, to_square, board)
        self.assertEqual(is_move_valid, False)
        # black
        black_pawn = Pawn("black")
        from_square = Square("black", "E7", True, black_pawn, 1, 4)
        to_square = Square("black", "E7", True, black_pawn, 1, 4)
        validator = MoveValidator.get_instance(black_pawn)
        is_move_valid = validator.is_move_valid(from_square, to_square, board)
        self.assertEqual(is_move_valid, False)

    def test_that_pawn_moving_forward_more_than_two_squares_is_not_allowed(self):
        board = Board().board
        # white
        white_pawn = Pawn("white")
        from_square = Square("white", "E2", True, white_pawn, 6, 4)
        to_square = Square("black", "E5", False, None, 3, 4)
        validator = MoveValidator.get_instance(white_pawn)
        is_move_valid = validator.is_move_valid(from_square, to_square, board)
        self.assertEqual(is_move_valid, False)
        # black
        black_pawn = Pawn("black")
        from_square = Square("black", "E7", True, black_pawn, 1, 4)
        to_square = Square("white", "E4", False, None, 4, 4)
        validator = MoveValidator.get_instance(black_pawn)
        is_move_valid = validator.is_move_valid(from_square, to_square, board)
        self.assertEqual(is_move_valid, False)


if __name__ == '__main__':
    unittest.main()
