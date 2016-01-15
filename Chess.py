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

    @staticmethod
    def main():
        """Main program"""

        print "\nWelcome to Kex Chess! Please select an option:\n"
        print "(1) Create new game"
        print "(2) Exit\n"

        print "Select: "
        selected_option = raw_input()

        if selected_option == '1':
            print "Player 1 name: "
            player1_name = raw_input()
            print "Player 2 name: "
            player2_name = raw_input()
            print player1_name + ", select white (w) or black (b) pieces: ",
            player1_color = raw_input()
            player2_color = ""
            (white_player, black_player) = (None, None)

            if player1_color is 'w':
                (player1_color, player2_color) = WHITE, BLACK
            elif player1_color is 'b':
                (player1_color, player2_color) = BLACK, WHITE

            player1 = Player(player1_name, player1_color)
            player2 = Player(player2_name, player2_color)

            if player1_color == WHITE:
                (white_player, black_player) = player1, player2
            elif player1_color == BLACK:
                (white_player, black_player) = player2, player1

            chess_game = Game(player1, player2)
            gameboard = chess_game.board

            players = [white_player, black_player]
            player_in_turn = white_player

            while True:
                # player_in_turn.print_board(gameboard)
                src_square = Chess.get_src_square_from_player(player_in_turn, gameboard)
                (new_move, dst_square) = Chess.get_dst_square_from_player(
                                            player_in_turn, gameboard)

                if new_move is True:     # choose a source square again
                    continue

                move_is_valid = Chess.validate_move(player_in_turn, src_square, dst_square, gameboard)
                if move_is_valid:
                    player_in_turn.finalize_move(src_square, dst_square, gameboard)
                    gameboard.update_lists(white_player, black_player)

                    check = gameboard.check_exists(player_in_turn, player_in_turn.available_pieces_positions)
                    if check is True:
                        print "Check!"
                        gameboard.move_history[-1]["check"] = True
                        checkmate = gameboard.checkmate_exists(
                            player_in_turn, player_in_turn.available_pieces_positions)
                        if checkmate is True:
                            gameboard.move_history[-1]["checkmate"] = True
                            print "Checkmate!!"

                    gameboard.print_move_history()
                else:
                    print "Invalid move. Please choose again.\n"
                    continue

                player_in_turn.print_board(gameboard)
                player_in_turn = Chess.change_turn(player_in_turn, players)

                # wait = input("Press enter to continue...")

    @staticmethod
    def get_src_square_from_player(current_player, gameboard):
        """ Asks players to move a piece from a square performing input validation. """
        print "===================================================================="
        print "%s (%s) to play." % (current_player.get_color_str().title(), current_player.name),
        print "\nAvailable %s pieces to move lie in squares: %s"\
            % (current_player.get_color_str(), current_player.get_square_codes_of_available_pieces())

        current_player.print_board(gameboard)

        while True:
            print "\nChoose a square (e.g. A2) to move a piece from: "
            selected_square_code = raw_input().upper()
            print "You chose square %s to move a piece from." % selected_square_code,
            selection_is_valid = current_player.src_square_selection_is_valid(selected_square_code)
            if selection_is_valid is True:
                from_square = SquareConverter.get_square_object_from_code(selected_square_code, gameboard.board)
                return from_square

    @staticmethod
    def get_dst_square_from_player(current_player, gameboard):
        """ Asks players for destination square performing input validation.
        Returns a tuple containing two values:
        1. a boolean variable that is True when the user has chosen to select a new source square,
        2. the destination square object, if variable from (1) is False. """
        board = gameboard.board
        new_move = False
        while True:
            print "\n"
            print "Choose a square (e.g. A4) to move a piece to (or press 'N' to choose a new piece to move): "
            given_square_code = raw_input().upper()
            if given_square_code != "N":
                print "You chose square %s to move a piece to." % given_square_code,

                dst_square_belongs_in_board = Chess.validate_input(given_square_code, gameboard)
                if dst_square_belongs_in_board is False:
                    print "Invalid input! Square must belong in chess board!"
                    continue

                dst_square = SquareConverter.get_square_object_from_code(given_square_code, board)
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
    def validate_move(player, src_square, dst_square, gameboard):
        """ Validates the move defined by the 'src_square' & 'dst_square' args of the piece in the 'src_square'. """
        pieceValidator = MoveValidator.get_instance(player, src_square.occupying_piece)
        move_is_valid = pieceValidator.is_move_valid(src_square, dst_square, gameboard)
        if move_is_valid is True:
            return True

    @staticmethod
    def validate_input(square_code, gameboard):
        """ Checks that the square given by the user (either for the source or destination square) belongs to the board
        by checking its code. """
        if square_code not in gameboard.square_codes:
            return False
        else:
            return True


if __name__ == "__main__":
    Chess.main()
