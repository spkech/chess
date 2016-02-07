import unittest
from Board import *
from Player import *
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
        player1 = Player("spy", WHITE)
        player2 = Player("theo", BLACK)
        board = Board([player1, player2])


if __name__ == '__main__':
    unittest.main()
