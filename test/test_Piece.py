import unittest
from Piece import *
from mock import patch, Mock, MagicMock, call
from patch_wrapper import PatchWrapper as pw
# from nokia.anscli.lib.anscli_validator import AnscliValidator


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
        white_pawn = Pawn("white")
        white_knight = Knight("white")
        white_bishop = Bishop("white")
        white_rook = Rook("white")
        white_queen = Queen("white")
        white_king = King("white")
        black_pawn = Pawn("black")
        black_knight = Knight("black")
        black_bishop = Bishop("black")
        black_rook = Rook("black")
        black_queen = Queen("black")
        black_king = King("black")

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
