from evaluator.hashtable_omaha import NO_FLUSH_OMAHA, FLUSH_OMAHA
from evaluator.hashtable import FLUSH
from evaluator.hash import hash_binary, hash_quinary


class Evaluator:
    def __init__(self):
        self.rank_map = {
            '2': 0,
            '3': 1,
            '4': 2,
            '5': 3,
            '6': 4,
            '7': 5,
            '8': 6,
            '9': 7,
            'T': 8,
            'J': 9,
            'Q': 10,
            'K': 11,
            'A': 12
        }

        self.suit_map = {
            'C': 0,
            'D': 1,
            'H': 2,
            'S': 3,
            'c': 0,
            'd': 1,
            'h': 2,
            's': 3
        }

        self.binaries_by_id = [
            0x1, 0x1, 0x1, 0x1,
            0x2, 0x2, 0x2, 0x2,
            0x4, 0x4, 0x4, 0x4,
            0x8, 0x8, 0x8, 0x8,
            0x10, 0x10, 0x10, 0x10,
            0x20, 0x20, 0x20, 0x20,
            0x40, 0x40, 0x40, 0x40,
            0x80, 0x80, 0x80, 0x80,
            0x100, 0x100, 0x100, 0x100,
            0x200, 0x200, 0x200, 0x200,
            0x400, 0x400, 0x400, 0x400,
            0x800, 0x800, 0x800, 0x800,
            0x1000, 0x1000, 0x1000, 0x1000,
        ]
        self.suitbit_by_id = [0x1, 0x8, 0x40, 0x200, ] * 13

    def evaluate_omaha5_cards(self, c1, c2, c3, c4, c5, h1, h2, h3, h4, h5):
        value_flush = 10000
        suit_count_board = [0, 0, 0, 0, 0]
        suit_count_hole = [0, 0, 0, 0, 0]

        suit_count_board[c1 & 0x3] += 1
        suit_count_board[c2 & 0x3] += 1
        suit_count_board[c3 & 0x3] += 1
        suit_count_board[c4 & 0x3] += 1
        suit_count_board[c5 & 0x3] += 1

        suit_count_hole[h1 & 0x3] += 1
        suit_count_hole[h2 & 0x3] += 1
        suit_count_hole[h3 & 0x3] += 1
        suit_count_hole[h4 & 0x3] += 1
        suit_count_hole[h5 & 0x3] += 1

        for i in range(5):
            if suit_count_board[i] >= 3 and suit_count_hole[i] >= 2:
                suit_binary_board = [0, 0, 0, 0, 0]

                suit_binary_board[c1 & 0x3] |= self.binaries_by_id[c1]
                suit_binary_board[c2 & 0x3] |= self.binaries_by_id[c2]
                suit_binary_board[c3 & 0x3] |= self.binaries_by_id[c3]
                suit_binary_board[c4 & 0x3] |= self.binaries_by_id[c4]
                suit_binary_board[c5 & 0x3] |= self.binaries_by_id[c5]

                suit_binary_hole = [0, 0, 0, 0, 0]

                suit_binary_hole[h1 & 0x3] |= self.binaries_by_id[h1]
                suit_binary_hole[h2 & 0x3] |= self.binaries_by_id[h2]
                suit_binary_hole[h3 & 0x3] |= self.binaries_by_id[h3]
                suit_binary_hole[h4 & 0x3] |= self.binaries_by_id[h4]
                suit_binary_hole[h5 & 0x3] |= self.binaries_by_id[h5]

                if suit_count_board[i] == 3 and suit_count_hole[i] == 2:
                    value_flush = FLUSH[suit_binary_board[i] | suit_binary_hole[i]]
                else:
                    padding = [0x0000, 0x2000, 0x6000]

                    suit_binary_board[i] |= padding[5 - suit_count_board[i]]
                    suit_binary_hole[i] |= padding[5 - suit_count_hole[i]]

                    board_hash = hash_binary(suit_binary_board[i], 5)
                    hole_hash = hash_binary(suit_binary_hole[i], 5)

                    value_flush = FLUSH_OMAHA[board_hash * 1365 + hole_hash]

                break

        quinary_board = [0] * 13
        quinary_hole = [0] * 13

        quinary_board[(c1 >> 2)] += 1
        quinary_board[(c2 >> 2)] += 1
        quinary_board[(c3 >> 2)] += 1
        quinary_board[(c4 >> 2)] += 1
        quinary_board[(c5 >> 2)] += 1

        quinary_hole[(h1 >> 2)] += 1
        quinary_hole[(h2 >> 2)] += 1
        quinary_hole[(h3 >> 2)] += 1
        quinary_hole[(h4 >> 2)] += 1
        quinary_hole[(h5 >> 2)] += 1

        board_hash = hash_quinary(quinary_board, 13, 5)
        hole_hash = hash_quinary(quinary_hole, 13, 5)

        value_noflush = NO_FLUSH_OMAHA[board_hash * 1820 + hole_hash]

        if value_flush < value_noflush:
            return value_flush
        else:
            return value_noflush

    def evaluate_omaha_cards(self, c1, c2, c3, c4, c5, h1, h2, h3, h4):
        value_flush = 10000
        suit_count_board = [0, 0, 0, 0]
        suit_count_hole = [0, 0, 0, 0]

        suit_count_board[c1 & 0x3] += 1
        suit_count_board[c2 & 0x3] += 1
        suit_count_board[c3 & 0x3] += 1
        suit_count_board[c4 & 0x3] += 1
        suit_count_board[c5 & 0x3] += 1

        suit_count_hole[h1 & 0x3] += 1
        suit_count_hole[h2 & 0x3] += 1
        suit_count_hole[h3 & 0x3] += 1
        suit_count_hole[h4 & 0x3] += 1

        for i in range(4):
            if suit_count_board[i] >= 3 and suit_count_hole[i] >= 2:
                suit_binary_board = [0, 0, 0, 0]

                suit_binary_board[c1 & 0x3] |= self.binaries_by_id[c1]
                suit_binary_board[c2 & 0x3] |= self.binaries_by_id[c2]
                suit_binary_board[c3 & 0x3] |= self.binaries_by_id[c3]
                suit_binary_board[c4 & 0x3] |= self.binaries_by_id[c4]
                suit_binary_board[c5 & 0x3] |= self.binaries_by_id[c5]

                suit_binary_hole = [0, 0, 0, 0]
                suit_binary_hole[h1 & 0x3] |= self.binaries_by_id[h1]
                suit_binary_hole[h2 & 0x3] |= self.binaries_by_id[h2]
                suit_binary_hole[h3 & 0x3] |= self.binaries_by_id[h3]
                suit_binary_hole[h4 & 0x3] |= self.binaries_by_id[h4]

                if suit_count_board[i] == 3 and suit_count_hole[i] == 2:
                    value_flush = FLUSH[suit_binary_board[i] | suit_binary_hole[i]]
                else:
                    padding = [0x0000, 0x2000, 0x6000]

                    suit_binary_board[i] |= padding[5 - suit_count_board[i]]
                    suit_binary_hole[i] |= padding[4 - suit_count_hole[i]]

                    board_hash = hash_binary(suit_binary_board[i], 5)
                    hole_hash = hash_binary(suit_binary_hole[i], 4)

                    value_flush = FLUSH_OMAHA[board_hash * 1365 + hole_hash]

                break

        quinary_board = [0] * 13
        quinary_hole = [0] * 13

        quinary_board[(c1 >> 2)] += 1
        quinary_board[(c2 >> 2)] += 1
        quinary_board[(c3 >> 2)] += 1
        quinary_board[(c4 >> 2)] += 1
        quinary_board[(c5 >> 2)] += 1

        quinary_hole[(h1 >> 2)] += 1
        quinary_hole[(h2 >> 2)] += 1
        quinary_hole[(h3 >> 2)] += 1
        quinary_hole[(h4 >> 2)] += 1

        board_hash = hash_quinary(quinary_board, 13, 5)
        hole_hash = hash_quinary(quinary_hole, 13, 4)

        value_noflush = NO_FLUSH_OMAHA[board_hash * 1820 + hole_hash]

        if value_flush < value_noflush:
            return value_flush
        else:
            return value_noflush

    def evaluate_cards(self, *args):
        if isinstance(args[0], str):
            cards = []
            for arg in args:
                cards.append(self.rank_map[arg[0]] * 4 + self.suit_map[arg[1]])
        else:
            cards = tuple(args)
        if len(args) == 9:
            return self.evaluate_omaha_cards(*cards)
        elif len(args) == 10:
            return self.evaluate_omaha5_cards(*cards)
