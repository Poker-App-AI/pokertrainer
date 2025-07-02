from poker.trainer.models.puzzle import Puzzle, Opponent

PUZZLES = [
    Puzzle(
        player_hand="KhJc",
        board_cards="AsTs5h",
        pot_size=100,
        bet_to_call=20,
        player_chips_remaining=500,
        opponents=[
            Opponent(type="standard", chips_remaining=400),
            Opponent(type="tight", chips_remaining=600)
        ],
        current_player_to_act_index=0,
        question="What should you do?"
    ),
    Puzzle(
        player_hand="9h9c",
        board_cards="2s5d8c",
        pot_size=150,
        bet_to_call=50,
        player_chips_remaining=350,
        opponents=[
            Opponent(type="loose", chips_remaining=200)
        ],
        current_player_to_act_index=0,
        question="Facing a large bet, what's your move?"
    ),
    Puzzle(
        player_hand="AdQc",
        board_cards="",
        pot_size=30,
        bet_to_call=10,
        player_chips_remaining=970,
        opponents=[
            Opponent(type="tight", chips_remaining=1000),
            Opponent(type="standard", chips_remaining=500)
        ],
        current_player_to_act_index=0,
        question="Preflop action: What should you do?"
    ),
] 