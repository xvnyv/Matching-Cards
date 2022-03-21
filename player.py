class Player:
    def __init__(self, color):
        self.COLOR_2_CODE = {
            "Green": "\033[1;32;40m",
            "Yellow": "\033[1;33;40m",
            "Blue": "\033[1;34;40m",
            "Purple": "\033[1;35;40m",
            "Cyan": "\033[1;36;40m",
        }
        self.score = 0
        self.color = self.COLOR_2_CODE[color]

    def select_card(self):
        return input("Select a card (eg. A1): ")
