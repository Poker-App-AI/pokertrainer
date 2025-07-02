import random
from collections import Counter
from itertools import combinations

class Card:
    """Represents a playing card."""
    SUITS = {'h': 'Hearts', 'd': 'Diamonds', 'c': 'Clubs', 's': 'Spades'}
    RANKS = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
    }
    RANK_CHARS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

    def __init__(self, rank_char, suit_char):
        """
        Initializes a Card object.
        Args:
            rank_char (str): The character representing the card's rank (e.g., 'K', 'A', '7').
            suit_char (str): The character representing the card's suit (e.g., 'h', 'c').
        Raises:
            ValueError: If an invalid rank or suit character is provided.
        """
        if rank_char not in self.RANKS:
            raise ValueError(f"Invalid rank character: {rank_char}")
        if suit_char not in self.SUITS:
            raise ValueError(f"Invalid suit character: {suit_char}")

        self.rank_char = rank_char
        self.suit_char = suit_char
        self.rank_value = self.RANKS[rank_char] # Numerical value for comparison

    def __str__(self):
        """Returns a string representation of the card (e.g., 'Kh')."""
        return f"{self.rank_char}{self.suit_char}"

    def __repr__(self):
        """Returns a developer-friendly representation."""
        return f"Card('{self.rank_char}', '{self.suit_char}')"

    def __eq__(self, other):
        """Checks if two cards are equal."""
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank_char == other.rank_char and self.suit_char == other.suit_char

    def __hash__(self):
        """Enables Card objects to be used in sets/dictionaries."""
        return hash((self.rank_char, self.suit_char))

class Deck:
    """Represents a standard 52-card deck."""
    def __init__(self):
        """Initializes a new, shuffled deck."""
        self.cards = [Card(r, s) for s in Card.SUITS.keys() for r in Card.RANKS.keys()]
        random.shuffle(self.cards)

    def deal(self, num_cards):
        """
        Deals a specified number of cards from the top of the deck.
        Args:
            num_cards (int): The number of cards to deal.
        Returns:
            list: A list of dealt Card objects.
        Raises:
            ValueError: If not enough cards in the deck.
        """
        if num_cards > len(self.cards):
            raise ValueError("Not enough cards in the deck to deal.")
        dealt_cards = self.cards[:num_cards]
        self.cards = self.cards[num_cards:]
        return dealt_cards

    def remove_cards(self, cards_to_remove):
        """
        Removes specified cards from the deck.
        Useful for setting up known cards (player hand, board cards).
        Args:
            cards_to_remove (list): A list of Card objects to remove.
        """
        for card_to_remove in cards_to_remove:
            # Only remove if the card is actually in the deck to avoid errors
            if card_to_remove in self.cards:
                self.cards.remove(card_to_remove)

def parse_hand_string(hand_string):
    """
    Parses a string like 'KhJc' or 'AsTs5h' into a list of Card objects.
    Args:
        hand_string (str): The string representation of cards.
    Returns:
        list: A list of Card objects.
    Raises:
        ValueError: If the string format is invalid.
    """
    cards = []
    # A single card is two characters (e.g., 'Ks')
    if len(hand_string) % 2 != 0:
        raise ValueError("Invalid hand string format. Expected pairs of rank-suit, e.g., 'KhJc'.")

    for i in range(0, len(hand_string), 2):
        rank_char = hand_string[i].upper()
        suit_char = hand_string[i+1].lower()
        cards.append(Card(rank_char, suit_char))
    return cards

def is_flush(cards):
    """
    Checks if a list of 5 cards forms a flush.
    Args:
        cards (list): A list of 5 Card objects.
    Returns:
        bool: True if it's a flush, False otherwise.
    """
    if len(cards) != 5:
        return False
    first_suit = cards[0].suit_char
    return all(card.suit_char == first_suit for card in cards)

def is_straight(cards):
    """
    Checks if a list of 5 cards forms a straight.
    Handles Ace-low straight (A, 2, 3, 4, 5).
    Args:
        cards (list): A list of 5 Card objects.
    Returns:
        bool: True if it's a straight, False otherwise.
    """
    if len(cards) != 5:
        return False
    values = sorted([card.rank_value for card in cards])

    # Check for Ace-low straight (A, 2, 3, 4, 5) - Ace value 14, but acts as 1 here
    if set(values) == {14, 2, 3, 4, 5}:
        return True

    # Check for regular straight (sequential values)
    return all(values[i] + 1 == values[i+1] for i in range(4))

