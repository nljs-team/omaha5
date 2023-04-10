class Player:
    def __init__(self, number: int):
        self.number = number
        self._hand = None
        self._wins = 0

    def add_hand(self, hand: str):
        self._hand = hand

    @property
    def hand(self):
        return self._hand

    @property
    def wins(self):
        return self._wins

    def wins_game(self):
        self._wins += 1

    def __str__(self):
        return "Player {} with {} wins".format(self.number, self._wins)
