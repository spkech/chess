from Square import Square
from HelperClasses import *
from Piece import Piece
from MoveValidator import MoveValidator
import copy


class Board(object):

    def __init__(self, players):
        """Creates a chess board."""
        self.position = [[None, None, None, None, None, None, None, None],
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
        self.avl_pieces_positions = {WHITE: [], BLACK: []}
        self.move_history = []
        self.en_passant_square = None    # the destination square in an 'en passant' move
        self.castling_square = None      # the destination square in a castling move
        self.check = False
        self.checkmate = False
        self.stalemate = False
        self.setup()

    def get_opponent(self, player):
        """ Returns the opponent of the player given as argument. """
        for selected_player in self.players:
            if player != selected_player:
                return selected_player

    def checkmate_exists(self, player):
        """ For every piece of 'player', checks if there exists an opponent's move that results in their king not
        being threatened. Returns True for checkmate, false otherwise. """

        print "\nIN MATE CHECKING:"
        opponent = self.get_opponent(player)
        opponent_src_squares = self.avl_pieces_positions[opponent.color]

        print "opponent color: ", opponent.get_color_str()
        print "opponent's pieces: ", opponent.get_square_codes_of_available_pieces(self)

        for opponent_src_square in opponent_src_squares:
            print "opponent_src_square:: ", opponent_src_square.code
            opponent_src_piece = opponent_src_square.occupying_piece
            print "opponent_src_piece: %s in %s" % (str(opponent_src_piece), opponent_src_square.code)
            pieceValidator = MoveValidator.get_instance(player, opponent_src_piece)
            opponent_dst_squares = pieceValidator.get_pseudolegal_dst_squares(opponent_src_square, self)

            # check if a move results to 'check', for every possible dst square of an opponent's piece
            for opponent_dst_square in opponent_dst_squares:

                opponent_dst_squares_codes = [square.code for square in opponent_dst_squares]
                print "opponent_dst_squares:: ", opponent_dst_squares_codes
                print "DST SQUARE: ", opponent_dst_square.code

                new_board = copy.deepcopy(self)   # deep (recursive) copy

                # update squares attributes
                new_board.position[opponent_dst_square.row][opponent_dst_square.col].is_occupied = True
                new_board.position[opponent_dst_square.row][opponent_dst_square.col].occupying_piece = \
                    self.position[opponent_src_square.row][opponent_src_square.col].occupying_piece
                new_board.position[opponent_src_square.row][opponent_src_square.col].is_occupied = False
                new_board.position[opponent_src_square.row][opponent_src_square.col].occupying_piece = None

                print "\nNEW BOARD:"
                opponent.print_board(new_board)

                new_board.update_lists()

                avl_pieces = copy.deepcopy(new_board.avl_pieces_positions[player.color])

                # avl_pieces_squares_codes = [square.code for square in avl_pieces]
                # print "avl_pieces in CHECKMATE1: ", avl_pieces_squares_codes

                # if opponent_dst_square.code in avl_pieces_squares_codes:
                #     print "IT IS!, dst square: ", opponent_dst_square.code

                #     avl_pieces = [square for square in avl_pieces if square.code != opponent_dst_square.code]
                #     avl_pieces.remove(opponent_dst_square)  # remove piece in case of capture

                avl_pieces_squares_codes = [square.code for square in avl_pieces]
                print "avl_pieces in CHECKMATE2: ", avl_pieces_squares_codes
                print "player color: ", player.color

                check = new_board.check_exists(player, avl_pieces)
                print "AROUMPA: check: ", check
                print "\nIN MATE CHECKING, check after move of %s (%s->%s) is: %s " % (
                    str(opponent_src_piece), opponent_src_square.code, opponent_dst_square.code, check)
                if check is True:
                    print "IN MATE CHECKING: Your king is being checked!"
                if check is False:
                    print "IN MATE CHECKING: Mate has been avoided! Check is false!"
                    return False
        return True

    def check_exists(self, player, avl_src_pieces_squares, castling=False):
        """ Traverses all available pieces given as argument and checks if any of them checks the opponent king.
        This method is called at the end of each move. """
        self.check = False
        dst_squares = []

        for src_square in avl_src_pieces_squares:
            pieceValidator = MoveValidator.get_instance(player, src_square.occupying_piece)
            dst_squares = pieceValidator.get_pseudolegal_dst_squares(src_square, self, castling=castling)

            for dst_square in dst_squares:
                if dst_square.is_occupied and dst_square.occupying_piece.code[1] == 'k':   # king
                    self.check = True
                    return True
        return False

    def init_empty(self):
        for row in range(0, 8):
            for col in range(0, 8):
                current_square_color = Converter.get_square_color(row, col)
                current_square_code = Converter.get_square_code_from_dimensions(row, col)
                self.position[row][col] = Square(current_square_color, current_square_code, False, None, row, col)

    def put_piece_on_square(self, piece, square_code):
        (row, col) = Converter.get_square_dimensions_from_code(square_code)
        self.position[row][col].is_occupied = True
        self.position[row][col].occupying_piece = piece

    def setup(self):
        """Sets up the board for the first time."""
        for row in range(0, 8):
            for col in range(0, 8):
                current_square_color = Converter.get_square_color(row, col)
                current_square_code = Converter.get_square_code_from_dimensions(row, col)
                is_current_square_occupied = Converter.is_square_occupied_at_board_setup(row, col)

                code_of_occupying_piece = Converter.get_code_of_occupying_piece_at_board_setup(row, col)
                color_of_occupying_piece = Converter.get_color_of_occupying_piece_at_board_setup(row, col)
                occupying_piece = Piece.get_instance(code_of_occupying_piece, color_of_occupying_piece)

                self.position[row][col] = Square(
                    current_square_color, current_square_code, is_current_square_occupied, occupying_piece, row, col)

    def _get_player_colors(self, player1, player2):
        """ Returns the tuple (<white_player>, <black_player>). """
        player_color_dict = {WHITE: (player1, player2), BLACK: (player2, player1)}
        return player_color_dict[player1.color]

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
                castling_str = ''

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
                    capture_str = str(capturing_piece) + " takes " + str(captured_piece)

                if move["check"] is True:
                    check_str = "\t[ Check! ]"
                if move["checkmate"] is True:
                    check_str = "\t[ Checkmate!! ]"
                if move["stalemate"] is True:
                    check_str = "\t[ Stalemate!! ]"

                if move["castling_square"] is not None:
                    if move["castling_square"].code[0] == 'G':
                        castling_str = "castles short"
                    elif move["castling_square"].code[0] == 'C':
                        castling_str = "castles long"

                color_str = move['player'].get_color_str().title()
                name = move['player'].name
                src = move['src_square'].code
                dst = move['dst_square'].code
                print " %s\t %s (%s):\t%s%s%s\t%s%s%s%s" \
                    % (sn_str, color_str, name, src, symbol, dst, capture_str, en_passant_str, check_str, castling_str)

            print "========================================================================"

    def update_lists(self):
        """Traverses the board and updates the following lists for both players according to the pieces' positions:
           1. 'available_pieces_positions':  the list containing all squares occupied by pieces of the player
        """
        white_pieces_list = []
        black_pieces_list = []

        for row in range(0, 8):
            for col in range(0, 8):
                square = self.position[row][col]
                if square.is_occupied:
                    if square.occupying_piece.color == WHITE:
                        white_pieces_list.append(square)

                    elif square.occupying_piece.color == BLACK:
                        black_pieces_list.append(square)

        self.avl_pieces_positions[WHITE] = white_pieces_list
        self.avl_pieces_positions[BLACK] = black_pieces_list
