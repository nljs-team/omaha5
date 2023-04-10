from textwrap import wrap
from typing import List

from casino.table import Table
from evaluator.evaluator import Evaluator


class Simulator:
    def __init__(self, players_num: int = 3, simulations_num: int = 10):
        """

        :param players_num: number of players
        :param simulations_num: number of simulations
        """
        self._simulations_num = simulations_num
        self.table = Table(players_num=players_num)
        self.evaluator = Evaluator()

    def simulate(self, deck_type: str = "full"):
        """
        Simulates a number of poker games
        :param deck_type: number of cards in deck (52 for full, 36 for short)
        :return:
        """
        all_combinations, all_combinations_num = self.table.get_all_deck_combinations()
        for combination in all_combinations:
            self.table._community_hand = self.table.start_community_hand + "".join(combination)
            hands_values = self.play(self.table.community_hand, self.table.hands)
            for player in self.table.players:
                if player.hand == hands_values[0][0]:
                    player.wins_game()
        self._simulations_num = all_combinations_num

    def evaluate_one_player(self, board: tuple, hand: str):
        all_4_combinations = [hand[2:], hand[:2] + hand[4:], hand[:4] + hand[6:], hand[:6] + hand[8:], hand[:8]]
        for i in range(len(all_4_combinations)):
            all_4_combinations[i] = tuple(wrap(all_4_combinations[i], 2))
        all_4_combinations.sort(key=lambda x: self.evaluator.evaluate_cards(*board, *x))
        ranks = list(map(lambda x: self.evaluator.evaluate_cards(*board, *x), all_4_combinations))
        return all_4_combinations[0], ranks[0]

    def play(self, community_hand: str, players_hands: List[str]):
        """
        Simulates one poker game
        :param community_hand: cards on table
        :param players_hands: cards in players' pockets
        :return: all players' hands with appropriate ranks (the less the rank the better hand is)
        """
        board = tuple(wrap(community_hand, 2))
        highest_hands, highest_ranks = [], []
        for hand in players_hands:
            highest_hand, rank = self.evaluate_one_player(board, hand)
            highest_hands.append(''.join(hand))
            highest_ranks.append(rank)
        hands_values = list(zip(highest_hands, highest_ranks))
        hands_values.sort(key=lambda t: t[1])
        return hands_values

    def show_status(self) -> None:
        """
        Show win probability from all simulations
        :return:
        """
        for player in self.table.players:
            print("Player {} with {:.2f} percent win probability".format(
                player.number, player.wins / self._simulations_num * 100
            )
        )
