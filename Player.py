from HelperClasses import *
from Piece import *


class Player(object):

    LETTER_NOTATION_STRING = "A   B   C   D   E   F   G   H"

    def __init__(self, name, color):
        """Creates a player in a chess game."""
        self.name = name
        self.color = color
        self.captured_pieces = []

    def get_square_codes_of_available_pieces(self, board):
        """ Returns a list containing the square codes of the available pieces of a player. """
        square_codes = [square.code for square in board.avl_pieces_positions[self.color]]
        return square_codes

    def get_color_str(self):
        """ Returns a string containing the player's color. """
        colors_dict = {WHITE: 'white', BLACK: 'black'}
        return colors_dict[self.color]

    def is_valid(self, selected_square_code, board):
        is_valid = None
        if selected_square_code not in self.get_square_codes_of_available_pieces(board):
            is_valid = False
        else:
            is_valid = True
        return is_valid

    def finalize_move(self, src_square, dst_square, board):
        pos = board.position
        src_piece = src_square.occupying_piece
        capture_dict = {'capture_made': False, 'capturing_piece': None, 'captured_piece': None}
        draw_move_counter = 1

        # update 'src_square' attributes
        pos[src_square.row][src_square.col].is_occupied = False
        pos[src_square.row][src_square.col].occupying_piece = None

        # update 'dst_square' attributes
        if dst_square.is_occupied:
            dst_piece = dst_square.occupying_piece
            self.captured_pieces.append(dst_piece)
            if dst_piece.color != src_piece.color:
                capture_dict['capture_made'] = True
                capture_dict['capturing_piece'] = src_piece
                capture_dict['captured_piece'] = dst_piece

        # 'en passant' case
        if board.en_passant_square == dst_square:
            previous_move = board.move_history[-1]
            capture_dict['capture_made'] = True
            capture_dict['capturing_piece'] = src_piece
            capture_dict['captured_piece'] = previous_move["dst_square"].occupying_piece
            previous_move["dst_square"].is_occupied = False
            previous_move["dst_square"].occupying_piece = None
            board.en_passant_square = None
            dst_square.en_passant = True

        # castling case
        castling_square = self.finalize_castling(dst_square, board)

        pos[dst_square.row][dst_square.col].is_occupied = True
        pos[dst_square.row][dst_square.col].occupying_piece = src_piece

        # pawn promotion case
        self.promote_pawn(dst_square, board)

        # mark king or rook as moved (used for castling)
        if (src_piece.code[1] == 'r') or (src_piece.code[1] == 'k'):
            src_piece.has_moved = True

        # keep count of consecutive draw moves
        if board.move_history != []:
            previous_move = board.move_history[-1]
            # if pawn was moved or capture was made in current move, reset draw counter to 1
            pawn_was_moved = src_piece.code[1] == 'p'
            capture_was_made = capture_dict['capture_made']
            if pawn_was_moved or capture_was_made:
                draw_move_counter = 1
            else:
                draw_move_counter = previous_move["draw_move_counter"] + 1

        self.update_move_history(src_square, dst_square, board, capture_dict, castling_square, draw_move_counter)

    def finalize_castling(self, dst_square, board):
        """ Move king and rook according to the type of castling selected (short or long). """
        pos = board.position
        castling_square = None

        if dst_square == board.castling_square:
            if self.color == WHITE:
                # castle short
                if dst_square.code == 'G1':
                    (e1, f1, g1, h1) = (pos[7][4], pos[7][5], pos[7][6], pos[7][7])
                    (g1.is_occupied, g1.occupying_piece) = (True, e1.occupying_piece)
                    (f1.is_occupied, f1.occupying_piece) = (True, h1.occupying_piece)
                    (e1.is_occupied, e1.occupying_piece) = (False, None)
                    (h1.is_occupied, h1.occupying_piece) = (False, None)
                # castle long
                elif dst_square.code == 'C1':
                    (a1, b1, c1, d1, e1) = (pos[7][0], pos[7][1], pos[7][2], pos[7][3], pos[7][4])
                    (c1.is_occupied, c1.occupying_piece) = (True, e1.occupying_piece)
                    (d1.is_occupied, d1.occupying_piece) = (True, a1.occupying_piece)
                    (a1.is_occupied, a1.occupying_piece) = (False, None)
                    (b1.is_occupied, b1.occupying_piece) = (False, None)
                    (e1.is_occupied, e1.occupying_piece) = (False, None)
            elif self.color == BLACK:
                # castle short
                if dst_square.code == 'G8':
                    (e8, f8, g8, h8) = (pos[0][4], pos[0][5], pos[0][6], pos[0][7])
                    (g8.is_occupied, g8.occupying_piece) = (True, e8.occupying_piece)
                    (f8.is_occupied, f8.occupying_piece) = (True, h8.occupying_piece)
                    (e8.is_occupied, e8.occupying_piece) = (False, None)
                    (h8.is_occupied, h8.occupying_piece) = (False, None)
                # castle long
                elif dst_square.code == 'C8':
                    (a8, b8, c8, d8, e8) = (pos[0][0], pos[0][1], pos[0][2], pos[0][3], pos[0][4])
                    (c8.is_occupied, c8.occupying_piece) = (True, e8.occupying_piece)
                    (d8.is_occupied, d8.occupying_piece) = (True, a8.occupying_piece)
                    (a8.is_occupied, a8.occupying_piece) = (False, None)
                    (b8.is_occupied, b8.occupying_piece) = (False, None)
                    (e8.is_occupied, e8.occupying_piece) = (False, None)
            castling_square = dst_square

        board.castling_square = None
        return castling_square

    def promote_pawn(self, dst_square, board):
        """ Promotes a pawn to a piece given by the user when asked. """
        if (dst_square.occupying_piece.code == 'wp') and (dst_square.row == 0):
            self.select_promotion_piece(dst_square, board.position)

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

    def get_move_sn(self, board):
        """ Gets the serial number of the player's last move. """
        # first move
        if board.move_history == []:
            current_move_sn = 1
        else:
            sn_dict = {WHITE: board.move_history[-1]["sn"] + 1, BLACK: board.move_history[-1]["sn"]}
            current_move_sn = sn_dict[self.color]
        return current_move_sn

    def update_move_history(self, src_square, dst_square, board, capture_dict, castling_square, draw_move_counter):
        """ Updates move history with current move. """

        current_move_sn = self.get_move_sn(board)

        board.move_history.append({
            "sn": current_move_sn,
            "player": self,
            "src_square": src_square,
            "dst_square": dst_square,
            "en_passant": dst_square.en_passant,
            "capture": capture_dict,
            "castling_square": castling_square,
            "check": False,
            "checkmate": False,
            "stalemate": False,
            "draw_move_counter": draw_move_counter
        })

    def src_square_selection_is_valid(self, selected_square_code, board):
        """ Tests that the given square to move piece from is valid and prints a message accordingly."""
        selection_is_valid = None

        if self.is_valid(selected_square_code, board) is False:
            selection_is_valid = False
            print "This square is invalid."
        else:
            selection_is_valid = True

        return selection_is_valid

    def print_board(self, board):
        """ Prints the board from the perspective of the player object that called the method. """

        board = board.position
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
        notation_string_dict = {WHITE: letter_notation_string, BLACK: letter_notation_string[::-1]}
        used_letter_notation_string = notation_string_dict[self.color]
        return used_letter_notation_string

    def get_indices(self, row, col):
        indices_dict = {WHITE: (row, col), BLACK: (7-row, 7-col)}
        return indices_dict[self.color]

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
