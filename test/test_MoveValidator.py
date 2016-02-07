import unittest
from Square import Square
from MoveValidator import MoveValidator
from HelperClasses import *
from Piece import *
from Player import Player
from Board import Board
from mock import patch, Mock, MagicMock, call
from patch_wrapper import PatchWrapper as pw


class TestMoveValidator(unittest.TestCase):

    def setUp(self):
        pass

    def test_that_pawn_moving_backwards_is_not_allowed(self):
        (white, black) = Player("John", WHITE), Player("Jane", BLACK)
        board = Board([white, black])
        # white
        white_pawn = Pawn(WHITE)
        from_square = Square(True, white_pawn, code="E2")
        to_square = Square(False, None, code="E1")
        validator = MoveValidator.get_instance(white, white_pawn)
        is_move_valid = validator.is_move_valid(from_square, to_square, board)
        self.assertEqual(is_move_valid, False)
        # black
        black_pawn = Pawn(BLACK)
        from_square = Square(True, black_pawn, code="E7")
        to_square = Square(False, None, code="E8")
        validator = MoveValidator.get_instance(black, black_pawn)
        is_move_valid = validator.is_move_valid(from_square, to_square, board)
        self.assertEqual(is_move_valid, False)

    def test_that_pawn_moving_to_the_same_square_it_is_located_on_is_not_allowed(self):
        (white, black) = Player("John", WHITE), Player("Jane", BLACK)
        board = Board([white, black])
        # white
        white_pawn = Pawn(WHITE)
        from_square = Square(True, white_pawn, code="E2")
        to_square = Square(True, white_pawn, code="E2")
        validator = MoveValidator.get_instance(white, white_pawn)
        is_move_valid = validator.is_move_valid(from_square, to_square, board)
        self.assertEqual(is_move_valid, False)
        # black
        black_pawn = Pawn(BLACK)
        from_square = Square(True, black_pawn, code="E7")
        to_square = Square(True, black_pawn, code="E7")
        validator = MoveValidator.get_instance(black, black_pawn)
        is_move_valid = validator.is_move_valid(from_square, to_square, board)
        self.assertEqual(is_move_valid, False)

    def test_that_pawn_moving_forward_more_than_two_squares_is_not_allowed(self):
        (white, black) = Player("John", WHITE), Player("Jane", BLACK)
        board = Board([white, black])
        # white
        white_pawn = Pawn(WHITE)
        from_square = Square(True, white_pawn, code="E2")
        to_square = Square(False, None, code="E5")
        validator = MoveValidator.get_instance(white, white_pawn)
        is_move_valid = validator.is_move_valid(from_square, to_square, board)
        self.assertEqual(is_move_valid, False)
        # black
        black_pawn = Pawn(BLACK)
        from_square = Square(True, black_pawn, code="E7")
        to_square = Square(False, None, code="E4")
        validator = MoveValidator.get_instance(black, black_pawn)
        is_move_valid = validator.is_move_valid(from_square, to_square, board)
        self.assertEqual(is_move_valid, False)


if __name__ == '__main__':
    unittest.main()
