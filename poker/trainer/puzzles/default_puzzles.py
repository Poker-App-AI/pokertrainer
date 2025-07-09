from poker.trainer.models.puzzle import Puzzle, Opponent
import random

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

PUZZLES += [
    Puzzle(
        player_hand="AsJs",
        board_cards="Ah7d4s9c",
        pot_size=400,
        bet_to_call=200,
        player_chips_remaining=800,
        opponents=[Opponent(type="tight", chips_remaining=600)],
        current_player_to_act_index=0,
        question="Top pair, good kicker, facing a pot-sized bet on the turn from a tight opponent. What's your move?"
    ),
    Puzzle(
        player_hand="9h9c",
        board_cards="5d6s7cKd",
        pot_size=350,
        bet_to_call=175,
        player_chips_remaining=700,
        opponents=[Opponent(type="standard", chips_remaining=500)],
        current_player_to_act_index=0,
        question="You have an overpair to the flop but the turn brings an overcard (K). Opponent bets half pot. What's your decision?"
    ),
    Puzzle(
        player_hand="KhQh",
        board_cards="Ks8c3d7s",
        pot_size=320,
        bet_to_call=160,
        player_chips_remaining=900,
        opponents=[Opponent(type="loose", chips_remaining=400)],
        current_player_to_act_index=0,
        question="Top pair, strong kicker, opponent bets half pot on turn. They can bluff often, but do you raise or call?"
    ),
    Puzzle(
        player_hand="AdTc",
        board_cards="AsTd4h2d",
        pot_size=300,
        bet_to_call=150,
        player_chips_remaining=650,
        opponents=[Opponent(type="tight", chips_remaining=600)],
        current_player_to_act_index=0,
        question="Top two pair but a flush draw is possible. Opponent bets half pot on turn. What's your move?"
    ),
    Puzzle(
        player_hand="JhTh",
        board_cards="Qd9h8h4c",
        pot_size=400,
        bet_to_call=200,
        player_chips_remaining=600,
        opponents=[Opponent(type="standard", chips_remaining=500)],
        current_player_to_act_index=0,
        question="You flopped a straight, turn is a blank. Opponent bets half pot. Tough spot against a balanced opponent. What's your move?"
    ),
    Puzzle(
        player_hand="8c8d",
        board_cards="7h8sQdTs",
        pot_size=350,
        bet_to_call=175,
        player_chips_remaining=700,
        opponents=[Opponent(type="loose", chips_remaining=400)],
        current_player_to_act_index=0,
        question="You flopped a set but turn brings straight possibilities. Opponent bets big. What's your move?"
    ),
    Puzzle(
        player_hand="QcJc",
        board_cards="KdTs9c5h",
        pot_size=300,
        bet_to_call=150,
        player_chips_remaining=600,
        opponents=[Opponent(type="tight", chips_remaining=700)],
        current_player_to_act_index=0,
        question="You flopped an open-ended straight draw, turn bricks. Opponent bets half pot. Call to see river or fold?"
    ),
    Puzzle(
        player_hand="Ac9c",
        board_cards="As7d3c9h",
        pot_size=330,
        bet_to_call=165,
        player_chips_remaining=700,
        opponents=[Opponent(type="standard", chips_remaining=500)],
        current_player_to_act_index=0,
        question="Top two pair, opponent bets half pot on turn. They are capable of semi-bluffing. What's your move?"
    ),
    Puzzle(
        player_hand="7s7h",
        board_cards="2d5c7d8d",
        pot_size=280,
        bet_to_call=140,
        player_chips_remaining=600,
        opponents=[Opponent(type="loose", chips_remaining=400)],
        current_player_to_act_index=0,
        question="You flopped a set but turn completes many draws. Opponent bets half pot. What's your decision?"
    ),
    Puzzle(
        player_hand="KdJd",
        board_cards="KsTs8d2s",
        pot_size=310,
        bet_to_call=155,
        player_chips_remaining=800,
        opponents=[Opponent(type="tight", chips_remaining=700)],
        current_player_to_act_index=0,
        question="Top pair, decent kicker, opponent bets half pot on turn. Their tight image makes this tough. What's your move?"
    ),
]
PUZZLES += [
    # 💔 Tough fold
    Puzzle(
        player_hand="QdQs",
        board_cards="KdJs8hAs",
        pot_size=500,
        bet_to_call=250,
        player_chips_remaining=800,
        opponents=[Opponent(type="tight", chips_remaining=700)],
        current_player_to_act_index=0,
        question="You have an overpair but the board has multiple overcards and straight possibilities. Opponent bets half pot on turn. Fold or call?"
    ),
    # 💔 Tough fold
    Puzzle(
        player_hand="ThTs",
        board_cards="QhJh9s8c",
        pot_size=450,
        bet_to_call=225,
        player_chips_remaining=600,
        opponents=[Opponent(type="standard", chips_remaining=500)],
        current_player_to_act_index=0,
        question="You have an overpair but opponent bets big on a dangerous board. Tough fold or call?"
    ),
    # 🧐 Tough call
    Puzzle(
        player_hand="AcQc",
        board_cards="As7h4d9c",
        pot_size=400,
        bet_to_call=200,
        player_chips_remaining=700,
        opponents=[Opponent(type="loose", chips_remaining=400)],
        current_player_to_act_index=0,
        question="Top pair top kicker facing a pot-sized bet from a loose opponent on turn. Tough call or fold?"
    ),
    # 🧐 Tough call
    Puzzle(
        player_hand="8h8s",
        board_cards="2c5d8cJd",
        pot_size=350,
        bet_to_call=175,
        player_chips_remaining=600,
        opponents=[Opponent(type="tight", chips_remaining=700)],
        current_player_to_act_index=0,
        question="You have a set but opponent bets large on turn with flush possibilities. Tough call or fold?"
    ),
    # 🧐 Tough call
    Puzzle(
        player_hand="KdJd",
        board_cards="Ks7s2h4d",
        pot_size=300,
        bet_to_call=150,
        player_chips_remaining=650,
        opponents=[Opponent(type="standard", chips_remaining=500)],
        current_player_to_act_index=0,
        question="Top pair with decent kicker. Opponent bets half pot on turn. Tough call or fold?"
    ),
    # 💥 Tough raise
    Puzzle(
        player_hand="JsTs",
        board_cards="Qs9s8h2d",
        pot_size=400,
        bet_to_call=100,
        player_chips_remaining=900,
        opponents=[Opponent(type="loose", chips_remaining=400)],
        current_player_to_act_index=0,
        question="You flopped a straight. Opponent bets small on turn. Do you just call or go for a tough value raise?"
    ),
    # 💥 Tough raise
    Puzzle(
        player_hand="AhKh",
        board_cards="AdKd7c2d",
        pot_size=500,
        bet_to_call=100,
        player_chips_remaining=1000,
        opponents=[Opponent(type="tight", chips_remaining=800)],
        current_player_to_act_index=0,
        question="You have top two pair and opponent bets small on turn. Tough raise for value or just call?"
    ),
    # 💥 Tough raise
    Puzzle(
        player_hand="9d9c",
        board_cards="5s9h2c6h",
        pot_size=350,
        bet_to_call=90,
        player_chips_remaining=700,
        opponents=[Opponent(type="standard", chips_remaining=500)],
        current_player_to_act_index=0,
        question="You flopped a set and turn brings straight possibilities. Opponent bets small. Tough raise or call?"
    ),
    # 🧐 Tough call
    Puzzle(
        player_hand="QsJs",
        board_cards="QcJd8c4s",
        pot_size=400,
        bet_to_call=200,
        player_chips_remaining=800,
        opponents=[Opponent(type="loose", chips_remaining=600)],
        current_player_to_act_index=0,
        question="Top two pair on turn. Opponent bets half pot. Tough call or fold?"
    ),
    # 💔 Tough fold
    Puzzle(
        player_hand="6d6c",
        board_cards="9s8s7hTd",
        pot_size=450,
        bet_to_call=225,
        player_chips_remaining=600,
        opponents=[Opponent(type="tight", chips_remaining=700)],
        current_player_to_act_index=0,
        question="Your underpair is crushed on this board with straight possibilities. Opponent bets big. Tough fold or call?"
    ),
]
PUZZLES += [
    # Preflop - easy fold
    Puzzle(player_hand="7d2h", board_cards="", pot_size=30, bet_to_call=10, player_chips_remaining=990, opponents=[Opponent(type="tight", chips_remaining=1000)], current_player_to_act_index=0, question="You're UTG preflop with 7-2 offsuit. What's your move?"),
    # Preflop - tough call
    Puzzle(player_hand="JhTs", board_cards="", pot_size=50, bet_to_call=20, player_chips_remaining=980, opponents=[Opponent(type="standard", chips_remaining=950)], current_player_to_act_index=0, question="You're in the big blind with JTs facing a button raise. What's your action?"),
    # Preflop - easy raise
    Puzzle(player_hand="AhKh", board_cards="", pot_size=40, bet_to_call=10, player_chips_remaining=1000, opponents=[Opponent(type="tight", chips_remaining=1200)], current_player_to_act_index=0, question="You're on the button with AhKh. What's your move?"),
    # Flop - medium fold
    Puzzle(player_hand="9h9c", board_cards="QsJd8c", pot_size=150, bet_to_call=75, player_chips_remaining=850, opponents=[Opponent(type="standard", chips_remaining=900)], current_player_to_act_index=0, question="You have an underpair to the board. Opponent bets half pot. What's your move?"),
    # Flop - tough call
    Puzzle(player_hand="AcJs", board_cards="Ah7c5d", pot_size=200, bet_to_call=100, player_chips_remaining=800, opponents=[Opponent(type="loose", chips_remaining=400)], current_player_to_act_index=0, question="Top pair decent kicker facing a pot-sized bet from a loose opponent. What's your move?"),
    # Flop - easy raise
    Puzzle(player_hand="Th9h", board_cards="JhQh2c", pot_size=180, bet_to_call=60, player_chips_remaining=920, opponents=[Opponent(type="standard", chips_remaining=500)], current_player_to_act_index=0, question="You flopped a flush draw + open-ended straight draw. Opponent bets small. What's your action?"),
    # Turn - tough fold
    Puzzle(player_hand="8d8s", board_cards="Td9s6cQs", pot_size=300, bet_to_call=150, player_chips_remaining=600, opponents=[Opponent(type="tight", chips_remaining=700)], current_player_to_act_index=0, question="You have a low overpair. Board is dangerous. Opponent bets half pot. Fold or call?"),
    # Turn - medium call
    Puzzle(player_hand="KsQs", board_cards="Kc7d2h4s", pot_size=260, bet_to_call=100, player_chips_remaining=750, opponents=[Opponent(type="standard", chips_remaining=500)], current_player_to_act_index=0, question="Top pair, good kicker. Opponent bets small on turn. What's your move?"),
    # Turn - tough raise
    Puzzle(player_hand="JhTh", board_cards="9h8h2dQc", pot_size=400, bet_to_call=100, player_chips_remaining=800, opponents=[Opponent(type="loose", chips_remaining=400)], current_player_to_act_index=0, question="You flopped a straight. Turn is a queen. Opponent bets small. Raise or call?"),
    # River - tough fold
    Puzzle(player_hand="QcQs", board_cards="KdJd8s2hAc", pot_size=500, bet_to_call=250, player_chips_remaining=700, opponents=[Opponent(type="tight", chips_remaining=600)], current_player_to_act_index=0, question="You have a middle pair. River completes broadway. Opponent bets big. Tough fold or call?"),
    # River - tough call
    Puzzle(player_hand="AdTd", board_cards="Ah7h2c5s3d", pot_size=350, bet_to_call=175, player_chips_remaining=800, opponents=[Opponent(type="standard", chips_remaining=500)], current_player_to_act_index=0, question="Top pair decent kicker facing a big river bet. Tough call or fold?"),
    # River - tough raise
    Puzzle(player_hand="9h9s", board_cards="9d4c7s9c2h", pot_size=400, bet_to_call=100, player_chips_remaining=900, opponents=[Opponent(type="loose", chips_remaining=500)], current_player_to_act_index=0, question="You rivered quads. Opponent bets small. Raise or just call for value?"),
    # Preflop - medium fold
    Puzzle(player_hand="4d5s", board_cards="", pot_size=30, bet_to_call=15, player_chips_remaining=970, opponents=[Opponent(type="standard", chips_remaining=950)], current_player_to_act_index=0, question="You're in middle position with 4-5 offsuit facing a raise. What's your move?"),
    # Flop - easy call
    Puzzle(player_hand="KdQd", board_cards="Ks7c2h", pot_size=150, bet_to_call=50, player_chips_remaining=900, opponents=[Opponent(type="loose", chips_remaining=400)], current_player_to_act_index=0, question="Top pair, strong kicker, opponent bets small. What's your move?"),
    # Turn - medium raise
    Puzzle(player_hand="5h5c", board_cards="5d8h2s9s", pot_size=280, bet_to_call=70, player_chips_remaining=800, opponents=[Opponent(type="standard", chips_remaining=600)], current_player_to_act_index=0, question="You flopped a set. Turn brings straight draws. Opponent bets small. What's your move?"),
    # River - easy call
    Puzzle(player_hand="AcQc", board_cards="Ad7c4d2h9s", pot_size=400, bet_to_call=100, player_chips_remaining=950, opponents=[Opponent(type="tight", chips_remaining=700)], current_player_to_act_index=0, question="Top pair top kicker. Opponent bets small on river. What's your move?"),
    # River - tough raise
    Puzzle(player_hand="JhTh", board_cards="9h8hQd7h2s", pot_size=450, bet_to_call=150, player_chips_remaining=800, opponents=[Opponent(type="loose", chips_remaining=500)], current_player_to_act_index=0, question="You rivered a flush. Opponent bets small. Raise or just call?"),
    # Flop - tough fold
    Puzzle(player_hand="6c6h", board_cards="KcQs9d", pot_size=200, bet_to_call=100, player_chips_remaining=700, opponents=[Opponent(type="tight", chips_remaining=800)], current_player_to_act_index=0, question="Underpair to flop. Opponent bets half pot. Fold or call?"),
    # Turn - tough call
    Puzzle(player_hand="JsTs", board_cards="Qs9s8c2d", pot_size=320, bet_to_call=160, player_chips_remaining=800, opponents=[Opponent(type="standard", chips_remaining=600)], current_player_to_act_index=0, question="Flopped straight, turn bricks. Opponent bets half pot. Tough call or raise?"),
    # River - medium fold
    Puzzle(player_hand="7d7c", board_cards="QsKd9hJc3s", pot_size=400, bet_to_call=200, player_chips_remaining=600, opponents=[Opponent(type="tight", chips_remaining=700)], current_player_to_act_index=0, question="Your underpair is crushed. Opponent bets big on river. Fold or hero call?"),
]

random.shuffle(PUZZLES)