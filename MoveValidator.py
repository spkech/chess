from abc import abstractmethod
from HelperClasses import *
import copy


class MoveValidator(object):

    def __init__(self, player, color):
        """Common move validator for all pieces of a given color."""
        self.player = player
        self.color = color

    @staticmethod
    def get_instance(player, piece_object):
        """Returns an instance of a MoveValidator according to the type of object
        passed as argument (pawn, knight, bishop, rook, queen, king)."""
        piece_code = piece_object.code[1]
        piece_color = piece_object.color

        move_validator_instance = None
        if piece_code == "p":
            move_validator_instance = PawnMoveValidator(player, piece_color)
        elif piece_code == "n":
            move_validator_instance = KnightMoveValidator(player, piece_color)
        elif piece_code == "b":
            move_validator_instance = BishopMoveValidator(player, piece_color)
        elif piece_code == "r":
            move_validator_instance = RookMoveValidator(player, piece_color)
        elif piece_code == "q":
            move_validator_instance = QueenMoveValidator(player, piece_color)
        elif piece_code == "k":
            move_validator_instance = KingMoveValidator(player, piece_color)

        return move_validator_instance

    def move_leaves_king_expsoed_to_check(self, src_square, dst_square, gameboard):
        """ Returns true if selected move leaves the king exposed to check. """
        pass

    @abstractmethod
    def get_valid_dst_squares(gameeboard, src_square, dst_square=None):
        """ Returns a list of the squares that the piece in the src_square can move to. """
        raise NotImplementedError

    def is_square_occupied_by_own_piece(self, square):
        """ Returns true if destination square is occupied by a piece of the same color. """
        square_is_occupied_by_own_piece = None
        if square.is_occupied is True:
            if square.occupying_piece.color == self.color:
                square_is_occupied_by_own_piece = True
            else:
                square_is_occupied_by_own_piece = False
        else:
            square_is_occupied_by_own_piece = False
        return square_is_occupied_by_own_piece

    def is_square_occupied_by_opponent_piece(self, square):
        """ Returns true if given square is occupied by an opponent's piece. """
        square_is_occupied_by_opponent_piece = None
        if square.is_occupied is True:
            if square.occupying_piece.color in [WHITE, BLACK] and square.occupying_piece.color != self.color:
                square_is_occupied_by_opponent_piece = True
            else:
                square_is_occupied_by_opponent_piece = False
        else:
            square_is_occupied_by_opponent_piece = False
        return square_is_occupied_by_opponent_piece

    def filter_out_of_bounds_dst_squares(self, allowed_squares):
        """ Filters out any destination squares in allowed_squares list that are out of bounds. """
        filtered_squares = [square for square in allowed_squares if (
            square.row >= 0 and square.row <= 7 and square.col >= 0 and square.col <= 7)]
        return filtered_squares

    def filter_squares_occupied_by_same_color_pieces(self, allowed_squares):
        """ Filters out any destination squares occupied by pieces of the same color as the piece
        in the source square. """

        filtered_squares = [square for square in allowed_squares if not (
            square.is_occupied and square.occupying_piece.color == self.color)]
        return filtered_squares

    def is_move_valid(self, src_square, dst_square, gameboard):
        """ Returns True if pawn move from src_square to dst_square is valid. """
        move_is_valid = True

        valid_dst_squares = self.get_valid_dst_squares(src_square, gameboard, dst_square)
        if dst_square.code not in valid_dst_squares:
            return False
        king_is_safe = self.king_is_safe_after_move(src_square, dst_square, gameboard)
        move_is_valid = move_is_valid and king_is_safe

        # print "move_is_valid: ", move_is_valid
        return move_is_valid

    def king_is_safe_after_move(self, src_square, dst_square, gameboard):
        """ Returns True if the king is safe after the piece in the src_square moves to dst_square. """
        king_is_safe = True
        if gameboard.check:
            # print "I AM BEING CHECKED!"
            opponent = gameboard.get_opponent(self.player)
            new_gameboard = copy.deepcopy(gameboard)   # deep (recursive) copy

            # update squares attributes
            new_gameboard.board[src_square.row][src_square.col].is_occupied = False
            new_gameboard.board[src_square.row][src_square.col].occupying_piece = None
            new_gameboard.board[dst_square.row][dst_square.col].is_occupied = True
            new_gameboard.board[dst_square.row][dst_square.col].occupying_piece = \
                gameboard.board[src_square.row][src_square.col].occupying_piece

            # print "\n---NEW BOARD---\n"
            # self.player.print_board(new_gameboard)

            check = new_gameboard.check_exists(opponent, opponent.available_pieces_positions)
            print "\ncheck NOW is: ", check
            if check is True:
                print "Your king is being checked!"
                king_is_safe = False
        return king_is_safe


