from HelperClasses import *


class Piece(object):

    def __init__(self, color):
        """Creates a chess piece."""
        self.color = color      # WHITE / BLACK

    def get_code(self, piece_object):
        """Returns a string code of a given piece. String code differs depending on the piece color."""

        code = ""
        if self.color == WHITE:
            code = "w"
        elif self.color == BLACK:
            code = "b"

        if type(piece_object) is Pawn:
            code += "p"
        elif type(piece_object) is Knight:
            code += "n"
        elif type(piece_object) is Bishop:
            code += "b"
        elif type(piece_object) is Rook:
            code += "r"
        elif type(piece_object) is Queen:
            code += "q"
        elif type(piece_object) is King:
            code += "k"

        return code

    @staticmethod
    def get_instance(piece_code, piece_color):
        """Returns an instance of a Piece according to the piece code given as an argument."""
        piece_instance = None

        if piece_code is not None:
            piece_code_part = piece_code[1]
            if piece_code_part == "p":
                piece_instance = Pawn(piece_color)
            elif piece_code_part == "n":
                piece_instance = Knight(piece_color)
            elif piece_code_part == "b":
                piece_instance = Bishop(piece_color)
            elif piece_code_part == "r":
                piece_instance = Rook(piece_color)
            elif piece_code_part == "q":
                piece_instance = Queen(piece_color)
            elif piece_code_part == "k":
                piece_instance = King(piece_color)

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
