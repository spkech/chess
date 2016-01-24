from Board import Board


class Game(object):

    def __init__(self, player1, player2):
        """Creates a chess game."""
        self.board = Board([player1, player2])
        self.board.update_lists()
