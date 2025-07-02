# poker_engine.py

import random
from collections import Counter
from itertools import combinations

# --- Card and Deck classes ---

class Card:
    SUITS = {'h': 'Hearts', 'd': 'Diamonds', 'c': 'Clubs', 's': 'Spades'}
    RANKS = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
    }

    def __init__(self, rank_char, suit_char):
        if rank_char not in self.RANKS:
            raise ValueError(f"Invalid rank character: {rank_char}")
        if suit_char not in self.SUITS:
            raise ValueError(f"Invalid suit character: {suit_char}")
        self.rank_char = rank_char
        self.suit_char = suit_char
        self.rank_value = self.RANKS[rank_char]

    def __str__(self):
        return f"{self.rank_char}{self.suit_char}"

    def __eq__(self, other):
        return isinstance(other, Card) and self.rank_char == other.rank_char and self.suit_char == other.suit_char

    def __hash__(self):
        return hash((self.rank_char, self.suit_char))

class Deck:
    def __init__(self):
        self.cards = [Card(r, s) for s in Card.SUITS for r in Card.RANKS]
        random.shuffle(self.cards)

    def deal(self, num_cards):
        if num_cards > len(self.cards):
            raise ValueError("Not enough cards in the deck to deal.")
        dealt = self.cards[:num_cards]
        self.cards = self.cards[num_cards:]
        return dealt

    def remove_cards(self, cards_to_remove):
        for card in cards_to_remove:
            if card in self.cards:
                self.cards.remove(card)

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
    from itertools import combinations
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

# --- Opponent ranges (simplified) ---

PREPROCESSED_OPPONENT_RANGES = {
    'tight': [[Card('A','s'), Card('A','h')], [Card('K','s'), Card('K','h')], [Card('Q','s'), Card('Q','h')]],
    'standard': [[Card('A','s'), Card('K','h')], [Card('Q','s'), Card('J','h')], [Card('T','s'), Card('T','h')]],
    'loose': [[Card('7','s'), Card('2','h')], [Card('9','s'), Card('4','h')], [Card('J','s'), Card('8','h')]]
}

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
            if PREPROCESSED_OPPONENT_RANGES[op_type]:
                hand = random.choice(PREPROCESSED_OPPONENT_RANGES[op_type])
                if hand[0] in deck.cards and hand[1] in deck.cards:
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
