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

# Helper function to convert a hand string like 'AKs' to its card permutations
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


# Example ranges (you'd expand these significantly for a full trainer)
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
        # Not enough cards to form a 5-card hand, return a placeholder or raise error
        # For simulation purposes, 'High Card' is a reasonable default if less than 5 cards.
        # However, for the purpose of getting a final hand, it's an error.
        raise ValueError("Not enough cards to form a 5-card hand.")


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

def calculate_odds_vs_opponent(player_hand_str, board_cards_str="", opponent_type='standard', num_simulations=10000):
    """
    Calculates the odds of the player winning, tying, or losing against an opponent
    whose hand is drawn from a pre-defined range. Also calculates player's specific
    hand odds.

    Args:
        player_hand_str (str): String representation of the player's two hole cards (e.g., 'KhJc').
        board_cards_str (str, optional): String representation of community cards (e.g., 'AsTs5h').
                                         Empty string for pre-flop. Defaults to "".
        opponent_type (str, optional): The type of opponent ('tight', 'standard', 'loose'). Defaults to 'standard'.
        num_simulations (int, optional): The number of simulations to run. Defaults to 10000.
    Returns:
        dict: A dictionary containing:
              - "player_win_percentage": Player's probability of winning.
              - "tie_percentage": Probability of a tie.
              - "opponent_win_percentage": Opponent's probability of winning.
              - "player_specific_hand_odds": Dictionary of player's specific hand type probabilities.
    Raises:
        ValueError: If inputs are invalid (e.g., wrong number of cards, duplicate cards, unknown opponent type).
    """
    player_hand = parse_hand_string(player_hand_str)
    board_cards = parse_hand_string(board_cards_str)

    if len(player_hand) != 2:
        raise ValueError("Player hand must consist of exactly two cards.")
    
    all_known_cards = player_hand + board_cards
    if len(set(all_known_cards)) != len(all_known_cards):
        raise ValueError("Duplicate cards detected in player hand or board cards. Please ensure all known cards are unique.")

    if opponent_type not in PREPROCESSED_OPPONENT_RANGES:
        raise ValueError(f"Unknown opponent type: '{opponent_type}'. Choose from {list(PREPROCESSED_OPPONENT_RANGES.keys())}")

    opponent_range_hands = PREPROCESSED_OPPONENT_RANGES[opponent_type]

    player_win_count = 0
    tie_count = 0
    opponent_win_count = 0
    
    player_hand_type_counts = Counter() # To store counts of each hand type encountered for the player

    for _ in range(num_simulations):
        deck = Deck()
        deck.remove_cards(player_hand)
        deck.remove_cards(board_cards)

        # --- Deal Opponent's Hand from Range ---
        # Find all hands in the opponent's range that are still available in the current deck
        available_opponent_hands_for_sim = []
        for op_hand_pair in opponent_range_hands: # op_hand_pair is a list of two Card objects like [Card('A','s'), Card('K','s')]
            card1, card2 = op_hand_pair[0], op_hand_pair[1]
            if card1 in deck.cards and card2 in deck.cards:
                available_opponent_hands_for_sim.append(op_hand_pair)
        
        opponent_hand = None
        if not available_opponent_hands_for_sim:
            # This should ideally not happen if ranges are sensible and deck large enough.
            # As a fallback: if no hands from opponent's range are available (e.g., opponent's entire range
            # consists of cards already on the board or in player's hand), deal a random hand.
            # In a very realistic trainer, you might just skip this simulation or warn.
            # For now, just deal random 2 cards from remaining deck.
            if len(deck.cards) >= 2:
                opponent_hand = deck.deal(2)
            else:
                # Not enough cards even for a random hand, skip this simulation
                continue 
        else:
            opponent_hand = random.choice(available_opponent_hands_for_sim)
        
        # Remove opponent's dealt hand from the deck for this specific simulation run
        deck.remove_cards(opponent_hand)

        # --- Deal Community Cards ---
        community_cards = list(board_cards) # Start with existing board cards
        cards_to_deal_for_river = 5 - len(board_cards) # How many more cards needed to reach a 5-card board
        
        if cards_to_deal_for_river > len(deck.cards):
            # Not enough cards left in the deck to complete the board, skip this simulation
            continue

        if cards_to_deal_for_river > 0:
            community_cards.extend(deck.deal(cards_to_deal_for_river))

        # --- Evaluate Hands and Determine Winner ---
        player_final_cards = player_hand + community_cards
        opponent_final_cards = opponent_hand + community_cards

        try:
            player_best_hand_info = get_hand_rank_and_kickers(player_final_cards)
            opponent_best_hand_info = get_hand_rank_and_kickers(opponent_final_cards)
        except ValueError:
            # This can happen if, somehow, there aren't enough cards to form a 5-card hand
            # after dealing due to previous errors or very specific edge cases.
            continue # Skip this simulation if a valid 5-card hand can't be formed

        # --- Track Player's Hand Type Odds (original functionality) ---
        # Note: This tracks what *your* final hand *would be*, not necessarily if you win.
        player_hand_type_counts[get_best_hand_type(player_final_cards)] += 1

        # --- Determine the winner of the hand ---
        if player_best_hand_info > opponent_best_hand_info:
            player_win_count += 1
        elif opponent_best_hand_info > player_best_hand_info:
            opponent_win_count += 1
        else:
            tie_count += 1

    total_simulations = num_simulations # This should match the loop count unless 'continue' was hit often.

    if total_simulations == 0: # Safety check if all simulations were skipped
         return {
            "player_win_percentage": 0.0,
            "tie_percentage": 0.0,
            "opponent_win_percentage": 0.0,
            "player_specific_hand_odds": {ht: 0.0 for ht in ['Straight Flush', 'Four of a Kind', 'Full House', 'Flush', 'Straight', 'Three of a Kind', 'Two Pair', 'Pair', 'High Card']}
        }


    # Calculate percentages for winning, tying, losing
    player_win_percentage = (player_win_count / total_simulations) * 100
    tie_percentage = (tie_count / total_simulations) * 100
    opponent_win_percentage = (opponent_win_count / total_simulations) * 100

    # Calculate percentages for player's specific hand types
    player_specific_hand_odds = {}
    hand_order = [
        'Straight Flush', 'Four of a Kind', 'Full House', 'Flush',
        'Straight', 'Three of a Kind', 'Two Pair', 'Pair', 'High Card'
    ]
    for hand_type in hand_order:
        player_specific_hand_odds[hand_type] = (player_hand_type_counts[hand_type] / total_simulations) * 100

    return {
        "player_win_percentage": player_win_percentage,
        "tie_percentage": tie_percentage,
        "opponent_win_percentage": opponent_win_percentage,
        "player_specific_hand_odds": player_specific_hand_odds
    }


