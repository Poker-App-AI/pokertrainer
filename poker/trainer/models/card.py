

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