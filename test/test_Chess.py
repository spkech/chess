import unittest
from Chess import Chess
from mock import patch, Mock, MagicMock, call
from patch_wrapper import PatchWrapper as pw


class TestChess(unittest.TestCase):

    def test_game_creation(self):
        pw.patch_module(self, '__builtin__.raw_input', side_effect=['1', 'Spy', 'Theo', 'w', 'S'])
        Chess.main()

    def test_invalid_move_from(self):
        pw.patch_module(self, '__builtin__.raw_input', side_effect=['1', 'Spy', 'Theo', 'w', 'J3', 'B2', 'S'])
        Chess.main()

    def test_allowed_sequence_of_moves(self):
        pw.patch_module(self, '__builtin__.raw_input', side_effect=[
            '1', 'Spy', 'Theo', 'w',
            'd2', 'd4',
            'E7', 'E5',
            'D4', 'C5',   # invalid
            'D4', 'E5',   # white pawn captures black pawn
            'D7', 'D5',
            # 'g2', 'g3',
            # 'g7', 'g6',
            'E5', 'D6',    # white pawn captures black pawn en passant
            'S'
            ])
        Chess.main()

    def test_allowed_sequence_of_moves_for_knight(self):
        pw.patch_module(self, '__builtin__.raw_input', side_effect=[
            '1', 'Spy', 'Theo', 'w',
            'g1', 'F4',   # invalid
            'g1', 'F3',   # white knight move
            'd7', 'd6',
            'f3', 'e1',
            'S'
            ])
        Chess.main()

    def test_allowed_sequence_of_moves_for_bishop(self):
        pw.patch_module(self, '__builtin__.raw_input', side_effect=[
            '1', 'Spy', 'Theo', 'w',
            'g1', 'h3',    # white knight move
            'd7', 'd6',    # black pawn move
            'd2', 'd4',    # white pawn move
            'c8', 'e6',    # black bishop move
            'b2', 'b3',    # dummy pawn move
            'e6', 'h3',
            'c1', 'f4',
            'S'
            ])
        Chess.main()

    def test_allowed_sequence_of_moves_for_rook(self):
        pw.patch_module(self, '__builtin__.raw_input', side_effect=[
            '1', 'Spy', 'Theo', 'w',
            'h2', 'h4',    # white pawn move
            'e7', 'e5',    # black pawn move
            'h4', 'h5',    # white pawn move
            'f8', 'b4',    # black bishop move
            'h1', 'h6',    # invalid white rook move
            'h1', 'h4',    # white rook move
            'a7', 'a5',    # black pawn move
            'h4', 'e5',    # invalid white rook move
            'h4', 'b4',
            'S'
            ])
        Chess.main()

    def test_allowed_sequence_of_moves_for_queen(self):
        pw.patch_module(self, '__builtin__.raw_input', side_effect=[
            '1', 'Spy', 'Theo', 'w',
            'e2', 'e4',    # white pawn move
            'd7', 'd5',    # black pawn move
            'd1', 'f3',    # white queen move
            'a7', 'a6',    # black pawn move
            'f3', 'f7',
            'S'
            ])
        Chess.main()

    def test_allowed_sequence_of_moves_for_king(self):
        pw.patch_module(self, '__builtin__.raw_input', side_effect=[
            '1', 'Spy', 'Theo', 'w',
            'e2', 'e4',    # white pawn move
            'e7', 'e5',    # black pawn move
            'd2', 'd4',    # white pawn move
            'd7', 'd5',    # black pawn move
            'e1', 'd1',    # invalid white king move
            'e1', 'e2',    # valid white king move
            'e8', 'd7',    # valid black king move
            'e2', 'f3',
            'd5', 'e4',
            'S'
            ])
        Chess.main()

    def test_allowed_sequence_of_moves_for_check(self):
        pw.patch_module(self, '__builtin__.raw_input', side_effect=[
            '1', 'Spy', 'Theo', 'w',
            'e2', 'e4',    # white pawn move
            'd7', 'D5',    # black pawn move
            'f1', 'b5',
            'c7', 'c5',
            'g7', 'g5',
            'c7', 'c6',
            'S'
            ])
        Chess.main()

    def test_fools_mate(self):
        pw.patch_module(self, '__builtin__.raw_input', side_effect=[
            '1', 'Spy', 'Theo', 'w',
            'f2', 'f3',    # white pawn move
            'e7', 'e5',    # black pawn move
            'g2', 'g4',
            'd8', 'h4',
            'S'
            ])
        Chess.main()

    def test_pawn_promotion(self):
        pw.patch_module(self, '__builtin__.raw_input', side_effect=[
            '1', 'Spy', 'Theo', 'w',
            'c2', 'c4',    # white pawn move
            'c7', 'c6',    # black pawn move
            'd1', 'a4',
            'g7', 'g6',
            'a4', 'c6',
            'h7', 'h6',
            'c6', 'f3',
            'h6', 'h5',
            'c4', 'c5',
            'h5', 'h4',
            'c5', 'c6',
            'd8', 'a5',
            'c6', 'c7',
            'b7', 'b5',
            'g2', 'g3',
            'c8', 'a6',
            'g3', 'g4',
            'b5', 'b4',
            'e2', 'e3',
            'a6', 'b5',
            'd2', 'd3',
            'a5', 'a4',
            'c7', 'b8', '1',
            'S'
            ])
        Chess.main()

    def test_scholars_mate(self):
        pw.patch_module(self, '__builtin__.raw_input', side_effect=[
            '1', 'Spy', 'Theo', 'w',
            'e2', 'e4',    # white pawn move
            'e7', 'e5',    # black pawn move
            'd1', 'h5',
            'b8', 'c6',
            'f1', 'c4',
            'g8', 'f6',
            'h5', 'f7',     # white queen check and mate
            'S'
            ])
        Chess.main()

    def test_smothered_mate_with_knight(self):
        pw.patch_module(self, '__builtin__.raw_input', side_effect=[
            '1', 'Spy', 'Theo', 'w',
            'g1', 'f3',    # white knight move
            'g7', 'g5',    # black pawn move
            'f3', 'g5',
            'f8', 'h6',
            'g5', 'e6',
            'h6', 'f4',
            'a2', 'a3',
            'g8', 'h6',
            'a3', 'a4',
            'h8', 'f8',
            'e6', 'g7',
            'S'
            ])
        Chess.main()

    def test_short_castling_for_white(self):
        pw.patch_module(self, '__builtin__.raw_input', side_effect=[
            '1', 'Spy', 'Theo', 'w',
            'e2', 'e4',    # white knight move
            'g7', 'g5',    # black pawn move
            'g1', 'f3',
            'f8', 'h6',
            'f1', 'c4',
            'a7', 'a5',
            'e1', 'g1',
            'S'
            ])
        Chess.main()

    def test_long_castling_for_white(self):
        pw.patch_module(self, '__builtin__.raw_input', side_effect=[
            '1', 'Spy', 'Theo', 'w',
            'd2', 'd4',    # white knight move
            'e7', 'e6',    # black pawn move
            'c1', 'f4',
            'd8', 'g5',
            'b1', 'c3',
            'g5', 'f4',
            'd1', 'd3',
            'f4', 'd6',    #d2
            'e1', 'c1',
            'S'
            ])
        Chess.main()

    def test_long_castling_for_black(self):
        pw.patch_module(self, '__builtin__.raw_input', side_effect=[
            '1', 'Spy', 'Theo', 'w',
            'e2', 'e3',    # white knight move
            'd7', 'd5',    # black pawn move
            'e3', 'e4',
            'b8', 'c6',
            'd2', 'd3',
            'c8', 'f5',
            'd3', 'd4',
            'd8', 'd6',
            'c2', 'c3',
            'e8', 'c8',
            'S'
            ])
        Chess.main()

    def test_short_castling_for_black(self):
        pw.patch_module(self, '__builtin__.raw_input', side_effect=[
            '1', 'Spy', 'Theo', 'w',
            'e2', 'e3',    # white knight move
            'e7', 'e5',    # black pawn move
            'd1', 'g4',
            'g8', 'f6',
            'd2', 'd3',
            'f8', 'c5',
            'g4', 'f5',
            'h7', 'h6',
            'f5', 'h7',
            'a7', 'a6',
            'h7', 'h6',
            'e8', 'g8',
            'S'
            ])
        Chess.main()

    def test_stalemate(self):
        pw.patch_module(self, '__builtin__.raw_input', side_effect=[
            '1', 'Spy', 'Theo', 'w',
            'a2', 'a4',    # white knight move
            'a7', 'a5',    # black pawn move
            'b2', 'b4',
            'b7', 'b5',
            'c2', 'c4',
            'c7', 'c5',
            'd2', 'd4',
            'd7', 'd5',
            'e2', 'e4',
            'e7', 'e5',
            'f2', 'f4',
            'g8', 'f6',
            'g2', 'g3',
            'g7', 'g5',
            'h2', 'h4',
            'h7', 'h5',
            'd1', 'h5',
            'a8', 'a6',
            'h5', 'h8',
            'a6', 'a8',
            'h8', 'g8',
            'a8', 'a6',
            'g8', 'f8',
            'e8', 'd7',
            'f8', 'c5',
            'a6', 'a7',
            'c5', 'c8',
            'd7', 'e8',
            'c8', 'b8',
            'g5', 'g4',
            'b8', 'a8',
            'b5', 'a4',
            'a1', 'a4',
            'a5', 'b4',
            'a4', 'b4',
            'e8', 'f8',
            'f4', 'e5',
            'f8', 'g7',
            'a8', 'd8',
            'f6', 'e4',
            'f1', 'd3',
            'g7', 'h7',
            'c4', 'd5',
            'h7', 'g7',
            'd3', 'e4',
            'f7', 'f6',
            'e5', 'f6',
            'g7', 'f7',
            'h1', 'h2',
            'a7', 'a4',
            'b4', 'a4',       # should be stalemate
            'S'
            ])
        Chess.main()

    def test_that_white_pawn_moving_forward_three_squares_is_not_allowed(self):
        pw.patch_module(self, '__builtin__.raw_input', side_effect=['1', 'Spy', 'Theo', 'w', 'B2', 'B5', 'S'])
        Chess.main()

    def test_that_already_moved_white_pawn_moving_forward_two_squares_is_not_allowed(self):
        pw.patch_module(self, '__builtin__.raw_input', side_effect=['1', 'Spy', 'Theo', 'w', 'B3', 'B5', 'S'])
        Chess.main()

    def test_change_turn(self):
        pw.patch_module(self, '__builtin__.raw_input', side_effect=['1', 'Spy', 'Theo', 'w', 'B2', 'B5', 'S'])


if __name__ == '__main__':
    unittest.main()
    # unittest.main(verbosity=0, buffer=True, exit=False)