class PawnMoveValidator(MoveValidator):
    def __init__(self, player, color):
        """Move validator for a pawn of a given color."""
        super(PawnMoveValidator, self).__init__(player, color)

    def can_capture_opponent_piece(self, src_square, dst_square, board):
        """ Checks if current player's pawn can capture opponent's piece at the given destination square."""
        can_capture = False
        if self.color is WHITE:
            if (src_square.row - dst_square.row == 1) and (abs(src_square.col - dst_square) == 1):
                can_capture = True
        elif self.color is BLACK:
            if (src_square.row - dst_square.row == -1) and (abs(src_square.col - dst_square) == 1):
                can_capture = True
        return can_capture

    def previous_move_satisfies_prerequisites_for_en_passant(self, moves, src_square):
        """ Returns true if the previous move satisfies the following prerequisites for an 'en passan' pawn capture:
            1. The piece that moved in the previous move is a pawn of the opposite color.
            2. The piece (pawn) that moved in the previous move landed on the same row as the current pawn.
            3. The piece (pawn) that moved in the previous move moved two squares forward."""
        previous_move_was_two_squares_forward_by_opponent_piece = False
        if moves != []:
            previous_move = moves[-1]
            if self.color is WHITE:
                previous_move_piece_is_black_pawn = (previous_move['dst_square'].occupying_piece.code == "bp")
                previous_move_piece_is_on_same_row_as_src_pawn = (previous_move['dst_square'].row == src_square.row)
                previous_move_piece_moved_two_squares_forward = \
                    (previous_move['dst_square'].row - previous_move['src_square'].row == 2)

                if previous_move_piece_is_black_pawn and previous_move_piece_is_on_same_row_as_src_pawn and \
                        previous_move_piece_moved_two_squares_forward:
                    previous_move_was_two_squares_forward_by_opponent_piece = True

            elif self.color is BLACK:
                previous_move_piece_is_white_pawn = (previous_move['dst_square'].occupying_piece.code == "wp")
                previous_move_piece_is_on_same_row_as_src_pawn = (previous_move['dst_square'].row == src_square.row)
                previous_move_piece_moved_two_squares_forward = \
                    (previous_move['dst_square'].row - previous_move['src_square'].row == -2)

                if previous_move_piece_is_white_pawn and previous_move_piece_is_on_same_row_as_src_pawn and \
                        previous_move_piece_moved_two_squares_forward:
                    previous_move_was_two_squares_forward_by_opponent_piece = True

            return previous_move_was_two_squares_forward_by_opponent_piece

    def can_capture_opponent_pawn_en_passant(self, src_square, dst_square, gameboard):
        """ Checks if current player's pawn can capture opponent's pawn en passant at the given destination square."""
        moves = gameboard.move_history

        # used when calling 'get_valid_dst_squares' for 'check' checking
        if not dst_square:
            return False

        can_capture = False

        opponent_piece_is_in_adjacent_column = (abs(src_square.col - dst_square.col) == 1)
        dst_square_is_empty = (not dst_square.is_occupied)
        dst_square_is_one_square_forward_for_white = (src_square.row - dst_square.row == 1)
        dst_square_is_one_square_forward_for_black = (src_square.row - dst_square.row == -1)
        previous_move_satisfies_prerequisites_for_en_passant = \
            self.previous_move_satisfies_prerequisites_for_en_passant(moves, src_square)

        if self.color is WHITE:
            if dst_square_is_one_square_forward_for_white and opponent_piece_is_in_adjacent_column and \
                    dst_square_is_empty and previous_move_satisfies_prerequisites_for_en_passant:
                can_capture = True
        elif self.color is BLACK:
            if dst_square_is_one_square_forward_for_black and opponent_piece_is_in_adjacent_column and \
                    dst_square_is_empty and previous_move_satisfies_prerequisites_for_en_passant:
                can_capture = True
        return can_capture

    def get_valid_dst_squares(self, src_square, gameboard, dst_square=None):
        """ Returns a list of the squares that the pawn in the src_square can move to. """

        board = gameboard.board

        src_piece_color = src_square.occupying_piece.color
        (row, col) = (src_square.row, src_square.col)
        allowed_squares = []

        if src_piece_color == WHITE:
            (front_left_square, front_right_square, front_square) = (None, None, None)
            front_left_square_is_in_bounds = (row-1 >= 0) and (col-1 >= 0)
            front_right_square_is_in_bounds = (row-1 >= 0) and (col+1 <= 7)
            front_square_is_in_bounds = (row-1 >= 0)
            if front_left_square_is_in_bounds:
                front_left_square = board[row-1][col-1]
            if front_right_square_is_in_bounds:
                front_right_square = board[row-1][col+1]
            if front_square_is_in_bounds:
                front_square = board[row-1][col]
            # examine front left and right squares for possible opponent pieces
            allowed_squares.append(front_square)
            if front_left_square and front_left_square.is_occupied and \
                    front_left_square.occupying_piece.color is not src_piece_color:
                allowed_squares.append(front_left_square)
            if front_right_square and front_right_square.is_occupied and \
                    front_right_square.occupying_piece.color is not src_piece_color:
                allowed_squares.append(front_right_square)
            if src_square.row == 6:                     # for starting pawns, also add square 2 positions forward
                allowed_squares.append(board[row-2][col])

        elif src_piece_color == BLACK:
            (front_left_square, front_right_square, front_square) = (None, None, None)
            front_left_square_is_in_bounds = (row+1 <= 7) and (col+1 <= 7)
            front_right_square_is_in_bounds = (row+1 <= 7) and (col-1 >= 0)
            front_square_is_in_bounds = (row+1 <= 7)
            if front_left_square_is_in_bounds:
                front_left_square = board[row+1][col+1]
            if front_right_square_is_in_bounds:
                front_right_square = board[row+1][col-1]
            if front_square_is_in_bounds:
                front_square = board[row+1][col]

            allowed_squares.append(front_square)
            if front_left_square and front_left_square.is_occupied and \
                    front_left_square.occupying_piece.color is not src_piece_color:
                allowed_squares.append(front_left_square)
            if front_right_square and front_right_square.is_occupied and \
                    front_right_square.occupying_piece.color is not src_piece_color:
                allowed_squares.append(front_right_square)
            if src_square.row == 1:                     # for starting pawns: moving forward 2 squares is allowed
                allowed_squares.append(board[row+2][col])

        if dst_square and self.can_capture_opponent_pawn_en_passant(src_square, dst_square, gameboard):
            allowed_squares.append(dst_square)
            gameboard.en_passant_square = dst_square

        allowed_squares = self.filter_out_of_bounds_dst_squares(allowed_squares)
        allowed_squares = self.filter_squares_occupied_by_same_color_pieces(allowed_squares)

        allowed_square_codes = [square.code for square in allowed_squares]
        # print "allowed_square_codes: ", allowed_square_codes

        return allowed_square_codes


