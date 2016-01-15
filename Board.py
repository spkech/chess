from Square import Square
from HelperClasses import *
from Piece import Piece
from MoveValidator import MoveValidator
import copy


class Board(object):

    def __init__(self, players):
        """Creates a chess board."""
        self.board = [[None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None]]

        self.square_codes = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8',
                             'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8',
                             'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8',
                             'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8',
                             'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8',
                             'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8',
                             'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8',
                             'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8']

        self.players = players
        self.move_history = []
        self.en_passant_square = None    # the destination square in an 'en passant' move
        self.check = False
        self.checkmate = False
        self._setup()

    def get_opponent(self, player):
        """ Returns the opponent of the player given as argument. """
        for selected_player in self.players:
            if player != selected_player:
                return selected_player

    def assign_players_to_board(self):
        """Assigns players given as arguments to current board."""
        (white_player, black_player) = self._get_player_colors(self.players[0], self.players[1])
        self.update_lists(white_player, black_player)

    def checkmate_exists(self, player, avl_src_pieces_squares):
        """ For every piece of 'player', checks if there exists a move that results in the king not
        being threatened. Returns True for checkmate, false otherwise. """

        # print "\nIN MATE CHECKING:"
        opponent = self.get_opponent(player)
        opponent_src_squares = opponent.available_pieces_positions
        # print "opponent color: ", opponent.get_color_str()
        # print "opponent's pieces: ", opponent.get_square_codes_of_available_pieces()

        for opponent_src_square in opponent_src_squares:
            opponent_src_piece = opponent_src_square.occupying_piece
            # print "opponent_src_piece: %s in %s" % (str(opponent_src_piece), opponent_src_square.code)
            pieceValidator = MoveValidator.get_instance(player, opponent_src_piece)
            opponent_dst_squares_codes = pieceValidator.get_valid_dst_squares(opponent_src_square, self)
            # print "dst_squares_codes for %s in %s: %s\n" % (
            #     str(opponent_src_piece), opponent_src_square.code, opponent_dst_squares_codes)

            opponent_dst_squares = [SquareConverter.get_square_object_from_code(
                square_code, self.board) for square_code in opponent_dst_squares_codes]

            for opponent_dst_square in opponent_dst_squares:
                new_gameboard = copy.deepcopy(self)   # deep (recursive) copy

                # update squares attributes
                new_gameboard.board[opponent_dst_square.row][opponent_dst_square.col].is_occupied = True
                new_gameboard.board[opponent_dst_square.row][opponent_dst_square.col].occupying_piece = \
                    self.board[opponent_src_square.row][opponent_src_square.col].occupying_piece
                new_gameboard.board[opponent_src_square.row][opponent_src_square.col].is_occupied = False
                new_gameboard.board[opponent_src_square.row][opponent_src_square.col].occupying_piece = None

                # print "\nNEW BOARD:"
                # opponent.print_board(new_gameboard)

                avl_pieces = player.available_pieces_positions
                if opponent_dst_square in player.available_pieces_positions:
                    # print "IT IS!, dst square: ", opponent_dst_square.code
                    avl_pieces.remove(opponent_dst_square)  # remove piece in case of capture

                check = new_gameboard.check_exists(player, avl_pieces)
                # print "\nIN MATE CHECKING, check after move of %s (%s->%s) is: %s " % (
                #     str(opponent_src_piece), opponent_src_square.code, opponent_dst_square.code, check)
                # if check is True:
                    # print "IN MATE CHECKING: Your king is being checked!"
                if check is False:
                    # print "IN MATE CHECKING: Mate has been avoided! Check is false!"
                    # print "CHECKMATE DOES NOT EXIST"
                    return False
        return True

    def check_exists(self, player, avl_src_pieces_squares):
        """ Traverses all available pieces given as argument and checks if any of them checks the opponent king.
        This method is called at the end of each move. """
        self.check = False
        dst_squares = []

        # print "\n\nIN CHECK EXISTS:"

        avl_src_pieces_squares_codes = [square.code for square in avl_src_pieces_squares]
        # print "avl_src_pieces_squares in CHECK: ", avl_src_pieces_squares_codes

        for src_square in avl_src_pieces_squares:
            pieceValidator = MoveValidator.get_instance(player, src_square.occupying_piece)
            dst_squares_codes = pieceValidator.get_valid_dst_squares(src_square, self)
            for dst_square_code in dst_squares_codes:
                dst_square = SquareConverter.get_square_object_from_code(dst_square_code, self.board)
                dst_squares.append(dst_square)

            # print "dst_squares for piece in %s: %s" % (src_square.code, dst_squares_codes)

            for dst_square in dst_squares:

                if dst_square.is_occupied and dst_square.occupying_piece.code[1] == 'k':   # king
                    self.check = True
                    print "Check!"
                    return True
        return False

    def _setup(self):
        """Sets up the board for the first time."""
        for row in range(0, 8):
            for col in range(0, 8):
                current_square_color = SquareConverter.get_square_color(row, col)
                current_square_code = SquareConverter.get_square_code_from_dimensions(row, col)
                is_current_square_occupied = SquareConverter.is_square_occupied_at_board_setup(row, col)

                code_of_occupying_piece = SquareConverter.get_code_of_occupying_piece_at_board_setup(row, col)
                color_of_occupying_piece = SquareConverter.get_color_of_occupying_piece_at_board_setup(row, col)
                occupying_piece = Piece.get_instance(code_of_occupying_piece, color_of_occupying_piece)

                self.board[row][col] = Square(
                    current_square_color, current_square_code, is_current_square_occupied, occupying_piece, row, col)

    def _get_player_colors(self, player1, player2):
        (white_player, black_player) = (None, None)
        if player1.color == WHITE:
            white_player = player1
            black_player = player2
        elif player1.color == BLACK:
            white_player = player2
            black_player = player1
        return (white_player, black_player)

    def print_move_history(self, player=None):
        """ Prints board's move history. If a player is given as argument, prints only this player's move history. """
        # print all (both players') move history
        moves = self.move_history
        en_passant_str = None

        if not player:
            print "\n=========================== Move History ==============================="
            for move in moves:
                symbol = '-'
                capture_str = ''
                check_str = ''

                if move["player"].color == WHITE:
                    sn_str = str(move['sn'])
                else:
                    sn_str = str(move['sn']) + "..."

                if move['en_passant'] == True:
                    en_passant_str = " en passant"
                    symbol = 'x'
                else:
                    en_passant_str = ""

                if move['capture']['capture_made'] is True:
                    symbol = 'x'
                    capturing_piece = move['capture']['capturing_piece']
                    captured_piece = move['capture']['captured_piece']
                    capture_str = " " + str(capturing_piece) + " takes " + str(captured_piece)

                if move["check"] is True:
                    check_str = "[ Check! ]"
                if move["checkmate"] is True:
                    check_str = "[ Checkmate!! ]"

                color_str = move['player'].get_color_str().title()
                name = move['player'].name
                src = move['src_square'].code
                dst = move['dst_square'].code
                print " %s\t %s (%s):\t%s%s%s\t%s%s%s" \
                    % (sn_str, color_str, name, src, symbol, dst, capture_str, en_passant_str, check_str)
            print "========================================================================"

    def update_lists(self, white_player, black_player):
        """Traverses the board and updates the following lists for both players according to the pieces' positions:
           1. 'available_pieces_positions':  the list containing all squares occupied by pieces of the player
        """
        white_pieces_list = []
        black_pieces_list = []

        for row in range(0, 8):
            for col in range(0, 8):
                square = self.board[row][col]
                if square.is_occupied:
                    if square.occupying_piece.color == WHITE:
                        white_pieces_list.append(square)

                    elif square.occupying_piece.color == BLACK:
                        black_pieces_list.append(square)

        white_player.available_pieces_positions = white_pieces_list
        black_player.available_pieces_positions = black_pieces_list
