import os
from libdw import sm

from player import Player
from board import Board


class MemoryGame(sm.SM):
    # States:
    # 1) new_game, 2) flip_card_1, 3) flip_card_2, 4) get_next_player, 5) game_over

    def __init__(self):
        self.board = Board()
        # output is colored based on which player's turn it is at the moment
        # coloring is done using ANSI escape code \033[
        # valid colors include Green, Yellow, Blue, Purple and Cyan
        self.p1 = Player(color="Green")
        self.p2 = Player(color="Yellow")
        self.cur_player = self.p1

        self.error_output_color = "\033[1;31;40m"
        self.neutral_output_color = "\033[1;37;40m"

        self.start_state = "new_game"

    def get_next_values(self, state, inp):
        next_state = state

        if state == "new_game":
            # checking if board size is valid -- limited options due to limited number of icons
            # 4: easy, 6: hard
            if inp.isdigit() and (inp == "4" or inp == "6"):
                # valid size
                self.board.size = int(inp)
                self.board.arrange_cards()
                next_state = "flip_card_1"
                output = (
                    f"\n{self.p1.color}Player 1's turn" + str(self.board) + "Card 1"
                )
            else:
                # invalid size
                output = f"{self.error_output_color}Error: invalid board size {self.cur_player.color}"
            return next_state, output

        elif state == "flip_card_1" or state == "flip_card_2":
            # error handling of user input
            card_coord = inp

            # validating input format of card coordinate:
            # ensure inp has length 2, char 1 is an alphabet, char 2 is a digit
            if (
                len(card_coord) != 2
                or not card_coord[0].isalpha()
                or not card_coord[1].isdigit()
            ):
                output = f"{self.error_output_color}Error: the input format is incorrect {self.cur_player.color}"
            else:
                row, col = self.board.convert_coord_to_index(card_coord)

                # checking whether coordinate is within range
                coord_exists = self.board.check_card_exists(row, col)
                if not coord_exists:
                    output = f"{self.error_output_color}Error: the card coordinate is not valid {self.cur_player.color}"
                else:
                    # checking whether coordinate maps to a card that has already been matched
                    # only if we already checked that the coordinate is within range
                    coord_unmatched = self.board.check_card_unmatched(row, col)
                    if not coord_unmatched:
                        output = f"{self.error_output_color}Error: the card has already been matched {self.cur_player.color}"
                    else:
                        # valid card coordinate for flip_card_1
                        if self.state == "flip_card_1":
                            self.board.open_card(row, col)
                            output = str(self.board) + "Card 2"
                            next_state = "flip_card_2"
                        else:
                            # checking whether card was already opened as the first card of the turn
                            coord_closed = self.board.check_card_closed(row, col)
                            if not coord_closed:
                                output = f"{self.error_output_color}Error: the card was just opened {self.cur_player.color}"
                            else:
                                # valid card coordinate for flip_card_2
                                self.board.open_card(row, col)
                                output = str(self.board)

                                # check for a match
                                self.board.matched = self.board.check_match()
                                if self.board.matched:
                                    self.cur_player.score += 1
                                    output += f"Congratulations! You got a match!\nScore: {self.cur_player.score}"
                                else:
                                    output += f"Sorry, it was not a match\nScore: {self.cur_player.score}"

                                self.board.end_turn()

                                # check if all cards have been matched
                                if self.board.check_win():
                                    # game ended
                                    if self.p1.score > self.p2.score:
                                        winner = self.p1
                                    elif self.p2.score > self.p1.score:
                                        winner = self.p2
                                    else:
                                        winner = None

                                    # there is a winner
                                    if winner:
                                        output += f"\n\n{winner.color}Player {1 if winner == self.p1 else 2} wins!"
                                    # the game is tied
                                    else:
                                        output += f"\n\n{self.neutral_output_color}It's a tie! Guess you're both winners!"

                                    output += (
                                        f"\n\n{self.neutral_output_color}Final Scores:\n"
                                        f"{self.p1.color}Player 1: {self.p1.score}\n"
                                        f"{self.p2.color}Player 2: {self.p2.score}"
                                    )

                                    next_state = "game_over"
                                else:
                                    # game not ended
                                    next_state = "get_next_player"

            return next_state, output

        elif state == "get_next_player":
            # getting a match allows a player to pick another 2 cards
            # checking if current player got a match
            if not self.board.matched:
                # switch players if no match
                self.cur_player = self.p2 if self.cur_player == self.p1 else self.p1

            next_state = "flip_card_1"
            output = (
                f"\n{self.cur_player.color}Player {1 if self.cur_player == self.p1 else 2}'s turn\n"
                + str(self.board)
                + "Card 1"
            )

            return next_state, output

        elif state == "game_over":
            inp = inp.upper()
            if inp != "Y" and inp != "N":
                # error
                output = f"{self.error_output_color}Error: invalid input {self.cur_player.color}"
            elif inp == "Y":
                # restart game
                output = "Restarting game..."
                self.p1.score = 0
                self.p2.score = 0
                self.cur_player = self.p1
                next_state = "new_game"
            else:
                # end game
                output = "Ending game..."

            return next_state, output

    def run(self):
        self.start()
        inp = ""

        while self.state != "game_over" or inp != "N":
            # only ends when inp is Y when state is game_over
            if self.state == "new_game":
                inp = input(f"{self.neutral_output_color}Enter board size (4 or 6): ")
            elif self.state == "get_next_player":
                inp = input("Press enter to continue: ")
            elif self.state == "game_over":
                inp = input(f"\n{self.neutral_output_color}Restart game? (Y/N) ")
            else:
                inp = self.cur_player.select_card()
            output = self.step(inp)
            print(output)


try:
    os.system(
        ""
    )  # kind of a hack to get Windows cmd.exe to enable virtual terminal for Python
    # so that Windows can recognise ANSI escape code for colored text to show
    game = MemoryGame()
    game.run()
except KeyboardInterrupt:
    print("\n\033[1;37;40mEnding game...")