class KnightMoveValidator(MoveValidator):
    def __init__(self, player, color):
        """Move validator for a knight of a given color."""
        super(KnightMoveValidator, self).__init__(player, color)

    def get_valid_dst_squares(self, src_square, gameboard, dst_square=None):
        """ Returns a list of the squares that the knight in the src_square can move to. """

        board = gameboard.board

        (row, col) = (src_square.row, src_square.col)
        allowed_squares = []

        dst_squares = [(row-1, col-2), (row-1, col+2), (row-2, col+1), (row-2, col-1),
                       (row+1, col-2), (row+1, col+2), (row+2, col+1), (row+2, col-1)]

        for dims in dst_squares:
            (dst_row, dst_col) = (dims[0], dims[1])
            if dst_row >= 0 and dst_row <= 7 and dst_col >= 0 and dst_col <= 7:
                allowed_squares.append(board[dst_row][dst_col])

        allowed_squares = self.filter_out_of_bounds_dst_squares(allowed_squares)
        allowed_squares = self.filter_squares_occupied_by_same_color_pieces(allowed_squares)

        allowed_square_codes = [square.code for square in allowed_squares]
        # print "allowed_square_codes for src_square %s: %s" % (src_square.code, allowed_square_codes)

        return allowed_square_codes


class BishopMoveValidator(MoveValidator):
    def __init__(self, player, color):
        """Move validator for a bishop of a given color."""
        super(BishopMoveValidator, self).__init__(player, color)

    def get_allowed_squares_in_diagonal(self, src_square, partial_diagonal, allowed_squares, board):
        """ Returns a list of the squares in the given partial diagonal that the bishop in the src_square
        can move to. """

        increment = {"top_right_diag": (1, 1),
                     "top_left_diag": (-1, -1),
                     "bottom_right_diag": (-1, 1),
                     "bottom_left_diag": (1, -1)}

        (row, col) = (src_square.row+increment[partial_diagonal][0], src_square.col+increment[partial_diagonal][1])
        while row >= 0 and row <= 7 and col >= 0 and col <= 7:
            if self.is_square_occupied_by_opponent_piece(board[row][col]):
                allowed_squares.append(board[row][col])
                break
            elif self.is_square_occupied_by_own_piece(board[row][col]):
                break
            elif not board[row][col].is_occupied:
                allowed_squares.append(board[row][col])
            (row, col) = (row+increment[partial_diagonal][0], col+increment[partial_diagonal][1])

        return allowed_squares

    def get_valid_dst_squares(self, src_square, gameboard, dst_square=None):
        """ Returns a list of the squares that the bishop in the src_square can move to. """

        board = gameboard.board
        allowed_squares = []

        allowed_squares = self.get_allowed_squares_in_diagonal(src_square, "top_right_diag", allowed_squares, board)
        allowed_squares = self.get_allowed_squares_in_diagonal(src_square, "top_left_diag", allowed_squares, board)
        allowed_squares = self.get_allowed_squares_in_diagonal(src_square, "bottom_right_diag", allowed_squares, board)
        allowed_squares = self.get_allowed_squares_in_diagonal(src_square, "bottom_left_diag", allowed_squares, board)

        allowed_squares = self.filter_out_of_bounds_dst_squares(allowed_squares)
        # allowed_squares = self.filter_squares_occupied_by_same_color_pieces(allowed_squares)

        allowed_square_codes = [square.code for square in allowed_squares]
        # print "allowed_square_codes for src_square %s: %s" % (src_square.code, allowed_square_codes)

        return allowed_square_codes