def get_hand_rank_and_kickers(five_cards):
    """
    Evaluates a 5-card hand and returns its type and kickers for comparison.
    This function is crucial for determining the best hand among multiple 5-card combinations.
    The return format allows direct tuple comparison to find the superior hand.

    Returns:
        tuple: (hand_rank_value, primary_kickers_tuple, secondary_kickers_tuple)
        Hand rank values (higher is better):
        9: Straight Flush
        8: Four of a Kind
        7: Full House
        6: Flush
        5: Straight
        4: Three of a Kind
        3: Two Pair
        2: One Pair
        1: High Card
    """
    ranks = sorted([card.rank_value for card in five_cards], reverse=True) # Sorted for kickers
    rank_counts = Counter(ranks) # Counts of each rank

    is_fl = is_flush(five_cards)
    is_st = is_straight(five_cards)

    # Special handling for Ace-low straight for consistent ranking comparison
    if is_st and set(ranks) == {14, 2, 3, 4, 5}:
        # Treat A,2,3,4,5 as 5,4,3,2,1 for comparison purposes
        sorted_ranks_for_comparison = [5, 4, 3, 2, 1]
    else:
        sorted_ranks_for_comparison = ranks # Already sorted descending

    # Evaluate hands in descending order of strength

    # Straight Flush
    if is_st and is_fl:
        return (9, (sorted_ranks_for_comparison[0],), ()) # Top card of straight

    # Four of a Kind
    if 4 in rank_counts.values():
        quad_rank = [r for r, count in rank_counts.items() if count == 4][0]
        kicker = [r for r in ranks if r != quad_rank][0] # The single remaining card
        return (8, (quad_rank,), (kicker,))

    # Full House
    if 3 in rank_counts.values() and 2 in rank_counts.values():
        trips_rank = [r for r, count in rank_counts.items() if count == 3][0]
        pair_rank = [r for r, count in rank_counts.items() if count == 2][0]
        return (7, (trips_rank, pair_rank), ())

    # Flush
    if is_fl:
        return (6, tuple(sorted_ranks_for_comparison), ()) # All 5 cards as kickers

    # Straight
    if is_st:
        return (5, (sorted_ranks_for_comparison[0],), ()) # Top card of straight

    # Three of a Kind
    if 3 in rank_counts.values():
        trips_rank = [r for r, count in rank_counts.items() if count == 3][0]
        kickers = sorted([r for r in ranks if r != trips_rank], reverse=True)
        return (4, (trips_rank,), tuple(kickers))

    # Two Pair
    pairs = sorted([r for r, count in rank_counts.items() if count == 2], reverse=True)
    if len(pairs) == 2:
        kicker = [r for r in ranks if r not in pairs][0] # The single remaining card
        return (3, tuple(pairs), (kicker,))

    # One Pair
    if 2 in rank_counts.values():
        pair_rank = [r for r, count in rank_counts.items() if count == 2][0]
        kickers = sorted([r for r in ranks if r != pair_rank], reverse=True)
        return (2, (pair_rank,), tuple(kickers))

    # High Card
    return (1, tuple(sorted_ranks_for_comparison), ()) # All 5 cards as kickers

def get_best_hand_type(community_and_hole_cards):
    """
    Given a list of 5, 6, or 7 cards (player's hand + community cards),
    this function finds the best possible 5-card poker hand.
    Args:
        community_and_hole_cards (list): A list of Card objects.
    Returns:
        str: The string name of the best hand found (e.g., 'Flush', 'Pair').
    """
    if len(community_and_hole_cards) < 5:
        return "Not enough cards to form a hand"

    # Generate all possible 5-card combinations from the given cards
    all_five_card_combinations = list(combinations(community_and_hole_cards, 5))

    # Initialize with the lowest possible hand rank
    best_hand_info = (0, (), ()) # (rank_value, primary_kickers, secondary_kickers)

    hand_names = {
        9: 'Straight Flush', 8: 'Four of a Kind', 7: 'Full House',
        6: 'Flush', 5: 'Straight', 4: 'Three of a Kind',
        3: 'Two Pair', 2: 'Pair', 1: 'High Card'
    }

    # Iterate through all 5-card combinations to find the best one
    for combo in all_five_card_combinations:
        current_hand_info = get_hand_rank_and_kickers(list(combo))
        if current_hand_info > best_hand_info: # Tuple comparison works as desired
            best_hand_info = current_hand_info

    # Return the name of the best hand found
    return hand_names.get(best_hand_info[0], "High Card")

