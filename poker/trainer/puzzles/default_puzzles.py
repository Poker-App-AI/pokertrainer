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
PUZZLES += [
    Puzzle(
        player_hand="AhKh",
        board_cards="AdKs7c2d",
        pot_size=300,
        bet_to_call=100,
        player_chips_remaining=800,
        opponents=[Opponent(type="tight", chips_remaining=900)],
        current_player_to_act_index=0,
        question="You have top two pair on the turn. Opponent bets pot. What do you do?"
    ),
    Puzzle(
        player_hand="9h9d",
        board_cards="9s4c2hQc",
        pot_size=250,
        bet_to_call=80,
        player_chips_remaining=700,
        opponents=[Opponent(type="standard", chips_remaining=600)],
        current_player_to_act_index=0,
        question="You flopped a set and turn brings a queen. Opponent bets half pot. What's your move?"
    ),
    Puzzle(
        player_hand="8s7s",
        board_cards="6s5h9dTd",
        pot_size=280,
        bet_to_call=90,
        player_chips_remaining=600,
        opponents=[Opponent(type="loose", chips_remaining=400)],
        current_player_to_act_index=0,
        question="You turned a straight with 7-8 on a draw heavy board. Opponent bets big. Your move?"
    ),
    Puzzle(
        player_hand="KcQc",
        board_cards="KsQh2s7d",
        pot_size=200,
        bet_to_call=70,
        player_chips_remaining=800,
        opponents=[Opponent(type="tight", chips_remaining=750)],
        current_player_to_act_index=0,
        question="Top two pair on the turn. Opponent bets small. What's your action?"
    ),
    Puzzle(
        player_hand="JhTh",
        board_cards="Qd9h8h2c",
        pot_size=260,
        bet_to_call=85,
        player_chips_remaining=550,
        opponents=[Opponent(type="standard", chips_remaining=500)],
        current_player_to_act_index=0,
        question="You flopped a straight. Turn is a blank. Opponent bets 85 into 260. What's your move?"
    ),
    Puzzle(
        player_hand="AsQs",
        board_cards="Ad7c4hQd",
        pot_size=310,
        bet_to_call=100,
        player_chips_remaining=850,
        opponents=[Opponent(type="loose", chips_remaining=500)],
        current_player_to_act_index=0,
        question="Top two pair on turn, opponent bets large. What's your action?"
    ),
    Puzzle(
        player_hand="5d5s",
        board_cards="7h5c2d8s",
        pot_size=220,
        bet_to_call=70,
        player_chips_remaining=600,
        opponents=[Opponent(type="tight", chips_remaining=650)],
        current_player_to_act_index=0,
        question="You flopped a set. Turn brings an 8. Opponent bets. What's your move?"
    ),
    Puzzle(
        player_hand="KdTd",
        board_cards="KsTs2h8c",
        pot_size=240,
        bet_to_call=80,
        player_chips_remaining=700,
        opponents=[Opponent(type="standard", chips_remaining=400)],
        current_player_to_act_index=0,
        question="Top two pair on turn, opponent bets half pot. Your move?"
    ),
    Puzzle(
        player_hand="JsTs",
        board_cards="Qs9s8c7d",
        pot_size=300,
        bet_to_call=100,
        player_chips_remaining=800,
        opponents=[Opponent(type="loose", chips_remaining=500)],
        current_player_to_act_index=0,
        question="You flopped a straight, turn brings a dangerous 7 completing multiple draws. Opponent bets pot. What's your action?"
    ),
    Puzzle(
        player_hand="AcKc",
        board_cards="AhKd2d7hQc",
        pot_size=400,
        bet_to_call=150,
        player_chips_remaining=900,
        opponents=[Opponent(type="tight", chips_remaining=800)],
        current_player_to_act_index=0,
        question="River completes with a queen. You have top two pair. Opponent bets large. What's your move?"
    ),
]
PUZZLES += [
    Puzzle(
        player_hand="AhKh",
        board_cards="AdKs7c2d",
        pot_size=300,
        bet_to_call=100,
        player_chips_remaining=800,
        opponents=[Opponent(type="tight", chips_remaining=900)],
        current_player_to_act_index=0,
        question="You have top two pair on the turn. Opponent bets pot. What do you do?"
    ),
    Puzzle(
        player_hand="9h9d",
        board_cards="9s4c2hQc",
        pot_size=250,
        bet_to_call=80,
        player_chips_remaining=700,
        opponents=[Opponent(type="standard", chips_remaining=600)],
        current_player_to_act_index=0,
        question="You flopped a set and turn brings a queen. Opponent bets half pot. What's your move?"
    ),
    Puzzle(
        player_hand="8s7s",
        board_cards="6s5h9dTd",
        pot_size=280,
        bet_to_call=90,
        player_chips_remaining=600,
        opponents=[Opponent(type="loose", chips_remaining=400)],
        current_player_to_act_index=0,
        question="You turned a straight with 7-8 on a draw heavy board. Opponent bets big. Your move?"
    ),
    Puzzle(
        player_hand="KcQc",
        board_cards="KsQh2s7d",
        pot_size=200,
        bet_to_call=70,
        player_chips_remaining=800,
        opponents=[Opponent(type="tight", chips_remaining=750)],
        current_player_to_act_index=0,
        question="Top two pair on the turn. Opponent bets small. What's your action?"
    ),
    Puzzle(
        player_hand="JhTh",
        board_cards="Qd9h8h2c",
        pot_size=260,
        bet_to_call=85,
        player_chips_remaining=550,
        opponents=[Opponent(type="standard", chips_remaining=500)],
        current_player_to_act_index=0,
        question="You flopped a straight. Turn is a blank. Opponent bets 85 into 260. What's your move?"
    ),
    Puzzle(
        player_hand="AsQs",
        board_cards="Ad7c4hQd",
        pot_size=310,
        bet_to_call=100,
        player_chips_remaining=850,
        opponents=[Opponent(type="loose", chips_remaining=500)],
        current_player_to_act_index=0,
        question="Top two pair on turn, opponent bets large. What's your action?"
    ),
    Puzzle(
        player_hand="5d5s",
        board_cards="7h5c2d8s",
        pot_size=220,
        bet_to_call=70,
        player_chips_remaining=600,
        opponents=[Opponent(type="tight", chips_remaining=650)],
        current_player_to_act_index=0,
        question="You flopped a set. Turn brings an 8. Opponent bets. What's your move?"
    ),
    Puzzle(
        player_hand="KdTd",
        board_cards="KsTs2h8c",
        pot_size=240,
        bet_to_call=80,
        player_chips_remaining=700,
        opponents=[Opponent(type="standard", chips_remaining=400)],
        current_player_to_act_index=0,
        question="Top two pair on turn, opponent bets half pot. Your move?"
    ),
    Puzzle(
        player_hand="JsTs",
        board_cards="Qs9s8c7d",
        pot_size=300,
        bet_to_call=100,
        player_chips_remaining=800,
        opponents=[Opponent(type="loose", chips_remaining=500)],
        current_player_to_act_index=0,
        question="You flopped a straight, turn brings a dangerous 7 completing multiple draws. Opponent bets pot. What's your action?"
    ),
    Puzzle(
        player_hand="AcKc",
        board_cards="AhKd2d7hQc",
        pot_size=400,
        bet_to_call=150,
        player_chips_remaining=900,
        opponents=[Opponent(type="tight", chips_remaining=800)],
        current_player_to_act_index=0,
        question="River completes with a queen. You have top two pair. Opponent bets large. What's your move?"
    ),
]
PUZZLES += [
    Puzzle(player_hand="7d7h", board_cards="TsJh2c", pot_size=200, bet_to_call=40, player_chips_remaining=800, opponents=[Opponent(type="standard", chips_remaining=500)], current_player_to_act_index=0, question="Opponent bets on the flop, what's your move?"),
    Puzzle(player_hand="AcKs", board_cards="", pot_size=50, bet_to_call=15, player_chips_remaining=1000, opponents=[Opponent(type="tight", chips_remaining=1200)], current_player_to_act_index=0, question="You are UTG preflop, what's your action?"),
    Puzzle(player_hand="QsJd", board_cards="8c9cTc", pot_size=180, bet_to_call=60, player_chips_remaining=600, opponents=[Opponent(type="loose", chips_remaining=500)], current_player_to_act_index=0, question="You flopped a straight, opponent bets, what now?"),
    Puzzle(player_hand="5h5s", board_cards="3d7cQc", pot_size=90, bet_to_call=20, player_chips_remaining=450, opponents=[Opponent(type="standard", chips_remaining=400)], current_player_to_act_index=0, question="Facing a continuation bet on the flop, what's your move?"),
    Puzzle(player_hand="AhKd", board_cards="Kh8s2c", pot_size=120, bet_to_call=40, player_chips_remaining=900, opponents=[Opponent(type="tight", chips_remaining=700)], current_player_to_act_index=0, question="You hit top pair top kicker on the flop, opponent bets, what now?"),
    Puzzle(player_hand="ThTd", board_cards="2h5sJc", pot_size=140, bet_to_call=35, player_chips_remaining=700, opponents=[Opponent(type="standard", chips_remaining=800)], current_player_to_act_index=0, question="Opponent bets on the flop, your action?"),
    Puzzle(player_hand="6h6d", board_cards="4s5d8h", pot_size=110, bet_to_call=30, player_chips_remaining=500, opponents=[Opponent(type="loose", chips_remaining=300)], current_player_to_act_index=0, question="Facing a bet on the flop with an underpair, what do you do?"),
    Puzzle(player_hand="QcJh", board_cards="", pot_size=60, bet_to_call=20, player_chips_remaining=600, opponents=[Opponent(type="tight", chips_remaining=900)], current_player_to_act_index=0, question="Preflop facing a raise, what's your move?"),
    Puzzle(player_hand="AdKd", board_cards="AsTs9d", pot_size=250, bet_to_call=75, player_chips_remaining=950, opponents=[Opponent(type="standard", chips_remaining=600)], current_player_to_act_index=0, question="Top pair top kicker on a draw-heavy flop, opponent bets big, what's your move?"),
    Puzzle(player_hand="JhJs", board_cards="Qd8h2c", pot_size=100, bet_to_call=25, player_chips_remaining=700, opponents=[Opponent(type="loose", chips_remaining=550)], current_player_to_act_index=0, question="Opponent bets on the flop, your action with an overpair?"),
    Puzzle(player_hand="8d9d", board_cards="TdJhQc", pot_size=180, bet_to_call=50, player_chips_remaining=800, opponents=[Opponent(type="standard", chips_remaining=500)], current_player_to_act_index=0, question="You flopped a straight, what's your move facing a bet?"),
    Puzzle(player_hand="KhQh", board_cards="", pot_size=40, bet_to_call=10, player_chips_remaining=960, opponents=[Opponent(type="tight", chips_remaining=700)], current_player_to_act_index=0, question="Preflop facing a raise, your action?"),
    Puzzle(player_hand="7h8h", board_cards="5h6h9c", pot_size=200, bet_to_call=60, player_chips_remaining=600, opponents=[Opponent(type="loose", chips_remaining=500)], current_player_to_act_index=0, question="You flopped a straight flush draw, facing a bet, what's your move?"),
    Puzzle(player_hand="AsQs", board_cards="Ad7c4h", pot_size=130, bet_to_call=35, player_chips_remaining=750, opponents=[Opponent(type="standard", chips_remaining=400)], current_player_to_act_index=0, question="Top pair top kicker on flop, facing a bet, what do you do?"),
    Puzzle(player_hand="3c3h", board_cards="2d5s9c", pot_size=90, bet_to_call=25, player_chips_remaining=400, opponents=[Opponent(type="tight", chips_remaining=600)], current_player_to_act_index=0, question="Small pocket pair, facing a bet on flop, what's your action?"),
    Puzzle(player_hand="KdTd", board_cards="", pot_size=50, bet_to_call=15, player_chips_remaining=700, opponents=[Opponent(type="loose", chips_remaining=500)], current_player_to_act_index=0, question="Preflop facing a raise, what's your move?"),
    Puzzle(player_hand="Ah9h", board_cards="Kh5h2c", pot_size=100, bet_to_call=30, player_chips_remaining=600, opponents=[Opponent(type="standard", chips_remaining=400)], current_player_to_act_index=0, question="Flopped flush draw + overcard, facing bet, your action?"),
    Puzzle(player_hand="9s9d", board_cards="3c5h9h", pot_size=120, bet_to_call=40, player_chips_remaining=800, opponents=[Opponent(type="tight", chips_remaining=900)], current_player_to_act_index=0, question="You flopped a set, opponent bets, what now?"),
]