def calculate_multi_way_equity(player_hand_str, board_cards_str="", opponent_types=[], num_simulations=10000):
    """
    Calculates the equity (win/tie/loss percentage) for the player in a multi-way pot
    against opponents drawing from specified hand ranges.

    Args:
        player_hand_str (str): String representation of the player's two hole cards (e.g., 'KhJc').
        board_cards_str (str, optional): String representation of community cards (e.g., 'AsTs5h').
                                         Empty string for pre-flop. Defaults to "".
        opponent_types (list): A list of strings, each representing an opponent's type
                               ('tight', 'standard', 'loose'). Empty list for heads-up.
        num_simulations (int, optional): The number of simulations to run. Defaults to 10000.
    Returns:
        dict: A dictionary containing:
              - "player_win_percentage": Player's probability of winning.
              - "tie_percentage": Probability of a tie.
              - "opponent_win_percentage": Player's probability of losing (an opponent wins).
              - "player_specific_hand_odds": Dictionary of player's specific hand type probabilities.
              - "opponent_equity_breakdown": (Optional) Breakdown of equity per opponent.
    Raises:
        ValueError: If inputs are invalid (e.g., wrong number of cards, duplicate cards, unknown opponent type).
    """
    player_hand = parse_hand_string(player_hand_str)
    board_cards = parse_hand_string(board_cards_str)

    if len(player_hand) != 2:
        raise ValueError("Player hand must consist of exactly two cards.")
    
    all_known_cards = player_hand + board_cards
    if len(set(all_known_cards)) != len(all_known_cards):
        raise ValueError("Duplicate cards detected in player hand or board cards. Please ensure all known cards are unique.")

    # Validate opponent types
    for op_type in opponent_types:
        if op_type not in PREPROCESSED_OPPONENT_RANGES:
            raise ValueError(f"Unknown opponent type: '{op_type}'. Choose from {list(PREPROCESSED_OPPONENT_RANGES.keys())}")

    player_win_count = 0
    tie_count = 0
    opponent_win_count = 0 # This means player loses, some opponent wins
    
    player_hand_type_counts = Counter() # To store counts of each hand type encountered for the player

    # Keep track of individual opponent wins for optional breakdown
    individual_opponent_win_counts = Counter({i: 0 for i in range(len(opponent_types))})

    for sim_idx in range(num_simulations):
        deck = Deck()
        deck.remove_cards(player_hand)
        deck.remove_cards(board_cards)

        # --- Deal Opponent Hands from Ranges ---
        current_sim_opponent_hands = []
        for i, op_type in enumerate(opponent_types):
            opponent_range_hands = PREPROCESSED_OPPONENT_RANGES[op_type]
            
            available_hands_for_this_opponent = []
            for op_hand_pair in opponent_range_hands:
                card1, card2 = op_hand_pair[0], op_hand_pair[1]
                # Check if these specific cards are still in the deck AND not already dealt to other opponents
                if card1 in deck.cards and card2 in deck.cards and \
                   card1 not in [c for h in current_sim_opponent_hands for c in h] and \
                   card2 not in [c for h in current_sim_opponent_hands for c in h]:
                    available_hands_for_this_opponent.append(op_hand_pair)
            
            if not available_hands_for_this_opponent:
                # If no hands from range are available, deal random from remaining deck
                # This can happen if ranges are too narrow or many players.
                if len(deck.cards) >= 2:
                    dealt_hand = deck.deal(2)
                else:
                    # Not enough cards for this opponent, skip this simulation
                    continue # This will skip the rest of the current simulation iteration
            else:
                dealt_hand = random.choice(available_hands_for_this_opponent)
            
            current_sim_opponent_hands.append(dealt_hand)
            deck.remove_cards(dealt_hand) # Remove dealt hand from deck for subsequent deals

        # If we skipped due to not enough cards for an opponent, continue to next simulation
        if len(current_sim_opponent_hands) != len(opponent_types):
            continue

        # --- Deal Community Cards ---
        community_cards = list(board_cards)
        cards_to_deal_for_river = 5 - len(board_cards)
        
        if cards_to_deal_for_river > len(deck.cards):
            # Not enough cards left in the deck to complete the board, skip this simulation
            continue

        if cards_to_deal_for_river > 0:
            community_cards.extend(deck.deal(cards_to_deal_for_river))

        # --- Evaluate All Hands ---
        player_final_cards = player_hand + community_cards
        
        try:
            player_best_hand_info = get_hand_rank_and_kickers(player_final_cards)
        except ValueError:
            # Not enough cards to form a 5-card hand for player, skip simulation
            continue

        opponent_final_hand_infos = []
        for op_hand in current_sim_opponent_hands:
            try:
                opponent_final_hand_infos.append(get_hand_rank_and_kickers(op_hand + community_cards))
            except ValueError:
                # Not enough cards to form a 5-card hand for opponent, treat as a loss for them in this context
                # Or, more robustly, skip this simulation. For simplicity, we'll mark as lowest possible hand.
                opponent_final_hand_infos.append((0, (), ())) # Lowest possible hand rank

        # --- Determine Winner(s) ---
        # Find the best hand among all players (including player and all opponents)
        all_hand_infos = [player_best_hand_info] + opponent_final_hand_infos
        
        # Check if any hand info is invalid (e.g., from skipped opponent deal)
        if any(h[0] == 0 and h != (0,(),()) for h in all_hand_infos): # If any hand info is the "error" tuple
            continue # Skip this simulation if any hand couldn't be evaluated properly

        max_hand_info = max(all_hand_infos)

        is_player_winner = (player_best_hand_info == max_hand_info)
        
        # Check for ties among winning hands
        num_winners = all_hand_infos.count(max_hand_info)

        if is_player_winner:
            if num_winners > 1:
                tie_count += 1
            else:
                player_win_count += 1
        else:
            opponent_win_count += 1
            # Optional: track which opponent won
            for i, op_info in enumerate(opponent_final_hand_infos):
                if op_info == max_hand_info:
                    individual_opponent_win_counts[i] += 1
        
        # --- Track Player's Hand Type Odds (original functionality) ---
        player_hand_type_counts[get_best_hand_type(player_final_cards)] += 1

    total_successful_simulations = player_win_count + tie_count + opponent_win_count

    if total_successful_simulations == 0:
         return {
            "player_win_percentage": 0.0,
            "tie_percentage": 0.0,
            "opponent_win_percentage": 0.0,
            "player_specific_hand_odds": {ht: 0.0 for ht in ['Straight Flush', 'Four of a Kind', 'Full House', 'Flush', 'Straight', 'Three of a Kind', 'Two Pair', 'Pair', 'High Card']},
            "opponent_equity_breakdown": {f"Opponent {i+1} ({opponent_types[i]})": 0.0 for i in range(len(opponent_types))}
        }

    # Calculate percentages for winning, tying, losing
    player_win_percentage = (player_win_count / total_successful_simulations) * 100
    tie_percentage = (tie_count / total_successful_simulations) * 100
    opponent_win_percentage = (opponent_win_count / total_successful_simulations) * 100

    # Calculate percentages for player's specific hand types
    player_specific_hand_odds = {}
    hand_order = [
        'Straight Flush', 'Four of a Kind', 'Full House', 'Flush',
        'Straight', 'Three of a Kind', 'Two Pair', 'Pair', 'High Card'
    ]
    for hand_type in hand_order:
        player_specific_hand_odds[hand_type] = (player_hand_type_counts[hand_type] / total_successful_simulations) * 100

    # Calculate individual opponent equity breakdown
    opponent_equity_breakdown = {}
    for i, op_type in enumerate(opponent_types):
        opponent_equity_breakdown[f"Opponent {i+1} ({op_type})"] = (individual_opponent_win_counts[i] / total_successful_simulations) * 100


    return {
        "player_win_percentage": player_win_percentage,
        "tie_percentage": tie_percentage,
        "opponent_win_percentage": opponent_win_percentage,
        "player_specific_hand_odds": player_specific_hand_odds,
        "opponent_equity_breakdown": opponent_equity_breakdown
    }



