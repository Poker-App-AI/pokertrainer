from treys import Card, Evaluator, Deck
import random

class PokerAI:
    def __init__(self):
        self.evaluator = Evaluator()
    def get_hand_strength(self, hole_cards, community_cards):
        """
        Returns hand strength:
        - Preflop: Chen formula (0-10)
        - Postflop: treys Evaluator (converted to 0-10)
        """

        if len(community_cards) == 0:
            # Preflop: Chen formula
            return self.chen_value(hole_cards[0], hole_cards[1])
        else:
            # Postflop: Evaluator score normalized
            hero_cards = [Card.new(hole_cards[0]), Card.new(hole_cards[1])]
            board = [Card.new(c) for c in community_cards]

            raw_score = self.evaluator.evaluate(board, hero_cards)
            # Evaluator scores: lower is better (1 = Royal Flush, 7462 = worst)
            # Normalize to 0-10 where 10 = best possible hand, 0 = worst
            normalized_strength = max(0, 10 - (raw_score / 7462 * 10))
            return round(normalized_strength, 2)

    def chen_value(self, card1, card2):
        # Your chen_value function here (simplified for brevity)
        rank_points = {
            'A': 10, 'K': 8, 'Q': 7, 'J': 6, 'T': 5,
            '9': 4.5, '8': 4, '7': 3.5, '6': 3, '5': 2.5,
            '4': 2, '3': 1.5, '2': 1
        }
        rank_order = '23456789TJQKA'

        r1, s1 = card1[0], card1[1]
        r2, s2 = card2[0], card2[1]

        high_card = r1 if rank_points[r1] >= rank_points[r2] else r2
        low_card = r2 if high_card == r1 else r1

        value = rank_points[high_card]

        if r1 == r2:
            value = max(value * 2, 5)
        else:
            if s1 == s2:
                value += 2

            gap = abs(rank_order.index(r1) - rank_order.index(r2)) - 1
            if gap == 1:
                value -= 1
            elif gap == 2:
                value -= 2
            elif gap == 3:
                value -= 4
            elif gap >= 4:
                penalty = 5
                if rank_order.index(high_card) < rank_order.index('Q'):
                    penalty /= 2
                value -= penalty

            if gap <= 1 and rank_order.index(r1) >= rank_order.index('8') and rank_order.index(r2) >= rank_order.index('8'):
                value += 1

        return max(value, 0)

    def calculate_equity(self, card1, card2, community_cards, num_opponents=1, num_simulations=500):
        hero_cards = [Card.new(card1), Card.new(card2)]
        community = [Card.new(c) for c in community_cards]

        wins = 0
        ties = 0

        for _ in range(num_simulations):
            deck = Deck()
            deck.cards = [c for c in deck.cards if c not in hero_cards + community]

            needed = 5 - len(community)
            sim_community = community + deck.draw(needed)

            villain_hands = []
            for _ in range(num_opponents):
                villain_hands.append([deck.draw(1)[0], deck.draw(1)[0]])

            hero_score = self.evaluator.evaluate(sim_community, hero_cards)
            villain_scores = [self.evaluator.evaluate(sim_community, hand) for hand in villain_hands]

            min_score = min([hero_score] + villain_scores)

            if hero_score == min_score:
                if villain_scores.count(min_score) > 0:
                    ties += 1
                else:
                    wins += 1

        equity = (wins + ties/2) / num_simulations
        return equity

    def position_strategy(self, position):
        if position == 'early':
            return {'bluff_freq': 0.05}
        elif position == 'middle':
            return {'bluff_freq': 0.1}
        elif position == 'late':
            return {'bluff_freq': 0.2}
        else:
            return {'bluff_freq': 0.05}

    def get_recommendation(self, hole_cards, community_cards, position, stack_size, pot_size, num_players, opponent_actions, board_texture='neutral'):
        # Calculate preflop hand strength
        hand_strength = self.chen_value(hole_cards[0], hole_cards[1])
        hand_strength = self.get_hand_strength(hole_cards, community_cards)

        # Calculate pot equity
        pot_equity = self.calculate_equity(hole_cards[0], hole_cards[1], community_cards, num_opponents=num_players-1)

        # Get position strategy
        strat = self.position_strategy(position)
        bluff_freq = strat['bluff_freq']

        # Decide to bluff or value bet
        action = 'fold'
        amount = 0

        # Simple decision logic:
        if pot_equity > 0.5:
            action = 'value bet'
            amount = min(pot_size * 0.75, stack_size)  # 75% pot bet
        else:
            # Decide to bluff based on frequency
            if random.random() < bluff_freq:
                action = 'bluff'
                amount = min(pot_size * random.uniform(0.5, 1.0), stack_size)
            else:
                action = 'check/fold'

        return {'action': action, 'amount': amount, 'pot_equity': pot_equity, 'hand_strength': hand_strength}

# Example usage
if __name__ == "__main__":
    ai = PokerAI()
    rec = ai.get_recommendation(
        hole_cards=['As', 'Ah'],
        community_cards=['Kd', 'Qh', '2s', 'Th'],
        position='late',
        stack_size=850,
        pot_size=500,
        num_players=1,
        opponent_actions=['check'],
        board_texture='dry'
    )
    print(rec)