def calculate_odds(player_hand_str, board_cards_str="", num_simulations=10000):
    """
    Calculates the odds of getting various poker hands through Monte Carlo simulation.
    Args:
        player_hand_str (str): String representation of the player's two hole cards (e.g., 'KhJc').
        board_cards_str (str, optional): String representation of community cards (e.g., 'AsTs5h').
                                         Empty string for pre-flop. Defaults to "".
        num_simulations (int, optional): The number of simulations to run. Defaults to 10000.
    Returns:
        dict: A dictionary where keys are hand names and values are their
              estimated probabilities as percentages.
    Raises:
        ValueError: If inputs are invalid (e.g., wrong number of cards, duplicate cards).
    """
    player_hand = parse_hand_string(player_hand_str)
    board_cards = parse_hand_string(board_cards_str)

    # Input validation
    if len(player_hand) != 2:
        raise ValueError("Player hand must consist of exactly two cards.")
    # Check for duplicates between player hand and board cards
    all_known_cards = player_hand + board_cards
    if len(set(all_known_cards)) != len(all_known_cards):
        raise ValueError("Duplicate cards detected in player hand or board cards. Please ensure all known cards are unique.")

    hand_counts = Counter() # To store counts of each hand type encountered

    for _ in range(num_simulations):
        deck = Deck() # Create a fresh deck for each simulation
        deck.remove_cards(player_hand) # Remove player's hole cards
        deck.remove_cards(board_cards) # Remove known board cards

        community_cards = list(board_cards) # Start with existing board cards

        # Determine how many more community cards need to be dealt to reach 5
        # Pre-flop: need 5 cards (Flop 3, Turn 1, River 1)
        # Flop: need 2 cards (Turn 1, River 1)
        # Turn: need 1 card (River 1)
        cards_to_deal_for_river = 5 - len(board_cards)
        if cards_to_deal_for_river > 0:
            community_cards.extend(deck.deal(cards_to_deal_for_river))

        combined_cards = player_hand + community_cards
        best_hand = get_best_hand_type(combined_cards)
        hand_counts[best_hand] += 1

    results = {}
    total_hands_evaluated = sum(hand_counts.values())
    if total_hands_evaluated == 0:
        return {"Error": "No simulations run. Check input or simulation count."}

    # Define the order of hands for consistent output
    hand_order = [
        'Straight Flush', 'Four of a Kind', 'Full House', 'Flush',
        'Straight', 'Three of a Kind', 'Two Pair', 'Pair', 'High Card'
    ]

    for hand_type in hand_order:
        # Calculate percentage; use 0.0 if a hand type was not encountered
        results[hand_type] = (hand_counts[hand_type] / total_hands_evaluated) * 100

    return results

preflop_odds = calculate_odds('KhJc', "")
print("--- Pre-flop Odds (KhJc) ---")
for hand, odds in preflop_odds.items():
    print(f"{hand}: {odds:.2f}%")

# Example 2: Odds given a flop (e.g., Kh Jc on As Ts 5h flop)
flop_odds = calculate_odds('KhJc', 'AsTs5h')
print("\n--- Flop Odds (KhJc on AsTs5h) ---")
for hand, odds in flop_odds.items():
    print(f"{hand}: {odds:.2f}%")

# Example 3: Odds given a turn (e.g., Kh Jc on As Ts 5h 7d board)
turn_odds = calculate_odds('KhJc', 'AsTs5h7d')
print("\n--- Turn Odds (KhJc on AsTs5h7d) ---")
for hand, odds in turn_odds.items():
    print(f"{hand}: {odds:.2f}%")