from HelperClasses import *


class Piece(object):

    def __init__(self, color):
        """Creates a chess piece."""
        self.color = color      # WHITE / BLACK

    def get_code(self, piece_object):
        """Returns a string code of a given piece. String code differs depending on the piece color."""
        color_code_dict = {WHITE: 'w', BLACK: 'b'}
        type_code_dict = {Pawn: 'p', Knight: 'n', Bishop: 'b', Rook: 'r', Queen: 'q', King: 'k'}
        return color_code_dict[self.color] + type_code_dict[type(piece_object)]

    @staticmethod
    def get_instance(code, color):
        """Returns an instance of a Piece according to the piece code given as an argument."""
        piece_instance = None
        if code:
            instance_dict = {'p': Pawn(color), 'n': Knight(color), 'b': Bishop(color),
                             'r': Rook(color), 'q': Queen(color), 'k': King(color)}
            piece_instance = instance_dict[code[1]]
        return piece_instance

    def __str__(self):
        """ Returns a string representation of the current object. """
        strings = {
            "wk": "white king",
            "wq": "white queen",
            "wr": "white rook",
            "wb": "white bishop",
            "wn": "white knight",
            "wp": "white pawn",
            "bk": "black king",
            "bq": "black queen",
            "br": "black rook",
            "bb": "black bishop",
            "bn": "black knight",
            "bp": "black pawn"
        }
        return strings[self.code]


class Pawn(Piece):

    def __init__(self, color):
        super(Pawn, self).__init__(color)
        self.code = self.get_code(self)


class Knight(Piece):

    def __init__(self, color):
        super(Knight, self).__init__(color)
        self.code = self.get_code(self)


class Bishop(Piece):

    def __init__(self, color):
        super(Bishop, self).__init__(color)
        self.code = self.get_code(self)


class Rook(Piece):

    def __init__(self, color):
        super(Rook, self).__init__(color)
        self.code = self.get_code(self)
        self.has_moved = False


class Queen(Piece):

    def __init__(self, color):
        super(Queen, self).__init__(color)
        self.code = self.get_code(self)


class King(Piece):

    def __init__(self, color):
        super(King, self).__init__(color)
        self.code = self.get_code(self)
        self.has_moved = False
