from dataclasses import dataclass
from typing import List

@dataclass
class Opponent:
    type: str
    chips_remaining: int

@dataclass
class Puzzle:
    player_hand: str
    board_cards: str
    pot_size: int
    bet_to_call: int
    player_chips_remaining: int
    opponents: List[Opponent]
    current_player_to_act_index: int
    question: str 