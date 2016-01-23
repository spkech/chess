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

    @abstractmethod
    def get_valid_dst_squares(gameboard, src_square, dst_square=None):
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
        # print "valid_dst_squares: ", valid_dst_squares
        if dst_square.code not in valid_dst_squares:
            return False
        king_is_safe = self.king_is_safe_after_move(src_square, dst_square, gameboard)
        move_is_valid = move_is_valid and king_is_safe

        # print "move_is_valid: ", move_is_valid
        return move_is_valid

    def king_is_safe_after_move(self, src_square, dst_square, gameboard):
        """ Returns True if the king is safe after the piece in the src_square moves to dst_square. """
        king_is_safe = True
        # print "IN   KING_IS_SAFE_AFTER_MOVE (MoveValidator)!"
        opponent = gameboard.get_opponent(self.player)
        new_gameboard = copy.deepcopy(gameboard)

        # update squares attributes
        new_gameboard.board[dst_square.row][dst_square.col].is_occupied = True
        new_gameboard.board[dst_square.row][dst_square.col].occupying_piece = \
            gameboard.board[src_square.row][src_square.col].occupying_piece
        new_gameboard.board[src_square.row][src_square.col].is_occupied = False
        new_gameboard.board[src_square.row][src_square.col].occupying_piece = None


        if self.player.color is WHITE:
            new_gameboard.update_lists(self.player, opponent)
        else:
            new_gameboard.update_lists(opponent, self.player)

        check = new_gameboard.check_exists(opponent, new_gameboard.avl_pieces_positions[opponent.color])

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

    def previous_move_satisfies_conditions_for_en_passant(self, moves, src_square):
        """ Returns true if the previous move satisfies the following conditions for an 'en passan' pawn capture:
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

                if previous_move_piece_is_black_pawn and\
                    previous_move_piece_is_on_same_row_as_src_pawn and \
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
        previous_move_satisfies_conditions_for_en_passant = \
            self.previous_move_satisfies_conditions_for_en_passant(moves, src_square)

        if self.color is WHITE:
            if dst_square_is_one_square_forward_for_white and opponent_piece_is_in_adjacent_column and \
                    dst_square_is_empty and previous_move_satisfies_conditions_for_en_passant:
                can_capture = True
        elif self.color is BLACK:
            if dst_square_is_one_square_forward_for_black and opponent_piece_is_in_adjacent_column and \
                    dst_square_is_empty and previous_move_satisfies_conditions_for_en_passant:
                can_capture = True
        return can_capture

    def get_valid_dst_squares(self, src_square, gameboard, dst_square=None, castling=False):
        """ Returns a list of the squares that the pawn in the src_square can move to. """

        board = gameboard.board

        src_piece_color = src_square.occupying_piece.color
        (row, col) = (src_square.row, src_square.col)
        allowed_squares = []

        if src_piece_color == WHITE:
            (front_left_square, front_right_square, front_square, front_leap_square) = (None, None, None, None)
            front_left_square_is_in_bounds = (row-1 >= 0) and (col-1 >= 0)
            front_right_square_is_in_bounds = (row-1 >= 0) and (col+1 <= 7)
            front_square_is_in_bounds = (row-1 >= 0)
            if front_left_square_is_in_bounds:
                front_left_square = board[row-1][col-1]
            if front_right_square_is_in_bounds:
                front_right_square = board[row-1][col+1]
            if front_square_is_in_bounds:
                front_square = board[row-1][col]
            if src_square.row == 6:
                front_leap_square = board[row-2][col]
            # examine front left and right squares for possible opponent pieces
            if not front_square.is_occupied:
                allowed_squares.append(front_square)

            if front_left_square and front_left_square.is_occupied and \
                    front_left_square.occupying_piece.color is not src_piece_color:
                allowed_squares.append(front_left_square)
            if front_right_square and front_right_square.is_occupied and \
                    front_right_square.occupying_piece.color is not src_piece_color:
                allowed_squares.append(front_right_square)
            # for starting pawns, also add square 2 positions forward)
            if src_square.row == 6 and not front_leap_square.is_occupied:
                allowed_squares.append(board[row-2][col])

        elif src_piece_color == BLACK:
            (front_left_square, front_right_square, front_square, front_leap_square) = (None, None, None, None)
            front_left_square_is_in_bounds = (row+1 <= 7) and (col+1 <= 7)
            front_right_square_is_in_bounds = (row+1 <= 7) and (col-1 >= 0)
            front_square_is_in_bounds = (row+1 <= 7)
            if front_left_square_is_in_bounds:
                front_left_square = board[row+1][col+1]
            if front_right_square_is_in_bounds:
                front_right_square = board[row+1][col-1]
            if front_square_is_in_bounds:
                front_square = board[row+1][col]
            if src_square.row == 1:
                front_leap_square = board[row+2][col]

            if not front_square.is_occupied:
                allowed_squares.append(front_square)

            if front_left_square and front_left_square.is_occupied and \
                    front_left_square.occupying_piece.color is not src_piece_color:
                allowed_squares.append(front_left_square)
            if front_right_square and front_right_square.is_occupied and \
                    front_right_square.occupying_piece.color is not src_piece_color:
                allowed_squares.append(front_right_square)
            # for starting pawns: moving forward 2 squares is allowed
            if src_square.row == 1 and not front_leap_square.is_occupied:
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

    def get_valid_dst_squares(self, src_square, gameboard, dst_square=None, castling=False):
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

        (row, col) = (src_square.row+increment[partial_diagonal][0], src_square.col + increment[partial_diagonal][1])
        while row >= 0 and row <= 7 and col >= 0 and col <= 7:
            if self.is_square_occupied_by_opponent_piece(board[row][col]):
                allowed_squares.append(board[row][col])
                break
            elif self.is_square_occupied_by_own_piece(board[row][col]):
                break
            elif not board[row][col].is_occupied:
                allowed_squares.append(board[row][col])
            (row, col) = (row + increment[partial_diagonal][0], col + increment[partial_diagonal][1])

        return allowed_squares

    def get_valid_dst_squares(self, src_square, gameboard, dst_square=None, castling=False):
        """ Returns a list of the squares that the bishop in the src_square can move to. """

        board = gameboard.board
        allowed_squares = []

        allowed_squares = self.get_allowed_squares_in_diagonal(src_square, "top_right_diag", allowed_squares, board)
        allowed_squares = self.get_allowed_squares_in_diagonal(src_square, "top_left_diag", allowed_squares, board)
        allowed_squares = self.get_allowed_squares_in_diagonal(src_square, "bottom_right_diag", allowed_squares, board)
        allowed_squares = self.get_allowed_squares_in_diagonal(src_square, "bottom_left_diag", allowed_squares, board)

        allowed_squares = self.filter_out_of_bounds_dst_squares(allowed_squares)
        allowed_squares = self.filter_squares_occupied_by_same_color_pieces(allowed_squares)

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

        (row, col) = (src_square.row+increment[partial_line][0], src_square.col + increment[partial_line][1])
        while row >= 0 and row <= 7 and col >= 0 and col <= 7:
            if self.is_square_occupied_by_opponent_piece(board[row][col]):
                allowed_squares.append(board[row][col])
                break
            elif self.is_square_occupied_by_own_piece(board[row][col]):
                break
            elif not board[row][col].is_occupied:
                allowed_squares.append(board[row][col])
            (row, col) = (row + increment[partial_line][0], col + increment[partial_line][1])

        return allowed_squares

    def get_valid_dst_squares(self, src_square, gameboard, dst_square=None, castling=False):
        """ Returns a list of the squares that the rook in the src_square can move to. """

        board = gameboard.board
        allowed_squares = []

        allowed_squares = self.get_allowed_squares_in_straight_line(src_square, "top", allowed_squares, board)
        allowed_squares = self.get_allowed_squares_in_straight_line(src_square, "bottom", allowed_squares, board)
        allowed_squares = self.get_allowed_squares_in_straight_line(src_square, "left", allowed_squares, board)
        allowed_squares = self.get_allowed_squares_in_straight_line(src_square, "right", allowed_squares, board)

        allowed_squares = self.filter_out_of_bounds_dst_squares(allowed_squares)
        allowed_squares = self.filter_squares_occupied_by_same_color_pieces(allowed_squares)

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

        (row, col) = (src_square.row + increment[partial_diagonal][0], src_square.col + increment[partial_diagonal][1])
        while row >= 0 and row <= 7 and col >= 0 and col <= 7:
            if self.is_square_occupied_by_opponent_piece(board[row][col]):
                allowed_squares.append(board[row][col])
                break
            elif self.is_square_occupied_by_own_piece(board[row][col]):
                break
            elif not board[row][col].is_occupied:
                allowed_squares.append(board[row][col])
            (row, col) = (row + increment[partial_diagonal][0], col + increment[partial_diagonal][1])

        return allowed_squares

    def get_allowed_squares_in_straight_line(self, src_square, partial_line, allowed_squares, board):
        """ Returns a list of the squares in the given partial straight line that the queen in the src_square
        can move to. """

        increment = {"top": (1, 0),
                     "bottom": (-1, 0),
                     "left": (0, -1),
                     "right": (0, 1)}

        (row, col) = (src_square.row + increment[partial_line][0], src_square.col + increment[partial_line][1])
        while row >= 0 and row <= 7 and col >= 0 and col <= 7:
            if self.is_square_occupied_by_opponent_piece(board[row][col]):
                allowed_squares.append(board[row][col])
                break
            elif self.is_square_occupied_by_own_piece(board[row][col]):
                break
            elif not board[row][col].is_occupied:
                allowed_squares.append(board[row][col])
            (row, col) = (row + increment[partial_line][0], col + increment[partial_line][1])

        return allowed_squares

    def get_valid_dst_squares(self, src_square, gameboard, dst_square=None, castling=False):
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
        allowed_squares = self.filter_squares_occupied_by_same_color_pieces(allowed_squares)

        allowed_square_codes = [square.code for square in allowed_squares]
        # print "allowed_square_codes for src_square %s: %s" % (src_square.code, allowed_square_codes)

        return allowed_square_codes


class KingMoveValidator(MoveValidator):
    def __init__(self, player, color):
        """Move validator for a king of a given color."""
        super(KingMoveValidator, self).__init__(player, color)

    def get_valid_dst_squares(self, src_square, gameboard, dst_square=None, castling=False):
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

        # if castling:
        # if not ((gameboard.move_history["check"] is True) and (self.color == gameboard.move_history[])):
        #     pass

        allowed_squares = self.add_castling_squares_to_valid_dst_squares(src_square, gameboard, allowed_squares)
        allowed_squares = self.filter_out_of_bounds_dst_squares(allowed_squares)
        allowed_squares = self.filter_squares_occupied_by_same_color_pieces(allowed_squares)

        allowed_square_codes = [square.code for square in allowed_squares]
        # print "allowed_square_codes for src_square %s: %s" % (src_square.code, allowed_square_codes)

        return allowed_square_codes

    def add_castling_squares_to_valid_dst_squares(self, src_square, gameboard, allowed_squares):
        """ If castling (either kingside and/or queenside) is possible, adds castling squares to
        allowed_squares list and returns it. """
        board = gameboard.board

        castling_squares = {WHITE: {"short": board[7][6], "long": board[7][2]},
                            BLACK: {"short": board[0][6], "long": board[0][2]}}

        king_can_castle_short = self.king_can_castle_short(src_square, gameboard)
        if king_can_castle_short:
            print "\nKING CAN CASTLE SHORT"
            gameboard.castling_square = castling_squares[self.color]["short"]
            allowed_squares.append(gameboard.castling_square)

        king_can_castle_long = self.king_can_castle_long(src_square, gameboard)
        if king_can_castle_long:
            print "\nKING CAN CASTLE LONG"
            gameboard.castling_square = castling_squares[self.color]["long"]
            allowed_squares.append(gameboard.castling_square)

        return allowed_squares

    def king_can_castle_short(self, src_square, gameboard):
        """ Returns true if king can castle. The king can castle short or long depending on the dst_square.
            Castling is only permissible if all of the following conditions hold:
            1. The king and the chosen rook are on the player's first rank.
            2. Neither the king nor the chosen rook has previously moved.
            3. There are no pieces between the king and the chosen rook.
            4. The king is not currently in check.
            5. The king does not pass through a square that is attacked by an enemy piece.
            6. The king does not end up in check. (True of any legal move.)"""
        king_can_castle_short = False
        (rook_square, knight_square, bishop_square, in_between_squares) = (None, None, None, None)

        if self.color is WHITE:
            rook_square = gameboard.board[7][7]
            knight_square = gameboard.board[7][6]
            bishop_square = gameboard.board[7][5]
        elif self.color is BLACK:
            rook_square = gameboard.board[0][7]
            knight_square = gameboard.board[0][6]
            bishop_square = gameboard.board[0][5]
        in_between_squares = [bishop_square, knight_square]

        king_can_castle_short = \
            self.king_and_rook_are_on_players_first_rank(src_square, rook_square) and\
            self.king_and_rook_have_not_previously_moved(src_square, rook_square) and\
            self.king_and_rook_are_connected(in_between_squares) and\
            self.king_is_not_currently_in_check(gameboard) and\
            not self.king_passes_through_attacked_square_or_ends_up_in_check(in_between_squares, gameboard)

        return king_can_castle_short

    def king_can_castle_long(self, src_square, gameboard):
        """ Returns true if king can castle. The king can castle short or long depending on the dst_square.
            Castling is only permissible if all of the following conditions hold:
            1. The king and the chosen rook are on the player's first rank.
            2. Neither the king nor the chosen rook has previously moved.
            3. There are no pieces between the king and the chosen rook.
            4. The king is not currently in check.
            5. The king does not pass through a square that is attacked by an enemy piece.
            6. The king does not end up in check. (True of any legal move.)"""
        print "LONG CASTLE"
        king_can_castle_long = False
        (rook_square, knight_square, bishop_square, queen_square, in_between_squares) = (None, None, None, None, None)

        if self.color is WHITE:
            rook_square = gameboard.board[7][0]
            knight_square = gameboard.board[7][1]
            bishop_square = gameboard.board[7][2]
            queen_square = gameboard.board[7][3]
        elif self.color is BLACK:
            rook_square = gameboard.board[0][0]
            knight_square = gameboard.board[0][1]
            bishop_square = gameboard.board[0][2]
            queen_square = gameboard.board[0][3]
        in_between_squares = [knight_square, bishop_square, queen_square]

        king_can_castle_long = \
            self.king_and_rook_are_on_players_first_rank(src_square, rook_square) and\
            self.king_and_rook_have_not_previously_moved(src_square, rook_square) and\
            self.king_and_rook_are_connected(in_between_squares) and\
            self.king_is_not_currently_in_check(gameboard) and\
            not self.king_passes_through_attacked_square_or_ends_up_in_check(in_between_squares, gameboard)

        return king_can_castle_long

    def king_and_rook_are_on_players_first_rank(self, king_square, rook_square):
        # Condition #1
        king_and_rook_are_on_players_first_rank = False
        if self.color is WHITE:
            king_and_rook_are_on_players_first_rank = \
                (king_square.row == 7 and king_square.is_occupied and king_square.occupying_piece.code == "wk") and\
                (rook_square.row == 7 and rook_square.is_occupied and rook_square.occupying_piece.code == "wr")
        elif self.color is BLACK:
            king_and_rook_are_on_players_first_rank =\
                (king_square.row == 0 and king_square.is_occupied and king_square.occupying_piece.code == "bk") and\
                (rook_square.row == 0 and rook_square.is_occupied and rook_square.occupying_piece.code == "br")
        # print "king_and_rook_are_on_players_first_rank: ", king_and_rook_are_on_players_first_rank
        return king_and_rook_are_on_players_first_rank

    def king_and_rook_have_not_previously_moved(self, king_square, rook_square):
        # Condition #2
        king_and_rook_have_not_previously_moved = True
        (king, rook) = (king_square.occupying_piece, rook_square.occupying_piece)
        if king.has_moved or rook.has_moved:
            king_and_rook_have_not_previously_moved = False
        # print "king_and_rook_have_not_previously_moved: ", king_and_rook_have_not_previously_moved
        return king_and_rook_have_not_previously_moved

    def king_and_rook_are_connected(self, in_between_squares):
        # Condition #3
        king_and_rook_are_connected = True
        for square in in_between_squares:
            if square.is_occupied:
                king_and_rook_are_connected = False
                break
        # print "king_and_rook_are_connected: ", king_and_rook_are_connected
        return king_and_rook_are_connected

    def king_is_not_currently_in_check(self, gameboard):
        # Condition #4
        # print "\nCURRENTLY IN CHECK?\n"
        # print "gameboard.move_history: ", gameboard.move_history

        # print "gameboard.move_history[-1]: ", gameboard.move_history[-1]
        check = gameboard.move_history[-1]["check"]

        # opponent = gameboard.get_opponent(self.player)
        # check = gameboard.check_exists(opponent, opponent.available_pieces_positions, castling=True)
        king_is_not_currently_in_check = (not check)
        # print "king_is_not_currently_in_check: ", king_is_not_currently_in_check
        return king_is_not_currently_in_check

    def king_passes_through_attacked_square_or_ends_up_in_check(self, in_between_squares, gameboard):
        # Conditions #5, #6
        opponent = gameboard.get_opponent(self.player)

        # print "\n---NEW BOARD FOR CASTLE---\n"
        # self.player.print_board(gameboard)

        # for src_square in opponent.available_pieces_positions:
        for src_square in gameboard.avl_pieces_positions[opponent.color]:
            print "src_square.code: ", src_square.code
            print "src_square.occupying_piece.code: ", src_square.occupying_piece.code
            pieceValidator = MoveValidator.get_instance(opponent, src_square.occupying_piece)
            opponent_dst_squares_codes = pieceValidator.get_valid_dst_squares(src_square, gameboard)
            opponent_dst_squares = [SquareConverter.get_square_object_from_code(
                square_code, gameboard.board) for square_code in opponent_dst_squares_codes]

            for square in in_between_squares:
                if square in opponent_dst_squares:
                    return True
        return False
