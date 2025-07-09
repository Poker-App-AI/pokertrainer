import random

class PokerBot:
    def __init__(self, name="Bot"):
        self.name = name

    def get_action(self, hole_cards, community_cards, position, stack_size, pot_size, num_players, opponent_actions, board_texture='neutral'):
        # Simple average bot: random between call/check and fold, with a slight bias to call/check
        if random.random() < 0.7:
            return {'action': 'call', 'amount': 0}
        else:
            return {'action': 'fold', 'amount': 0} 