# Example 1: Pre-flop odds (e.g., for Kh Jc) against a 'standard' opponent
result_preflop = calculate_odds_vs_opponent('KhJc', "", opponent_type='standard')
print("--- Pre-flop Odds (KhJc vs Standard Opponent) ---")
print(f"Player Win %: {result_preflop['player_win_percentage']:.2f}%")
print(f"Tie %: {result_preflop['tie_percentage']:.2f}%")
print(f"Opponent Win %: {result_preflop['opponent_win_percentage']:.2f}%")
print("\nPlayer's Specific Hand Odds:")
for hand, odds in result_preflop['player_specific_hand_odds'].items():
    print(f"  {hand}: {odds:.2f}%")

# Example 2: Odds given a flop (e.g., Kh Jc on As Ts 5h flop) against a 'tight' opponent
result_flop = calculate_odds_vs_opponent('KhJc', 'AsTs5h', opponent_type='tight')
print("\n--- Flop Odds (KhJc on AsTs5h vs Tight Opponent) ---")
print(f"Player Win %: {result_flop['player_win_percentage']:.2f}%")
print(f"Tie %: {result_flop['tie_percentage']:.2f}%")
print(f"Opponent Win %: {result_flop['opponent_win_percentage']:.2f}%")
print("\nPlayer's Specific Hand Odds:")
for hand, odds in result_flop['player_specific_hand_odds'].items():
    print(f"  {hand}: {odds:.2f}%")

