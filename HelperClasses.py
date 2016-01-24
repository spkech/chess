WHITE = 0
BLACK = 1


class Printer(object):

    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    BLOCK = u"\u2588"

    WHITE_KING = u"\u2654"
    WHITE_QUEEN = u"\u2655"
    WHITE_ROOK = u"\u2656"
    WHITE_BISHOP = u"\u2657"
    WHITE_KNIGHT = u"\u2658"
    WHITE_PAWN = u"\u2659"

    BLACK_KING = u"\u265A"
    BLACK_QUEEN = u"\u265B"
    BLACK_ROOK = u"\u265C"
    BLACK_BISHOP = u"\u265D"
    BLACK_KNIGHT = u"\u265E"
    BLACK_PAWN = u"\u265F"

    symbols = {
        "wk": WHITE_KING,
        "wq": WHITE_QUEEN,
        "wr": WHITE_ROOK,
        "wb": WHITE_BISHOP,
        "wn": WHITE_KNIGHT,
        "wp": WHITE_PAWN,
        "bk": BLACK_KING,
        "bq": BLACK_QUEEN,
        "br": BLACK_ROOK,
        "bb": BLACK_BISHOP,
        "bn": BLACK_KNIGHT,
        "bp": BLACK_PAWN
    }


class Converter(object):

    @staticmethod
    def get_square_dimensions_from_code(code):
        """ Returns square dimensions (row, col) given the square code ('A1', 'A2', 'A3' etc)."""
        letter = code[0]
        row_num = code[1]
        col = ord(letter) - ord('A')
        row = 8 - int(row_num)
        return (row, col)

    @staticmethod
    def get_squares_codes_from_squares(squares_list):
        """ Returns a list with the square codes corresponding to the squares in squares_list."""
        return [square.code for square in squares_list]

    @staticmethod
    def get_square_code_from_dimensions(row, col):
        """ Returns square code ('A1', 'A2', 'A3' etc)."""
        row = 7 - row + 1                    # numbers start from 1, while rows start from 0
        square_code = chr(col + ord('A'))    # get first char from number (0->'A', 1->'B' etc.)
        square_code += str(row)
        return square_code

    @staticmethod
    def get_square_object_from_code(code, board_position):
        """ Returns the square object corresponding to a given square code ('A1', 'A2', 'A3' etc)."""
        (row, col) = Converter.get_square_dimensions_from_code(code)
        return board_position[row][col]

    @staticmethod
    def get_square_color(row, col):
        """ Returns square color ('black' or 'white'). """
        square_color = None
        if (row + col) % 2 == 0:
            square_color = WHITE
        elif (row + col) % 2 == 1:
            square_color = BLACK
        return square_color

    @staticmethod
    def is_square_occupied_at_board_setup(row, col):
        """ Returns True if the square in the given dimensions is occupied by a chess piece."""
        is_square_occupied = None
        if row in [0, 1, 6, 7]:
            is_square_occupied = True
        elif row in [2, 3, 4, 5]:
            is_square_occupied = False
        return is_square_occupied

    @staticmethod
    def get_code_of_occupying_piece_at_board_setup(row, col):
        """ Returns the string code of the piece that occupies the square of the given dimensions.
        Works for board starting position only. """

        # keys are (row, col) tuples (e.g. (0, 1)), values are string codes of pieces (e.g. 'br', 'wq')
        pieces_at_setup_dict = {
            (0, 0): "br", (0, 7): "br", (0, 1): "bn", (0, 6): "bn",
            (0, 2): "bb", (0, 5): "bb", (0, 3): "bq", (0, 4): "bk",
            (1, 0): "bp", (1, 1): "bp", (1, 2): "bp", (1, 3): "bp",
            (1, 4): "bp", (1, 5): "bp", (1, 6): "bp", (1, 7): "bp",
            (7, 0): "wr", (7, 7): "wr", (7, 1): "wn", (7, 6): "wn",
            (7, 2): "wb", (7, 5): "wb", (7, 3): "wq", (7, 4): "wk",
            (6, 0): "wp", (6, 1): "wp", (6, 2): "wp", (6, 3): "wp",
            (6, 4): "wp", (6, 5): "wp", (6, 6): "wp", (6, 7): "wp"
        }

        square_is_occupied_by = None
        if Converter.is_square_occupied_at_board_setup(row, col):
            square_is_occupied_by = pieces_at_setup_dict[(row, col)]

        return square_is_occupied_by

    @staticmethod
    def get_color_of_occupying_piece_at_board_setup(row, col):
        """ Returns the color of the piece that occupies the square of the given dimensions.
        Works for board starting position only. """
        piece_color = None
        if row in [0, 1]:
            piece_color = BLACK
        elif row in [6, 7]:
            piece_color = WHITE
        return piece_color