class RookMoveValidator(MoveValidator):
    def __init__(self, player, color):
        """Move validator for a rook of a given color."""
        super(RookMoveValidator, self).__init__(player, color)

    def get_allowed_squares_in_straight_line(self, src_square, partial_line, allowed_squares, board):
        """ Returns a list of the squares in the given partial straight line that the rook in the src_square
        can move to. """

        increment = {"top": (1, 0),
                     "bottom": (-1, 0),
                     "left": (0, -1),
                     "right": (0, 1)}

        (row, col) = (src_square.row+increment[partial_line][0], src_square.col+increment[partial_line][1])
        while row >= 0 and row <= 7 and col >= 0 and col <= 7:
            if self.is_square_occupied_by_opponent_piece(board[row][col]):
                allowed_squares.append(board[row][col])
                break
            elif self.is_square_occupied_by_own_piece(board[row][col]):
                break
            elif not board[row][col].is_occupied:
                allowed_squares.append(board[row][col])
            (row, col) = (row+increment[partial_line][0], col+increment[partial_line][1])

        return allowed_squares

    def get_valid_dst_squares(self, src_square, gameboard, dst_square=None):
        """ Returns a list of the squares that the bishop in the src_square can move to. """

        board = gameboard.board
        allowed_squares = []

        allowed_squares = self.get_allowed_squares_in_straight_line(src_square, "top", allowed_squares, board)
        allowed_squares = self.get_allowed_squares_in_straight_line(src_square, "bottom", allowed_squares, board)
        allowed_squares = self.get_allowed_squares_in_straight_line(src_square, "left", allowed_squares, board)
        allowed_squares = self.get_allowed_squares_in_straight_line(src_square, "right", allowed_squares, board)

        allowed_squares = self.filter_out_of_bounds_dst_squares(allowed_squares)
        # allowed_squares = self.filter_squares_occupied_by_same_color_pieces(allowed_squares)

        allowed_square_codes = [square.code for square in allowed_squares]
        # print "allowed_square_codes for src_square %s: %s" % (src_square.code, allowed_square_codes)

        return allowed_square_codes


