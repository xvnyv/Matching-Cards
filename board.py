from random import choice, sample


class Board:
    def __init__(self):
        # initial icon bank that looks so much nicer:
        # ['☆', '☂', '♘', '♰', '¿', '?', 'Δ', '⚐', '♔', '⇒', '⇐', '∞', '♤', '♧', '♡', '♢', '☀', '☁']
        # fmt: off
        self.icon_bank = ['?', '¿', 'Δ', 'Ψ', '#', '$', '€', '†', '^', '∞', '£', '<', '>', '§', 'µ', '=', '₩', '&']
        self.size = 0

        self.cards = None
        self.cards_icons = None
        self.opened_icons = []
        self.matched = False

    def __str__(self):
        if self.cards:
            # only allows board to be printed as a string after icons have been randomly placed

            A_char_code = ord("A")
            # column coordinates at the top
            board = (
                "\n{:>8s}".format("")
                + "".join(["{:>8s}".format(str(i)) for i in range(1, self.size + 1)])
                + "\n\n"
            )

            for i, row in enumerate(self.cards):
                row = self.cards[i]
                # row coordinates on the right
                board += "{:>8s}".format(chr(A_char_code + i))
                # cards
                for card in row:
                    board += "{:>8s}".format(card)
                board += "\n\n"
        else:
            # informs user that the board is not yet functional and that they must first call arrange_cards()
            board = "The board has not been set up yet. Call the arrange_cards() method to set up the board."

        return board

    def arrange_cards(self):
        """Called at the beginning of a new game to randomise the placement of each icon."""

        # pick icons to use based on the specified size of the board
        # did not use sample for both sizes as size = 6 requries all available icons
        if self.size == 4:
            icons = sample(self.icon_bank, self.size**2 // 2)
        else:
            icons = self.icon_bank

        # create 2D array for cards based on the specified size of the board
        self.cards = [["x"] * self.size for i in range(self.size)]
        self.cards_icons = []

        # create a dictionary to keep track of how many times
        # each icon has been placed into the card deck
        icons_in_cards = {}
        for icon in icons:
            icons_in_cards[icon] = 0

        for row in range(self.size):
            self.cards_icons.append([])
            for col in range(self.size):
                chosen_icon = choice(list(icons_in_cards.keys()))
                self.cards_icons[row].append(chosen_icon)
                # updating the number of times an icon has been placed into the cards
                # and removing the icon once it has been placed twice
                icons_in_cards[chosen_icon] += 1
                if icons_in_cards[chosen_icon] == 2:
                    del icons_in_cards[chosen_icon]

    def open_card(self, row, col):
        """Reveals the icon located at the specified row and col."""

        self.cards[row][col] = self.cards_icons[row][col]
        self.opened_icons.append(self.cards_icons[row][col])

    def end_turn(self):
        """Hides all opened icons by turning them into 'x'. If a match occurred, leaves blanks where the matched icons were previously located at."""

        for row in range(self.size):
            for col in range(self.size):
                # if unmatched, flip cards back to show 'x' instead of icon
                # if matched, remove cards
                if self.cards[row][col] != "x" and self.cards[row][col] != "":
                    self.cards[row][col] = "x" if not self.matched else ""
        # reset opened icons to nothing at the end of each turn
        self.opened_icons = []

    def check_card_unmatched(self, row, col):
        """Checks whether the player's card choice had already been matched."""

        return self.cards[row][col] != ""

    def check_card_exists(self, row, col):
        """Checks whether the player's card choice is within the range of valid coordinates."""

        return row + 1 <= self.size and col + 1 <= self.size

    def check_card_closed(self, row, col):
        """Checks whether the player is trying to open the same card twice in a round."""

        return self.cards[row][col] == "x"

    def convert_coord_to_index(self, coord):
        """Converts the coordinate input from the user into row and col indices to be used in the program."""

        row = ord(coord[0]) - ord("A")
        col = int(coord[1]) - 1

        return row, col

    def check_match(self):
        """Checks for a match at the end of each turn."""

        return self.opened_icons[0] == self.opened_icons[1]

    def check_win(self):
        """Checks whether all cards have been matched."""

        return self.cards == [[""] * self.size for i in range(self.size)]
