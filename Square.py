class Square(object):

    def __init__(self, color, code, is_occupied, occupying_piece, row, col):
        """Creates a chess board square."""
        self.color = color                                  # WHITE / BLACK
        self.code = code                                    # A1, E3, H6 etc.
        self.is_occupied = is_occupied
        self.occupying_piece = occupying_piece
        self.row = row
        self.col = col
        self.en_passant = False