# Example 3: Odds given a turn (e.g., Kh Jc on As Ts 5h 7d board) against a 'loose' opponent
result_turn = calculate_odds_vs_opponent('KhJc', 'AsTs5h7d', opponent_type='loose')
print("\n--- Turn Odds (KhJc on AsTs5h7d vs Loose Opponent) ---")
print(f"Player Win %: {result_turn['player_win_percentage']:.2f}%")
print(f"Tie %: {result_turn['tie_percentage']:.2f}%")
print(f"Opponent Win %: {result_turn['opponent_win_percentage']:.2f}%")
print("\nPlayer's Specific Hand Odds:")
for hand, odds in result_turn['player_specific_hand_odds'].items():
    print(f"  {hand}: {odds:.2f}%")




# Example 1: 3-way hand (you vs. a 'standard' and a 'tight' opponent) pre-flop
result_3way_preflop = calculate_multi_way_equity(
    player_hand_str='AsKs',
    board_cards_str="",
    opponent_types=['standard', 'tight'],
    num_simulations=5000 # Reduced for quicker example
)
print("--- 3-way Pre-flop (AsKs vs Standard, Tight) ---")
print(f"Player Win %: {result_3way_preflop['player_win_percentage']:.2f}%")
print(f"Tie %: {result_3way_preflop['tie_percentage']:.2f}%")
print(f"Opponent Win % (Player Loses): {result_3way_preflop['opponent_win_percentage']:.2f}%")
print("\nPlayer's Specific Hand Odds:")
for hand, odds in result_3way_preflop['player_specific_hand_odds'].items():
    print(f"  {hand}: {odds:.2f}%")
