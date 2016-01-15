from HelperClasses import *
from Piece import *


class Player(object):

    LETTER_NOTATION_STRING = "A   B   C   D   E   F   G   H"

    def __init__(self, name, color):
        """Creates a player in a chess game."""
        self.name = name
        self.color = color
        self.available_pieces_positions = []
        # self.lost_pieces = []
        self.captured_pieces = []

    def get_square_codes_of_available_pieces(self):
        """ Returns a list containing the square codes of the available pieces of a player. """
        square_codes = [square.code for square in self.available_pieces_positions]
        return square_codes

    def get_color_str(self):
        """ Returns a string containing the player's color. """
        colors_dict = {WHITE: 'white', BLACK: 'black'}
        return colors_dict[self.color]

    def is_valid(self, selected_square_code):
        is_valid = None
        if selected_square_code not in self.get_square_codes_of_available_pieces():
            is_valid = False
        else:
            is_valid = True
        return is_valid

    def finalize_move(self, src_square, dst_square, gameboard):
        board = gameboard.board
        src_piece = src_square.occupying_piece
        capture_dict = {'capture_made': False, 'capturing_piece': None, 'captured_piece': None}

        # update 'src_square' attributes
        board[src_square.row][src_square.col].is_occupied = False
        board[src_square.row][src_square.col].occupying_piece = None

        # update 'dst_square' attributes
        if dst_square.is_occupied:
            dst_piece = dst_square.occupying_piece
            self.captured_pieces.append(dst_piece)
            if dst_piece.color != src_piece.color:
                capture_dict['capture_made'] = True
                capture_dict['capturing_piece'] = src_piece
                capture_dict['captured_piece'] = dst_piece

        # 'en passant' case
        if gameboard.en_passant_square == dst_square:
            previous_move = gameboard.move_history[-1]
            capture_dict['capture_made'] = True
            capture_dict['capturing_piece'] = src_piece
            capture_dict['captured_piece'] = previous_move["dst_square"].occupying_piece
            previous_move["dst_square"].is_occupied = False
            previous_move["dst_square"].occupying_piece = None
            gameboard.en_passant_square = None
            dst_square.en_passant = True

        board[dst_square.row][dst_square.col].is_occupied = True
        board[dst_square.row][dst_square.col].occupying_piece = src_piece

        # pawn promotion
        self.promote_pawn(dst_square, gameboard)

        self.update_move_history(src_square, dst_square, gameboard, capture_dict)

    def promote_pawn(self, dst_square, gameboard):
        """ Promotes a pawn to a piece given by the user when asked. """
        if (dst_square.occupying_piece.code == 'wp') and (dst_square.row == 0):
            self.select_promotion_piece(dst_square, gameboard.board)

    def select_promotion_piece(self, dst_square, board):
        """ Asks player for the piece to replace the promoted pawn with. """
        while True:
            print "\nReplace pawn with:"
            print "1. Queen"
            print "2. Rook"
            print "3. Bishop"
            print "4. Knight"
            print "Your choice: "
            selection = raw_input()
            if selection in ['1', '2', '3', '4']:
                break
            else:
                print "Invalid selection. Choose again: "
                continue
        promotion_pieces = {
            '1': Queen(self.color),
            '2': Rook(self.color),
            '3': Bishop(self.color),
            '4': Knight(self.color)
        }
        board[dst_square.row][dst_square.col].occupying_piece = promotion_pieces[selection]

    def get_move_sn(self, gameboard):
        """ Gets the serial number of the player's last move. """
        # first move
        if gameboard.move_history == []:
            current_move_sn = 1
        else:
            if self.color == WHITE:
                current_move_sn = gameboard.move_history[-1]["sn"] + 1
            else:
                current_move_sn = gameboard.move_history[-1]["sn"]
        return current_move_sn

    def update_move_history(self, src_square, dst_square, gameboard, capture_dict):
        """ Updates move history with current move. """

        current_move_sn = self.get_move_sn(gameboard)

        gameboard.move_history.append({
            "sn": current_move_sn,
            "player": self,
            "src_square": src_square,
            "dst_square": dst_square,
            "en_passant": dst_square.en_passant,
            "capture": capture_dict,
            "check": False,
            "checkmate": False
        })

    def src_square_selection_is_valid(self, selected_square_code):
        """ Tests that the given square to move piece from is valid and prints a message accordingly."""
        selection_is_valid = None

        if self.is_valid(selected_square_code) is False:
            selection_is_valid = False
            print "This square is invalid."
        else:
            selection_is_valid = True

        return selection_is_valid

    def print_board(self, gameboard):
        """ Prints the board from the perspective of the player object that called the method. """

        board = gameboard.board
        used_letter_notation_string = self.get_used_letter_notation_string(Player.LETTER_NOTATION_STRING)

        self.print_line()
        self.print_horizontal_letters(used_letter_notation_string)
        for row in range(0, 8):
            self.print_board_horizontal_border()

            for col in range(0, 8):

                (row_index, col_index) = self.get_indices(row, col)

                square_color = board[row_index][col_index].color
                is_occupied = board[row_index][col_index].is_occupied
                if not board[row_index][col_index].occupying_piece:
                    occupying_piece_code = None
                else:
                    occupying_piece_code = board[row_index][col_index].occupying_piece.code

                self.print_vertical_numbers(row_index, col)
                self.print_square_content(square_color, is_occupied, occupying_piece_code)

            self.print_vertical_dividing_line_and_numbers(row_index, col)

        self.print_board_horizontal_border()
        self.print_horizontal_letters(used_letter_notation_string)
        self.print_line()

    def get_used_letter_notation_string(self, letter_notation_string):
        used_letter_notation_string = None
        if self.color == WHITE:
            used_letter_notation_string = letter_notation_string
        elif self.color == BLACK:
            used_letter_notation_string = letter_notation_string[::-1]
        return used_letter_notation_string

    def get_indices(self, row, col):
        (row_index, col_index) = (None, None)
        if self.color == WHITE:
            (row_index, col_index) = (row, col)
        elif self.color == BLACK:
            (row_index, col_index) = (7-row, 7-col)
        return (row_index, col_index)

    def print_board_horizontal_border(self):
        print "\n   |---|---|---|---|---|---|---|---| "

    def print_letter(self, letter):
        print letter

    def print_vertical_numbers(self, row_index, col):
        if col == 0:
            print Printer.BOLD + " " + str(8-row_index) + Printer.END,
        print "|",

    def print_square_content(self, square_color, is_occupied, occupying_piece_code):
        # print empty squares
        if not is_occupied:
            if square_color == BLACK:
                print Printer.BLOCK,
            else:
                print " ",
        # print occupied squares (i.e. print pieces)
        else:
            print Printer.symbols[occupying_piece_code],

    def print_horizontal_letters(self, used_letter_notation_str):
        print Printer.BOLD + "     " + used_letter_notation_str + Printer.END,

    def print_vertical_dividing_line_and_numbers(self, row_index, col):
        print "|" + Printer.BOLD + " " + str(8-row_index) + Printer.END,

    def print_line(self):
        print "\n"
