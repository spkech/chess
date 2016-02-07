import unittest
from Piece import *
from mock import patch, Mock, MagicMock, call
from patch_wrapper import PatchWrapper as pw


class TestPiece(unittest.TestCase):

    def setUp(self):
        pass
        # self.patcher1 = patch.object(YamlDictionary, "create_configuration_dirs_if_not_exist")
        # self.patcher2 = patch("nokia.anscli.lib.anscli_editor.os")

        # self.addCleanup(self.patcher1.stop)
        # self.addCleanup(self.patcher2.stop)

        # self.mock_conf_dirs = self.patcher1.start()
        # self.mock_os = self.patcher2.start()

    def test_piece_creation(self):
        white_pawn = Pawn(WHITE)
        white_knight = Knight(WHITE)
        white_bishop = Bishop(WHITE)
        white_rook = Rook(WHITE)
        white_queen = Queen(WHITE)
        white_king = King(WHITE)
        black_pawn = Pawn(BLACK)
        black_knight = Knight(BLACK)
        black_bishop = Bishop(BLACK)
        black_rook = Rook(BLACK)
        black_queen = Queen(BLACK)
        black_king = King(BLACK)

        self.assertEqual(white_pawn.code, "wp")
        self.assertEqual(white_knight.code, "wn")
        self.assertEqual(white_bishop.code, "wb")
        self.assertEqual(white_rook.code, "wr")
        self.assertEqual(white_queen.code, "wq")
        self.assertEqual(white_king.code, "wk")
        self.assertEqual(black_pawn.code, "bp")
        self.assertEqual(black_knight.code, "bn")
        self.assertEqual(black_bishop.code, "bb")
        self.assertEqual(black_rook.code, "br")
        self.assertEqual(black_queen.code, "bq")
        self.assertEqual(black_king.code, "bk")

if __name__ == '__main__':
    unittest.main()
