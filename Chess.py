# ==================================================================================
# Written by:    Spyros Kechagias
# e-mail:        spiridon_kechagias at gmail.com
#
# Started in:    5/12/2015
#
# ==================================================================================

from Game import Game
from Player import Player
from MoveValidator import MoveValidator
from HelperClasses import *


class Chess(object):

    def __init__(self):
        """Runs the program. """
        self.chess_game = None
        Chess.run(self)

    @staticmethod
    def run(self):
        """Runs the program's main loop (which entails printing the main menu, creating a chess game,
        playing and ending it. """

        Chess.print_main_menu()
        selected_option = raw_input()

        if selected_option == '1':    # new game creation

            (player1, player2) = Chess.setup_players()
            (white_player, black_player) = Chess.get_players_from_color(player1, player2)
            self.chess_game = Game(player1, player2)
            board = self.chess_game.board
            players = [white_player, black_player]
            player_in_turn = white_player

            print "Game started! Press 'S' at any time to stop the game and return to the main menu."

            while True:

                src_square = Chess.get_src_square_from_player(player_in_turn, board)
                if src_square == 'S':
                    break

                (new_move, dst_square) = Chess.get_dst_square_from_player(player_in_turn, board)

                if dst_square == 'S':
                    break

                if new_move is True:     # choose a source square again
                    continue

                move_is_valid = Chess.validate_move(player_in_turn, src_square, dst_square, board)
                if move_is_valid:
                    player_in_turn.finalize_move(src_square, dst_square, board)
                    board.update_lists()
                    (check, checkmate, stalemate) = Chess.check_for_check_checkmate_stalemate(
                        board, player_in_turn)
                    board.print_move_history()
                else:
                    print "Invalid move. Please choose again.\n"
                    continue

                player_in_turn.print_board(board)
                player_in_turn = Chess.change_turn(player_in_turn, players)

        elif selected_option == '2':    # exit program
            pass

    @staticmethod
    def print_main_menu():
        """ Prints the game's main menu to the console. """
        print "\nWelcome to Kex Chess! Please select an option:\n"
        print "(1) Create new game"
        print "(2) Exit\n"
        print "Select: "

    @staticmethod
    def setup_players():
        """ Asks the user for the players' names and colors and sets them up. Returns the two players. """
        print "Player 1 name: "
        player1_name = raw_input()
        print "Player 2 name: "
        player2_name = raw_input()
        print player1_name + ", select white (w) or black (b) pieces: ",
        player1_color = raw_input()
        player2_color = ""

        if player1_color is 'w':
            (player1_color, player2_color) = WHITE, BLACK
        elif player1_color is 'b':
            (player1_color, player2_color) = BLACK, WHITE

        player1 = Player(player1_name, player1_color)
        player2 = Player(player2_name, player2_color)
        return (player1, player2)

    @staticmethod
    def get_players_from_color(player1, player2):
        """ Given the two players, returns the 'white' and 'black' player according to the color chosen. """
        (white_player, black_player) = (None, None)
        if player1.color == WHITE:
            (white_player, black_player) = player1, player2
        elif player1.color == BLACK:
            (white_player, black_player) = player2, player1
        return (white_player, black_player)

    @staticmethod
    def check_for_check_checkmate_stalemate(board, player):
        """ Checks for check and checkmate and proceeds to the appropriate actions accordingly. """
        check = board.check_exists(player, board.avl_pieces_positions[player.color])

        checkmate = False
        stalemate = False

        if check is True:
            print "Check!"
            board.move_history[-1]["check"] = True
            checkmate = board.checkmate_exists(player)
            if checkmate is True:
                board.move_history[-1]["checkmate"] = True
                print "Checkmate!!"

        else:
            checkmate = board.checkmate_exists(player)
            if checkmate is True:
                board.move_history[-1]["stalemate"] = True
                stalemate = True
                print "Stalemate!!"

        return (check, checkmate, stalemate)

    @staticmethod
    def get_src_square_from_player(current_player, board):
        """ Asks players to move a piece from a square performing input validation. """
        print "===================================================================="
        print "%s (%s) to play." % (current_player.get_color_str().title(), current_player.name),
        print "\nAvailable %s pieces to move lie in squares: %s"\
            % (current_player.get_color_str(), current_player.get_square_codes_of_available_pieces(board))

        current_player.print_board(board)

        while True:
            print "\nChoose a square (e.g. A2) to move a piece from: "
            selected_square_code = raw_input().upper()
            if selected_square_code == 'S':
                return selected_square_code
            print "You chose square %s to move a piece from." % selected_square_code,
            selection_is_valid = current_player.src_square_selection_is_valid(selected_square_code, board)
            if selection_is_valid is True:
                from_square = Converter.get_square_object_from_code(selected_square_code, board.position)
                return from_square

    @staticmethod
    def get_dst_square_from_player(current_player, board):
        """ Asks players for destination square performing input validation.
        Returns a tuple containing two values:
        1. a boolean variable that is True when the user has chosen to select a new source square,
        2. the destination square object, if variable from (1) is False. """
        # board = board.position
        new_move = False
        while True:
            print "\n"
            print "Choose a square (e.g. A4) to move a piece to (or press 'N' to choose a new piece to move): "
            given_square_code = raw_input().upper()
            if given_square_code == 'S':
                return (False, given_square_code)
            if given_square_code != "N":
                print "You chose square %s to move a piece to." % given_square_code,

                dst_square_belongs_in_board = Chess.validate_input(given_square_code, board)
                if dst_square_belongs_in_board is False:
                    print "Invalid input! Square must belong in chess board!"
                    continue

                dst_square = Converter.get_square_object_from_code(given_square_code, board.position)
                return (new_move, dst_square)

            else:
                print "\nNew move.",
                new_move = True
                return (new_move, None)

    @staticmethod
    def change_turn(current_player, players):
        """ Changes turns according to current player. Returns new player in turn. """
        (white_player, black_player) = (players[0], players[1])
        new_player_in_turn = None
        if current_player == white_player:
            new_player_in_turn = black_player
        elif current_player == black_player:
            new_player_in_turn = white_player
        return new_player_in_turn

    @staticmethod
    def validate_move(player, src_square, dst_square, board):
        """ Validates the move defined by the 'src_square' & 'dst_square' args of the piece in the 'src_square'. """
        pieceValidator = MoveValidator.get_instance(player, src_square.occupying_piece)
        move_is_valid = pieceValidator.is_move_valid(src_square, dst_square, board)
        if move_is_valid is True:
            return True

    @staticmethod
    def validate_input(square_code, board):
        """ Checks that the square given by the user (either for the source or destination square) belongs to the board
        by checking its code. """
        if square_code not in board.square_codes:
            return False
        else:
            return True

    @staticmethod
    def main():
        """ Main program. """
        Chess()

if __name__ == "__main__":
    Chess.main()
