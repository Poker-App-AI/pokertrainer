from collections import defaultdict

regret_sum = defaultdict(lambda: [0.0, 0.0, 0.0]) # fold, call, raise
strategy_sum = defaultdict(lambda: [0.0, 0.0, 0.0])
class PokerState:
    def __init__(self, hole_cards, board_cards, pot, stacks, betting_history, terminal=False, utility=0):
        self.hole_cards = hole_cards
        self.board_cards = board_cards
        self.pot = pot
        self.stacks = stacks
        self.betting_history = betting_history
        self.terminal = terminal
        self.utility = utility

    def is_terminal(self):
        # Returns True if the hand is over (fold or showdown)
        return self.terminal

    def get_utility(self, player):
        # Returns chips won/lost for player at terminal state
        return self.utility

    def get_infoset_key(self, player):
        # Returns bucketed infoset key for this player in this state
        hole_bucket = bucket_hole_cards(self.hole_cards[player])
        board_bucket = bucket_board(self.board_cards)
        return (hole_bucket, board_bucket, tuple(self.betting_history))

    def next_state(self, action):
        # Returns next PokerState after taking `action`
        # Update pot, stacks, betting history, terminal/utility if action ends the hand
        new_history = self.betting_history + [action]
        # Simplified: Always returns terminal with +1 utility for 'raise'
        return PokerState(
            hole_cards=self.hole_cards,
            board_cards=self.board_cards,
            pot=self.pot + 1,
            stacks=self.stacks,
            betting_history=new_history,
            terminal=True,
            utility=1 if action == 'raise' else -1
        )
def bucket_hole_cards(hole_cards):
    # Simplified: return 'high', 'medium', or 'low' based on highest card rank
    ranks = [card.rank_value for card in hole_cards]
    if max(ranks) >= 12: # Q,K,A
        return 'high'
    elif max(ranks) >= 9: # 9,J,T
        return 'medium'
    else:
        return 'low'

def bucket_board(board_cards):
    # Simplified: return 'dry' or 'wet' flop
    suits = [card.suit_char for card in board_cards]
    if len(set(suits)) == 3:
        return 'dry'
    else:
        return 'wet'


def get_strategy(infoset, regret_sum):
    regrets = regret_sum[infoset]
    positive_regrets = [r if r > 0 else 0 for r in regrets]
    normalizing_sum = sum(positive_regrets)
    if normalizing_sum > 0:
        return [r / normalizing_sum for r in positive_regrets]
    else:
        return [1.0/3, 1.0/3, 1.0/3] # uniform strategy if no positive regrets

def cfr(state, player, probability):
    if state.is_terminal():
        return state.get_utility(player)

    infoset = state.get_infoset_key(player)
    strategy = get_strategy(infoset, regret_sum)
    util = [0.0, 0.0, 0.0]
    node_util = 0.0

    for a in range(3):
        next_state = state.next_state(a)
        util[a] = cfr(next_state, player, probability * strategy[a])
        node_util += strategy[a] * util[a]

    # Regret update
    for a in range(3):
        regret_sum[infoset][a] += probability * (util[a] - node_util)

    # Strategy sum update
    for a in range(3):
        strategy_sum[infoset][a] += probability * strategy[a]

    return node_util

# Initialize mock state

class Card:
    RANKS = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
        '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
    }
    SUITS = {'h', 'd', 'c', 's'}

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

    def __repr__(self):
        return f"Card('{self.rank_char}', '{self.suit_char}')"

    def __eq__(self, other):
        return self.rank_char == other.rank_char and self.suit_char == other.suit_char

    def __hash__(self):
        return hash((self.rank_char, self.suit_char))

import random

class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for rank in Card.RANKS.keys() for suit in Card.SUITS]
        random.shuffle(self.cards)

    def deal(self, num_cards):
        if num_cards > len(self.cards):
            raise ValueError("Not enough cards left in the deck")
        dealt = self.cards[:num_cards]
        self.cards = self.cards[num_cards:]
        return dealt

    def remove_cards(self, cards_to_remove):
        for card in cards_to_remove:
            if card in self.cards:
                self.cards.remove(card)

# Example test cases
print(bucket_hole_cards([Card('A','s'), Card('Q','h')]))  # should print 'high'
print(bucket_hole_cards([Card('T','s'), Card('9','h')]))  # should print 'medium'
print(bucket_hole_cards([Card('7','s'), Card('4','h')]))  # should print 'low'

print(bucket_board([Card('K','s'), Card('7','h'), Card('2','c')])) # 'dry'
print(bucket_board([Card('J','h'), Card('8','h'), Card('2','c')])) # 'wet'

# Create card objects
card1 = Card('A', 's')
card2 = Card('K', 'h')
print(card1, card2)  # Output: As Kh

# Create and shuffle deck
deck = Deck()
print(deck.deal(2))  # Deal 2 cards
state = PokerState(
    hole_cards = {0: [Card('A','s'), Card('Q','h')], 1: [Card('K','s'), Card('J','h')]},
    board_cards = [Card('K','c'), Card('7','h'), Card('2','d')],
    pot = 10,
    stacks = {0: 90, 1: 90},
    betting_history = [],
    terminal = False,
    utility = 0
)

print(state.get_infoset_key(0))  # should show ('high', 'dry', ())

next_state = state.next_state('raise')
print(next_state.pot)            # should be 11
print(next_state.terminal)       # should be True
print(next_state.utility)        # +1 if raise in simplified next_state logic

initial_state = PokerState(
    hole_cards = {0: [Card('A','s'), Card('Q','h')], 1: [Card('K','s'), Card('J','h')]},
    board_cards = [Card('K','c'), Card('7','h'), Card('2','d')],
    pot = 10,
    stacks = {0: 90, 1: 90},
    betting_history = [],
    terminal = False,
    utility = 0
)

# Run CFR iterations
for i in range(10):
    cfr(initial_state, player=0, probability=1)
    cfr(initial_state, player=1, probability=1)

print("Regret Sum:", dict(regret_sum))
print("Strategy Sum:", dict(strategy_sum))