class QueenMoveValidator(MoveValidator):
    def __init__(self, player, color):
        """Move validator for a queen of a given color."""
        super(QueenMoveValidator, self).__init__(player, color)

    def get_allowed_squares_in_diagonal(self, src_square, partial_diagonal, allowed_squares, board):
        """ Returns a list of the squares in the given partial diagonal that the queen in the src_square
        can move to. """

        increment = {"top_right_diag": (1, 1),
                     "top_left_diag": (-1, -1),
                     "bottom_right_diag": (-1, 1),
                     "bottom_left_diag": (1, -1)}

        (row, col) = (src_square.row+increment[partial_diagonal][0], src_square.col+increment[partial_diagonal][1])
        while row >= 0 and row <= 7 and col >= 0 and col <= 7:
            if self.is_square_occupied_by_opponent_piece(board[row][col]):
                allowed_squares.append(board[row][col])
                break
            elif self.is_square_occupied_by_own_piece(board[row][col]):
                break
            elif not board[row][col].is_occupied:
                allowed_squares.append(board[row][col])
            (row, col) = (row+increment[partial_diagonal][0], col+increment[partial_diagonal][1])

        return allowed_squares

    def get_allowed_squares_in_straight_line(self, src_square, partial_line, allowed_squares, board):
        """ Returns a list of the squares in the given partial straight line that the queen in the src_square
        can move to. """

        increment = {"top": (1, 0),
                     "bottom": (-1, 0),
                     "left": (0, -1),
                     "right": (0, 1)}

        (row, col) = (src_square.row+increment[partial_line][0], src_square.col+increment[partial_line][1])
        while row >= 0 and row <= 7 and col >= 0 and col <= 7:
            if self.is_square_occupied_by_opponent_piece(board[row][col]):
                allowed_squares.append(board[row][col])
                break
            elif self.is_square_occupied_by_own_piece(board[row][col]):
                break
            elif not board[row][col].is_occupied:
                allowed_squares.append(board[row][col])
            (row, col) = (row+increment[partial_line][0], col+increment[partial_line][1])

        return allowed_squares

    def get_valid_dst_squares(self, src_square, gameboard, dst_square=None):
        """ Returns a list of the squares that the queen in the src_square can move to. """

        board = gameboard.board
        allowed_squares = []

        allowed_squares = self.get_allowed_squares_in_diagonal(src_square, "top_right_diag", allowed_squares, board)
        allowed_squares = self.get_allowed_squares_in_diagonal(src_square, "top_left_diag", allowed_squares, board)
        allowed_squares = self.get_allowed_squares_in_diagonal(src_square, "bottom_right_diag", allowed_squares, board)
        allowed_squares = self.get_allowed_squares_in_diagonal(src_square, "bottom_left_diag", allowed_squares, board)
        allowed_squares = self.get_allowed_squares_in_straight_line(src_square, "top", allowed_squares, board)
        allowed_squares = self.get_allowed_squares_in_straight_line(src_square, "bottom", allowed_squares, board)
        allowed_squares = self.get_allowed_squares_in_straight_line(src_square, "left", allowed_squares, board)
        allowed_squares = self.get_allowed_squares_in_straight_line(src_square, "right", allowed_squares, board)

        allowed_squares = self.filter_out_of_bounds_dst_squares(allowed_squares)
        # allowed_squares = self.filter_squares_occupied_by_same_color_pieces(allowed_squares)

        allowed_square_codes = [square.code for square in allowed_squares]
        # print "allowed_square_codes for src_square %s: %s" % (src_square.code, allowed_square_codes)

        return allowed_square_codes


class KingMoveValidator(MoveValidator):
    def __init__(self, player, color):
        """Move validator for a king of a given color."""
        super(KingMoveValidator, self).__init__(player, color)

    def get_valid_dst_squares(self, src_square, gameboard, dst_square=None):
        """ Returns a list of the squares that the king in the src_square can move to. """

        board = gameboard.board

        (row, col) = (src_square.row, src_square.col)
        allowed_squares = []

        dst_squares = [(row-1, col), (row+1, col), (row, col-1), (row, col+1),
                       (row-1, col-1), (row-1, col+1), (row+1, col-1), (row+1, col+1)]

        for dims in dst_squares:
            (dst_row, dst_col) = (dims[0], dims[1])
            if dst_row >= 0 and dst_row <= 7 and dst_col >= 0 and dst_col <= 7:
                allowed_squares.append(board[dst_row][dst_col])

        allowed_squares = self.filter_out_of_bounds_dst_squares(allowed_squares)
        allowed_squares = self.filter_squares_occupied_by_same_color_pieces(allowed_squares)

        allowed_square_codes = [square.code for square in allowed_squares]
        # print "allowed_square_codes for src_square %s: %s" % (src_square.code, allowed_square_codes)

        return allowed_square_codes
