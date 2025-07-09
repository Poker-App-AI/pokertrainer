from treys import Card, Deck
import random
import sys

class HeadsUpPoker:
    def __init__(self):
        self.deck = Deck()
        self.player_stack = 1000
        self.ai_stack = 1000
        self.pot = 0
        self.community_cards = []
        self.player_cards = []
        self.ai_cards = []
        self.game_ai = None
        self.player_first = True  # Track who goes first
        
    def deal_cards(self):
        """Deal hole cards to both players"""
        self.deck = Deck()
        self.player_cards = [Card.int_to_str(self.deck.draw(1)[0]) for _ in range(2)]
        self.ai_cards = [Card.int_to_str(self.deck.draw(1)[0]) for _ in range(2)]
        self.community_cards = []
        
    def deal_community(self, num_cards):
        """Deal community cards"""
        for _ in range(num_cards):
            self.community_cards.append(Card.int_to_str(self.deck.draw(1)[0]))
            
    def get_user_action(self, current_bet=0):
        """Get action from user"""
        print(f"\nYour cards: {self.player_cards}")
        print(f"Community cards: {self.community_cards}")
        print(f"Your stack: ${self.player_stack}")
        print(f"AI stack: ${self.ai_stack}")
        print(f"Pot: ${self.pot}")
        if current_bet > 0:
            print(f"Current bet to call: ${current_bet}")
            
        while True:
            if current_bet == 0:
                action = input("\nYour action (fold/check/bet): ").lower().strip()
            else:
                action = input("\nYour action (fold/call/bet): ").lower().strip()
            
            if action == 'fold':
                return {'action': 'fold', 'amount': 0}
            elif action == 'check':
                if current_bet > 0:
                    print("Cannot check when there's a bet to call!")
                    continue
                return {'action': 'check', 'amount': 0}
            elif action == 'call':
                if current_bet == 0:
                    print("No bet to call. Choose bet or check.")
                    continue
                if current_bet > self.player_stack:
                    print("Not enough chips to call!")
                    continue
                return {'action': 'call', 'amount': current_bet}
            elif action == 'bet':
                try:
                    amount = int(input("Bet amount: $"))
                    if amount > self.player_stack:
                        print("Not enough chips!")
                        continue
                    if amount <= 0:
                        print("Bet must be positive!")
                        continue
                    return {'action': 'bet', 'amount': amount}
                except ValueError:
                    print("Please enter a valid number!")
                    continue
            else:
                if current_bet == 0:
                    print("Invalid action! Choose fold, check, or bet.")
                else:
                    print("Invalid action! Choose fold, call, or bet.")
                
    def get_ai_action(self, current_bet=0):
        """Get action from AI"""
        # Simple AI logic
        hand_strength = self.game_ai.get_hand_strength(self.ai_cards, self.community_cards)
        
        if hand_strength > 7:
            action = 'bet'
            amount = min(50, self.ai_stack)
        elif hand_strength > 5:
            if current_bet == 0:
                action = 'check'
                amount = 0
            else:
                action = 'call'
                amount = current_bet
        elif hand_strength > 3:
            if random.random() < 0.3:  # 30% chance to bluff
                action = 'bet'
                amount = min(30, self.ai_stack)
            else:
                if current_bet == 0:
                    action = 'check'
                    amount = 0
                else:
                    action = 'fold'
                    amount = 0
        else:
            if random.random() < 0.1:  # 10% chance to bluff
                action = 'bet'
                amount = min(20, self.ai_stack)
            else:
                if current_bet == 0:
                    action = 'check'
                    amount = 0
                else:
                    action = 'fold'
                    amount = 0
                
        return {'action': action, 'amount': amount}
    
    def determine_winner(self):
        """Determine winner at showdown"""
        from treys import Evaluator
        evaluator = Evaluator()
        
        player_cards_int = [Card.new(c) for c in self.player_cards]
        ai_cards_int = [Card.new(c) for c in self.ai_cards]
        community_int = [Card.new(c) for c in self.community_cards]
        
        player_score = evaluator.evaluate(community_int, player_cards_int)
        ai_score = evaluator.evaluate(community_int, ai_cards_int)
        
        # Lower score is better in treys
        if player_score < ai_score:
            return 'player'
        elif ai_score < player_score:
            return 'ai'
        else:
            return 'tie'
    
    def play_hand(self):
        """Play one complete hand"""
        print("\n" + "="*50)
        print("NEW HAND")
        print("="*50)
        
        # Deal cards
        self.deal_cards()
        print(f"Your cards: {self.player_cards}")
        print(f"{'You go first' if self.player_first else 'AI goes first'}")
        
        # Preflop betting
        print("\n--- PREFLOP ---")
        current_bet = 0
        
        if self.player_first:
            # Player acts first
            player_action = self.get_user_action(current_bet)
            if player_action['action'] == 'bet':
                current_bet = player_action['amount']
                self.player_stack -= player_action['amount']
                self.pot += player_action['amount']
                print(f"You bet ${player_action['amount']}")
            elif player_action['action'] == 'fold':
                print("You fold. AI wins the pot!")
                self.ai_stack += self.pot
                self.pot = 0
                self.player_first = not self.player_first  # Switch for next hand
                return 'ai'
            elif player_action['action'] == 'check':
                print("You check")
                
            # AI responds
            ai_action = self.get_ai_action(current_bet)
            if ai_action['action'] == 'fold':
                print(f"AI folds. You win the pot!")
                self.player_stack += self.pot
                self.pot = 0
                self.player_first = not self.player_first  # Switch for next hand
                return 'player'
            elif ai_action['action'] == 'call':
                if current_bet > 0:
                    self.ai_stack -= current_bet
                    self.pot += current_bet
                    print(f"AI calls ${current_bet}")
                else:
                    print("AI checks")
            elif ai_action['action'] == 'bet':
                self.ai_stack -= ai_action['amount']
                self.pot += ai_action['amount']
                current_bet = ai_action['amount']
                print(f"AI bets ${ai_action['amount']}")
                
                # Player must respond to AI bet
                player_action = self.get_user_action(current_bet)
                if player_action['action'] == 'fold':
                    print("You fold. AI wins the pot!")
                    self.ai_stack += self.pot
                    self.pot = 0
                    self.player_first = not self.player_first  # Switch for next hand
                    return 'ai'
                elif player_action['action'] == 'call':
                    self.player_stack -= current_bet
                    self.pot += current_bet
                    print(f"You call ${current_bet}")
                elif player_action['action'] == 'bet':
                    self.player_stack -= player_action['amount']
                    self.pot += player_action['amount']
                    print(f"You bet ${player_action['amount']}")
        else:
            # AI acts first
            ai_action = self.get_ai_action(current_bet)
            if ai_action['action'] == 'fold':
                print(f"AI folds. You win the pot!")
                self.player_stack += self.pot
                self.pot = 0
                self.player_first = not self.player_first  # Switch for next hand
                return 'player'
            elif ai_action['action'] == 'call':
                if current_bet > 0:
                    self.ai_stack -= current_bet
                    self.pot += current_bet
                    print(f"AI calls ${current_bet}")
                else:
                    print("AI checks")
            elif ai_action['action'] == 'bet':
                self.ai_stack -= ai_action['amount']
                self.pot += ai_action['amount']
                current_bet = ai_action['amount']
                print(f"AI bets ${ai_action['amount']}")
                
            # Player responds
            player_action = self.get_user_action(current_bet)
            if player_action['action'] == 'fold':
                print("You fold. AI wins the pot!")
                self.ai_stack += self.pot
                self.pot = 0
                self.player_first = not self.player_first  # Switch for next hand
                return 'ai'
            elif player_action['action'] == 'call':
                if current_bet > 0:
                    self.player_stack -= current_bet
                    self.pot += current_bet
                    print(f"You call ${current_bet}")
            elif player_action['action'] == 'bet':
                self.player_stack -= player_action['amount']
                self.pot += player_action['amount']
                print(f"You bet ${player_action['amount']}")
            elif player_action['action'] == 'check':
                print("You check")
        
        # Deal flop
        print("\n--- FLOP ---")
        self.deal_community(3)
        print(f"Community cards: {self.community_cards}")
        
        # Flop betting (simplified - just one round)
        current_bet = 0
        if self.player_first:
            player_action = self.get_user_action(current_bet)
            if player_action['action'] == 'fold':
                print("You fold. AI wins the pot!")
                self.ai_stack += self.pot
                self.pot = 0
                self.player_first = not self.player_first  # Switch for next hand
                return 'ai'
            elif player_action['action'] == 'bet':
                current_bet = player_action['amount']
                self.player_stack -= player_action['amount']
                self.pot += player_action['amount']
                print(f"You bet ${player_action['amount']}")
            elif player_action['action'] == 'check':
                print("You check")
                
            ai_action = self.get_ai_action(current_bet)
            if ai_action['action'] == 'fold':
                print(f"AI folds. You win the pot!")
                self.player_stack += self.pot
                self.pot = 0
                self.player_first = not self.player_first  # Switch for next hand
                return 'player'
            elif ai_action['action'] == 'call':
                if current_bet > 0:
                    self.ai_stack -= current_bet
                    self.pot += current_bet
                    print(f"AI calls ${current_bet}")
                else:
                    print("AI checks")
            elif ai_action['action'] == 'bet':
                self.ai_stack -= ai_action['amount']
                self.pot += ai_action['amount']
                current_bet = ai_action['amount']
                print(f"AI bets ${ai_action['amount']}")
                
                player_action = self.get_user_action(current_bet)
                if player_action['action'] == 'fold':
                    print("You fold. AI wins the pot!")
                    self.ai_stack += self.pot
                    self.pot = 0
                    self.player_first = not self.player_first  # Switch for next hand
                    return 'ai'
                elif player_action['action'] == 'call':
                    self.player_stack -= current_bet
                    self.pot += current_bet
                    print(f"You call ${current_bet}")
        else:
            ai_action = self.get_ai_action(current_bet)
            if ai_action['action'] == 'fold':
                print(f"AI folds. You win the pot!")
                self.player_stack += self.pot
                self.pot = 0
                self.player_first = not self.player_first  # Switch for next hand
                return 'player'
            elif ai_action['action'] == 'call':
                if current_bet > 0:
                    self.ai_stack -= current_bet
                    self.pot += current_bet
                    print(f"AI calls ${current_bet}")
                else:
                    print("AI checks")
            elif ai_action['action'] == 'bet':
                self.ai_stack -= ai_action['amount']
                self.pot += ai_action['amount']
                current_bet = ai_action['amount']
                print(f"AI bets ${ai_action['amount']}")
                
            player_action = self.get_user_action(current_bet)
            if player_action['action'] == 'fold':
                print("You fold. AI wins the pot!")
                self.ai_stack += self.pot
                self.pot = 0
                self.player_first = not self.player_first  # Switch for next hand
                return 'ai'
            elif player_action['action'] == 'call':
                if current_bet > 0:
                    self.player_stack -= current_bet
                    self.pot += current_bet
                    print(f"You call ${current_bet}")
            elif player_action['action'] == 'check':
                print("You check")
        
        # Deal turn and river
        print("\n--- TURN ---")
        self.deal_community(1)
        print(f"Community cards: {self.community_cards}")
        
        print("\n--- RIVER ---")
        self.deal_community(1)
        print(f"Community cards: {self.community_cards}")
        
        # Showdown
        print("\n--- SHOWDOWN ---")
        print(f"Your cards: {self.player_cards}")
        print(f"AI cards: {self.ai_cards}")
        print(f"Community cards: {self.community_cards}")
        
        winner = self.determine_winner()
        if winner == 'player':
            print("You win the pot!")
            self.player_stack += self.pot
        elif winner == 'ai':
            print("AI wins the pot!")
            self.ai_stack += self.pot
        else:
            print("It's a tie! Pot is split.")
            self.player_stack += self.pot // 2
            self.ai_stack += self.pot // 2
            
        self.pot = 0
        self.player_first = not self.player_first  # Switch for next hand
        return winner
    
    def play_game(self):
        """Play 10 hands"""
        print("Welcome to Heads-Up Poker!")
        print("You'll play 10 hands against the AI.")
        print("Starting stacks: $1000 each")
        
        player_wins = 0
        ai_wins = 0
        
        for hand in range(1, 11):
            print(f"\nHand {hand}/10")
            winner = self.play_hand()
            
            if winner == 'player':
                player_wins += 1
            elif winner == 'ai':
                ai_wins += 1
                
            print(f"\nCurrent score - You: {player_wins}, AI: {ai_wins}")
            print(f"Current stacks - You: ${self.player_stack}, AI: ${self.ai_stack}")
            
            if hand < 10:
                input("\nPress Enter to continue to next hand...")
        
        # Final results
        print("\n" + "="*50)
        print("GAME OVER")
        print("="*50)
        print(f"Final score - You: {player_wins}, AI: {ai_wins}")
        print(f"Final stacks - You: ${self.player_stack}, AI: ${self.ai_stack}")
        
        if player_wins > ai_wins:
            print("Congratulations! You won the match!")
        elif ai_wins > player_wins:
            print("AI won the match!")
        else:
            print("It's a tie!")

if __name__ == "__main__":
    # Import the GameAI
    sys.path.append('.')
    from poker.trainer.game_ai import GameAI
    
    game = HeadsUpPoker()
    game.game_ai = GameAI()
    game.play_game() 