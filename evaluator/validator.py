import re
from textwrap import wrap


class Validator:
    def __init__(self):
        self.LENGTH_MAP = {
            'texas-holdem': [5, 2, 4],
            'omaha5': [5, 5, 10],
            'five-card-draw': [5, 5, 10]
        }

    def validate_hands(self, game_type, hands):
        for i in hands:
            if len(i) != self.LENGTH_MAP[game_type][2]:
                return False
        return True

    @staticmethod
    def validate_input(string):
        ret = True
        pattern = re.compile("[AKQJT2-9][hdcs]")
        res = pattern.findall(string)
        if res is None or len(res) < len(string) // 2:
            ret = False
        return ret

    @staticmethod
    def validate_unique(cards_list):
        return False if len(set(cards_list)) < len(cards_list) else True

    def validate_length(self, game_type, cards_list):
        ret = True
        if len(cards_list[:5]) % self.LENGTH_MAP[game_type][0] and len(cards_list[5:]) % self.LENGTH_MAP[game_type][1]:
            ret = False
        return ret

    def validate_game(self, board, hands):
        ret, message = True, 'OK'
        curr_game = list(wrap(board, 2) + list(wrap(''.join(hands), 2)))
        if not (self.validate_input(board + ''.join(hands))):
            ret, message = False, 'Error: Invalid cards input: non-existent value or suit'
        elif not self.validate_hands("omaha5", hands):
            ret, message = False, 'Error: Invalid hand length'
        elif not (self.validate_unique(curr_game)):
            ret, message = False, 'Error: Cards are not unique'
        elif not (self.validate_length("omaha5", curr_game)):
            ret, message = False, 'Error: Not enough cards to evaluate hands'
        return ret, message
