from treys import Card, Evaluator, Deck
import random

class GameAI:
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

    def get_recommendation(self, hole_cards, community_cards, position, stack_size, pot_size, num_players, opponent_actions, board_texture='neutral'):
        # Calculate hand strength
        hand_strength = self.get_hand_strength(hole_cards, community_cards)

        # Simple decision logic based on hand strength
        if hand_strength > 7:
            action = 'bet'
            amount = min(pot_size * 0.75, stack_size)
        elif hand_strength > 5:
            action = 'call'
            amount = 0
        elif hand_strength > 3:
            if random.random() < 0.3:  # 30% chance to bluff
                action = 'bet'
                amount = min(pot_size * 0.5, stack_size)
            else:
                action = 'fold'
                amount = 0
        else:
            if random.random() < 0.1:  # 10% chance to bluff
                action = 'bet'
                amount = min(pot_size * 0.5, stack_size)
            else:
                action = 'fold'
                amount = 0

        return {'action': action, 'amount': amount, 'hand_strength': hand_strength}

    def get_ai_action(self, hole_cards, community_cards, position, stack_size, pot_size, num_players, opponent_actions, board_texture='neutral'):
        """Get AI action for the bot to use"""
        rec = self.get_recommendation(hole_cards, community_cards, position, stack_size, pot_size, num_players, opponent_actions, board_texture)
        return rec 