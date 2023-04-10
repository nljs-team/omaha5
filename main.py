from casino.simulator import Simulator
from evaluator.validator import Validator

if __name__ == "__main__":
    players_num = int(input("Input number of players at table: "))
    while players_num < 2 or players_num > 6:
        print("Wrong number of players! Should be 2-6")
        players_num = int(input("Input number of players at table: "))

    print(f"\n{players_num} players at the table\n")

    simulator = Simulator(players_num=players_num)
    validator = Validator()

    hands = input("""Input hands for all players(one line separated by whitespace).
Use 2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K to set card value and c, d, s, h to set card suit.
Like this: AhTd2s2h4d QhKd6h7sTc: 
    """)
    hands = hands.split()

    ret, message = validator.validate_game(board="", hands=hands)
    while not ret:
        print(message)
        hands = input("""Input hands for all players(one line separated by whitespace).
Use 2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K to set card value and c, d, s, h to set card suit.
Like this: AhTd2s2h4d QhKd6h7sTc: 
            """)
        hands = hands.split()
        ret, message = validator.validate_game(board="", hands=hands)

    for num, player in enumerate(simulator.table.players):
        player.add_hand(hands[num])
    print(simulator.table.players_hands)

    game_stage = input("Input current game stage (preflop, flop, turn): ")
    while game_stage not in ["preflop", "flop", "turn"]:
        print("Please input valid game stage")
        game_stage = input("Input current game stage (preflop, flop, turn): ")

    simulator.table.start_game_stage = game_stage
    simulator.table.set_stage_iterator(game_stage)
    simulator.table.generate_deck("full")
    simulator.table.set_stage_deck(hands)

    if game_stage != "preflop":
        board_cards = input("Input boards cards (same way as hands):")
        ret, message = validator.validate_game(board_cards, hands)
        while not ret:
            print(message)
            board_cards = input("Input boards cards (same way as hands):")
            ret, message = validator.validate_game(board_cards, hands)

        simulator.table.set_stage_deck(board_cards)
        simulator.table.start_community_hand = board_cards
    simulator.simulate("full")
    simulator.show_status()
