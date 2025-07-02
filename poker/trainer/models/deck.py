from .card import Card
import random

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