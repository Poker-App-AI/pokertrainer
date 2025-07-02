from poker.trainer.models import Card
from collections import Counter
from itertools import combinations

# --- Parsing functions ---
def parse_hand_string(hand_string):
    cards = []
    if len(hand_string) % 2 != 0:
        raise ValueError("Invalid hand string format.")
    for i in range(0, len(hand_string), 2):
        cards.append(Card(hand_string[i].upper(), hand_string[i+1].lower()))
    return cards

# --- Hand evaluation functions ---
def is_flush(cards):
    return len(set(card.suit_char for card in cards)) == 1

def is_straight(cards):
    values = sorted(set(card.rank_value for card in cards))
    if len(values) < 5:
        return False
    for i in range(len(values)-4):
        if values[i+4] - values[i] == 4:
            return True
    # Check for Ace-low straight
    if set([14,2,3,4,5]).issubset(set(values)):
        return True
    return False

def get_hand_rank_and_kickers(five_cards):
    ranks = sorted([c.rank_value for c in five_cards], reverse=True)
    count = Counter(ranks)
    is_st = is_straight(five_cards)
    is_fl = is_flush(five_cards)

    if is_st and is_fl:
        return (9, (max(ranks),), ())
    if 4 in count.values():
        quad = [r for r in count if count[r] == 4][0]
        kicker = max([r for r in ranks if r != quad])
        return (8, (quad,), (kicker,))
    if 3 in count.values() and 2 in count.values():
        trips = [r for r in count if count[r] == 3][0]
        pair = [r for r in count if count[r] == 2][0]
        return (7, (trips, pair), ())
    if is_fl:
        return (6, tuple(ranks), ())
    if is_st:
        return (5, (max(ranks),), ())
    if 3 in count.values():
        trips = [r for r in count if count[r] == 3][0]
        kickers = sorted([r for r in ranks if r != trips], reverse=True)
        return (4, (trips,), tuple(kickers))
    pairs = [r for r in count if count[r] == 2]
    if len(pairs) >= 2:
        high_pair, low_pair = sorted(pairs, reverse=True)[:2]
        kicker = max([r for r in ranks if r not in (high_pair, low_pair)])
        return (3, (high_pair, low_pair), (kicker,))
    if len(pairs) == 1:
        pair = pairs[0]
        kickers = sorted([r for r in ranks if r != pair], reverse=True)
        return (2, (pair,), tuple(kickers))
    return (1, tuple(ranks), ())

def get_best_hand_type(cards):
    hand_names = {
        9: 'Straight Flush', 8: 'Four of a Kind', 7: 'Full House',
        6: 'Flush', 5: 'Straight', 4: 'Three of a Kind',
        3: 'Two Pair', 2: 'Pair', 1: 'High Card'
    }
    best_rank = (0, (), ())
    for combo in combinations(cards, 5):
        rank = get_hand_rank_and_kickers(combo)
        if rank > best_rank:
            best_rank = rank
    return hand_names[best_rank[0]]

def get_hand_permutations(hand_string):
    """
    Converts a hand string (e.g., 'AKs', 'QQ', '72o') into all possible Card combinations.
    's' for suited, 'o' for offsuit, no suffix for pairs.
    """
    rank1_char = hand_string[0].upper()
    rank2_char = hand_string[1].upper()
    permutations = []

    if rank1_char == rank2_char: # Pair, e.g., 'QQ'
        ranks_same_suit_choices = [c for c in Card.SUITS.keys()]
        for i in range(len(ranks_same_suit_choices)):
            for j in range(i + 1, len(ranks_same_suit_choices)):
                s1 = ranks_same_suit_choices[i]
                s2 = ranks_same_suit_choices[j]
                try:
                    permutations.append(f"{rank1_char}{s1}{rank2_char}{s2}")
                except ValueError:
                    continue # Skip invalid card combos

    elif len(hand_string) == 2 or hand_string[2].lower() == 'o': # Offsuit, e.g., 'AK', '72o'
        for s1 in Card.SUITS.keys():
            for s2 in Card.SUITS.keys():
                if s1 != s2: # Must be different suits for offsuit
                    try:
                        permutations.append(f"{rank1_char}{s1}{rank2_char}{s2}")
                    except ValueError:
                        continue # Skip invalid card combos

    elif hand_string[2].lower() == 's': # Suited, e.g., 'AKs'
        for suit in Card.SUITS.keys():
            try:
                permutations.append(f"{rank1_char}{suit}{rank2_char}{suit}")
            except ValueError:
                continue # Skip invalid card combos
    return [parse_hand_string(p) for p in permutations] 