print("\nOpponent Equity Breakdown:")
for op, equity in result_3way_preflop['opponent_equity_breakdown'].items():
    print(f"  {op} Win %: {equity:.2f}%")


# Example 2: 4-way hand on the flop
result_4way_flop = calculate_multi_way_equity(
    player_hand_str='7h8h',
    board_cards_str='5h6h9c', # Flush draw, straight draw
    opponent_types=['loose', 'standard', 'tight'], # You vs 3 opponents
    num_simulations=5000
)
print("\n--- 4-way Flop (7h8h on 5h6h9c vs Loose, Standard, Tight) ---")
print(f"Player Win %: {result_4way_flop['player_win_percentage']:.2f}%")
print(f"Tie %: {result_4way_flop['tie_percentage']:.2f}%")
print(f"Opponent Win % (Player Loses): {result_4way_flop['opponent_win_percentage']:.2f}%")
print("\nPlayer's Specific Hand Odds:")
for hand, odds in result_4way_flop['player_specific_hand_odds'].items():
    print(f"  {hand}: {odds:.2f}%")
print("\nOpponent Equity Breakdown:")
for op, equity in result_4way_flop['opponent_equity_breakdown'].items():
    print(f"  {op} Win %: {equity:.2f}%")

puzzle_state = {
    "player_hand": "KhJc",
    "board_cards": "AsTs5h",
    "pot_size": 100, # Current pot before your action
    "bet_to_call": 20, # Amount you need to put in to call
    "player_chips_remaining": 500,
    "opponents": [
        {"type": "standard", "chips_remaining": 400},
        {"type": "tight", "chips_remaining": 600}
    ],
    "current_player_to_act_index": 0, # Assuming player is index 0
    "question": "What should you do?"
}

def run_poker_puzzle(puzzle_state):
    print("🃏 Poker Puzzle 🃏")
    print("Your hand:", puzzle_state["player_hand"])
    print("Board cards:", puzzle_state["board_cards"])
    print("Pot size:", puzzle_state["pot_size"])
    print("Bet to call:", puzzle_state["bet_to_call"])
    print("Your remaining chips:", puzzle_state["player_chips_remaining"])
    print("Opponents:")
    for i, op in enumerate(puzzle_state["opponents"]):
        print(f"  Opponent {i+1}: Type = {op['type']}, Chips = {op['chips_remaining']}")

    # ✅ Show the user the puzzle question clearly
    print("\nQuestion:", puzzle_state["question"])
    
    user_answer = input("Your action (fold, call, raise): ").strip().lower()

    opponent_types = [op["type"] for op in puzzle_state["opponents"]]

    equity_result = calculate_multi_way_equity(
        puzzle_state["player_hand"],
        puzzle_state["board_cards"],
        opponent_types,
        num_simulations=10000
    )

    pot_odds_percentage = (puzzle_state["bet_to_call"] / (puzzle_state["pot_size"] + puzzle_state["bet_to_call"])) * 100
    player_equity = equity_result["player_win_percentage"] + equity_result["tie_percentage"] / 2

    if player_equity > pot_odds_percentage + 15:
        correct_action = "raise"
    elif player_equity > pot_odds_percentage:
        correct_action = "call"
    else:
        correct_action = "fold"

    print("\n--- Result ---")
    if user_answer == correct_action:
        print("✅ Correct! Your action is optimal here.")
    else:
        print(f"❌ Incorrect. The correct action was: {correct_action.upper()}.")

    print("\n--- Equity Breakdown ---")
    print(f"Your equity (win + tie/2): {player_equity:.2f}%")
    print(f"Pot odds required: {pot_odds_percentage:.2f}%")
    print("Full equity result:")
    print(equity_result)

# To run:
run_poker_puzzle(puzzle_state)
