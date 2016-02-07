from HelperClasses import *


class Square(object):

    def __init__(self, is_occupied, occupying_piece, color=None, code=None, row=None, col=None):
    # def __init__(self, color, code, is_occupied, occupying_piece, row, col):
        """Creates a chess board square."""
        self.color = color                                  # WHITE / BLACK
        self.code = code                                    # A1, E3, H6 etc.
        self.is_occupied = is_occupied
        self.occupying_piece = occupying_piece
        self.row = row
        self.col = col
        self.en_passant = False
        self.assign_missing_attribute_values()

    def assign_missing_attribute_values(self):
        """ Assigns values to any arguments that were not passed to the constructor. """
        if self.code is None:
            self.code = Converter.get_square_code_from_dimensions(self.row, self.col)
        if (self.row is None) and (self.col is None):
            (self.row, self.col) = Converter.get_square_dimensions_from_code(self.code)
        if self.color is None:
            self.color = Converter.get_square_color(self.row, self.col)
