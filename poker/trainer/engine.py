# poker/engine.py

import random
from poker.trainer.models import Card, Deck
from poker.trainer.utils import (
    parse_hand_string, get_hand_rank_and_kickers, get_hand_permutations
)

# --- Opponent ranges (simplified) ---
OPPONENT_RANGES = {
    'tight': [
        'AA', 'KK', 'QQ', 'JJ', 'AKs', 'AKo', 'AQs', 'AQo'
    ],
    'standard': [
        'AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88',
        'AKs', 'AQs', 'AJs', 'ATs', 'KQs', 'KJs', 'QTs',
        'AKo', 'AQo', 'KQo', 'KJo'
    ],
    'loose': [
        'AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77', '66', '55', '44', '33', '22',
        'AKs', 'AQs', 'AJs', 'ATs', 'A9s', 'A8s', 'A7s', 'A6s', 'A5s', 'A4s', 'A3s', 'A2s',
        'KQs', 'KJs', 'KTs', 'K9s', 'K8s', 'K7s', 'K6s', 'K5s', 'K4s', 'K3s', 'K2s',
        'QJs', 'QTs', 'Q9s', 'Q8s', 'Q7s',
        'JTs', 'J9s', 'J8s',
        'T9s', 'T8s',
        '98s', '97s',
        '87s', '86s',
        '76s', '75s',
        '65s', '64s',
        '54s',
        'AKo', 'AQo', 'AJo', 'ATo', 'KQo', 'KJo', 'QJo', 'JTo', 'T9o', '98o', '87o', '76o', '65o', '54o',
        # This is still a simplified loose range, real ranges are vast!
    ]
}

# Pre-process ranges into actual Card objects for efficiency later
PREPROCESSED_OPPONENT_RANGES = {}
for player_type, hand_strings in OPPONENT_RANGES.items():
    all_possible_hands_for_type = []
    for hs in hand_strings:
        all_possible_hands_for_type.extend(get_hand_permutations(hs))
    PREPROCESSED_OPPONENT_RANGES[player_type] = all_possible_hands_for_type

# --- Main equity calculation function ---


def calculate_multi_way_equity(player_hand_str, board_cards_str="", opponent_types=[], num_simulations=1000):
    player_hand = parse_hand_string(player_hand_str)
    board_cards = parse_hand_string(board_cards_str)
    player_win = tie = opponent_win = 0

    for _ in range(num_simulations):
        deck = Deck()
        deck.remove_cards(player_hand + board_cards)

        opp_hands = []
        for op_type in opponent_types:
            available_hands = [h for h in PREPROCESSED_OPPONENT_RANGES[op_type]
                               if h[0] in deck.cards and h[1] in deck.cards]
            if available_hands:
                hand = random.choice(available_hands)
                opp_hands.append(hand)
                deck.remove_cards(hand)
            else:
                opp_hands.append(deck.deal(2))

        community = board_cards + deck.deal(5 - len(board_cards))
        player_final = player_hand + community
        player_rank = get_hand_rank_and_kickers(player_final)

        opp_ranks = []
        for hand in opp_hands:
            opp_final = hand + community
            opp_ranks.append(get_hand_rank_and_kickers(opp_final))

        all_ranks = [player_rank] + opp_ranks
        best = max(all_ranks)

        if all_ranks.count(best) > 1:
            tie += 1
        elif best == player_rank:
            player_win += 1
        else:
            opponent_win += 1

    total = player_win + tie + opponent_win
    return {
        "player_win_percentage": player_win / total * 100,
        "tie_percentage": tie / total * 100,
        "opponent_win_percentage": opponent_win / total * 100,
    }