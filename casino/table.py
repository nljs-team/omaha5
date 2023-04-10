import random
from itertools import combinations
from textwrap import wrap
from typing import List, Union

from casino.exceptions import DeckException
from casino.player import Player


class Table:
    def __init__(self, players_num: int) -> None:
        """
        Initialize new table
        :param players_num: number of poker players
        """
        self._deck = None
        self.players_num = players_num
        self.players = [Player(number=player_num) for player_num in range(1, players_num + 1)]
        self.start_community_hand = ""
        self._community_hand = ""
        self.game_stages = {
            "flop": 3,
            "turn": 1,
            "river": 1
        }
        self.start_game_stage = None
        self._current_game_stage = None
        self._game_stages_iter = None

    def generate_deck(self, deck_type: str) -> None:
        """
        Generate shuffled deck for game
        :param deck_type: type of deck: full of short
        :return: deck (list of strings)
        """
        if deck_type == "full":
            vals = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
        elif deck_type == "short":
            vals = ["6", "7", "8", "9", "T", "J", "Q", "K", "A"]
        else:
            raise DeckException("Invalid Deck Type. Valid options are: full/short ")

        suits = ["s", "c", "h", "d"]
        self._deck = [v + s for v in vals for s in suits]
        random.shuffle(self._deck)

    def set_stage_deck(self, hands: Union[str, List[str]]):
        if isinstance(hands, str):
            cards = list(wrap(hands, 2))
        else:
            cards = list(wrap(''.join(hands), 2))
        for card in cards:
            self._deck.remove(card)

    def generate_hand(self, deck: List[str], hand_size: int = 4) -> str:
        """
        Generate hand (for player or community)
        :param deck: deck of cards
        :param hand_size: number of cards to give
        :return: hand
        """
        hand = ""
        if hand_size < len(deck):
            for i in range(hand_size):
                hand += deck[0]
                deck.pop(0)
        return hand

    def deal_players(self) -> None:
        """
        Deal cards to players
        :return:
        """
        for player in self.players:
            player.add_hand(self.generate_hand(self._deck, hand_size=5))

    def deal_community(self) -> None:
        """
        Deal community cards
        :return:
        """
        self._community_hand += self.generate_hand(self._deck, hand_size=5)

    def flush_game(self):
        """
        Clean table
        :return:
        """
        self._community_hand = self.start_community_hand
        self._current_game_stage = self.start_game_stage

    def add_to_community(self, game_stage: str) -> None:
        """
        Add cards to community
        :param game_stage: Current game stage (flop, turn or river)
        :return: extended community cards
        """
        self._community_hand += self.generate_hand(self._deck, self.game_stages[game_stage])

    def set_stage_iterator(self, game_stage: str) -> int:
        game_stages = None
        if game_stage == "preflop":
            game_stages = ["flop", "turn", "river"]
            self._game_stages_iter = iter(game_stages)
        elif game_stage == "flop":
            game_stages = ["turn", "river"]
            self._game_stages_iter = iter(game_stages)
        elif game_stage == "turn":
            game_stages = ["river"]
            self._game_stages_iter = iter(game_stages)
        self._current_game_stage = self.start_game_stage
        return len(game_stages)

    def get_all_deck_combinations(self):
        combinations_len = (10 - len(self.start_community_hand)) // 2
        all_combinations = combinations(self._deck, combinations_len)
        all_combinations_num = 0
        for _ in all_combinations:
            all_combinations_num += 1
        all_combinations = combinations(self._deck, combinations_len)
        return all_combinations, all_combinations_num

    def new_round(self) -> None:
        """
        Trigger new round of game (draw cards to community)
        :return:
        """
        self._current_game_stage = next(self._game_stages_iter)
        self.add_to_community(self._current_game_stage)

    @property
    def community_hand(self) -> str:
        return self._community_hand

    @property
    def players_hands(self) -> str:
        """
        Show all players' hands
        :return: current players' hands
        """
        situation = ""
        for player in self.players:
            situation += "Player {} hand: {} \n".format(player.number, player.hand)
        return situation

    @property
    def hands(self) -> List[str]:
        return [player.hand for player in self.players]

    @property
    def game_cards(self):
        return self._community_hand + " " + " ".join([player.hand for player in self.players])

    @property
    def deck_size(self) -> int:
        return len(self._deck)
