import unittest
from Board import *
from mock import patch, Mock, MagicMock, call
from patch_wrapper import PatchWrapper as pw
# from nokia.anscli.lib.anscli_validator import AnscliValidator


class TestBoard(unittest.TestCase):

    def setUp(self):
        pass
        # self.patcher1 = patch.object(YamlDictionary, "create_configuration_dirs_if_not_exist")
        # self.patcher2 = patch("nokia.anscli.lib.anscli_editor.os")

        # self.addCleanup(self.patcher1.stop)
        # self.addCleanup(self.patcher2.stop)

        # self.mock_conf_dirs = self.patcher1.start()
        # self.mock_os = self.patcher2.start()

    def test_get_square_code(self):
        mock_update_lists = pw.patch_object(self, Board, "update_lists")
        board = Board("player1", "player2")

        # board._get_square_code(0,0)

        # self.assertEqual(black_king.code, "bk")

if __name__ == '__main__':
    unittest.main()
