import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Alert,
  ScrollView,
  TextInput,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';

interface Card {
  rank: string;
  suit: string;
}

interface GameState {
  playerCards: Card[];
  aiCards: Card[];
  communityCards: Card[];
  playerStack: number;
  aiStack: number;
  pot: number;
  currentBet: number;
  playerFirst: boolean;
  gamePhase: 'preflop' | 'flop' | 'turn' | 'river' | 'showdown';
  handNumber: number;
  playerWins: number;
  aiWins: number;
  isPlayerTurn: boolean;
  lastAction: string;
  showAICards: boolean;
}

const HeadsUpScreen: React.FC = () => {
  const navigation = useNavigation();
  const [gameState, setGameState] = useState<GameState>({
    playerCards: [],
    aiCards: [],
    communityCards: [],
    playerStack: 1000,
    aiStack: 1000,
    pot: 0,
    currentBet: 0,
    playerFirst: true,
    gamePhase: 'preflop',
    handNumber: 1,
    playerWins: 0,
    aiWins: 0,
    isPlayerTurn: true,
    lastAction: '',
    showAICards: false,
  });

  const [betAmount, setBetAmount] = useState('');

  const suits = ['♠', '♥', '♦', '♣'];
  const ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'];

  const dealCards = () => {
    const deck = [...Array(52)].map((_, i) => ({
      rank: ranks[i % 13],
      suit: suits[Math.floor(i / 13)],
    }));
    
    // Shuffle deck
    for (let i = deck.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [deck[i], deck[j]] = [deck[j], deck[i]];
    }

    const playerCards = [deck[0], deck[1]];
    const aiCards = [deck[2], deck[3]];

    setGameState(prev => ({
      ...prev,
      playerCards,
      aiCards,
      communityCards: [],
      pot: 0,
      currentBet: 0,
      gamePhase: 'preflop',
      isPlayerTurn: prev.playerFirst,
      lastAction: '',
      showAICards: false,
    }));
  };

  const dealCommunityCards = (count: number) => {
    setGameState(prev => {
      const newCommunityCards = [...prev.communityCards];
      for (let i = 0; i < count; i++) {
        newCommunityCards.push({
          rank: ranks[Math.floor(Math.random() * ranks.length)],
          suit: suits[Math.floor(Math.random() * suits.length)],
        });
      }
      return {
        ...prev,
        communityCards: newCommunityCards,
        currentBet: 0,
        isPlayerTurn: prev.playerFirst,
      };
    });
  };

  const getHandStrength = (cards: Card[], community: Card[]) => {
    // Simplified hand strength calculation
    if (community.length === 0) {
      // Preflop: simple calculation based on card ranks
      const values = cards.map(card => ranks.indexOf(card.rank));
      return Math.max(...values) + Math.min(...values) / 10;
    } else {
      // Postflop: more complex calculation
      const allCards = [...cards, ...community];
      const values = allCards.map(card => ranks.indexOf(card.rank));
      return values.reduce((sum, val) => sum + val, 0) / allCards.length;
    }
  };

  const aiAction = () => {
    const aiCards = gameState.aiCards;
    const community = gameState.communityCards;
    const handStrength = getHandStrength(aiCards, community);
    const currentBet = gameState.currentBet;

    let action = 'check';
    let amount = 0;

    if (handStrength > 7) {
      action = 'bet';
      amount = Math.min(75, gameState.aiStack);
    } else if (handStrength > 6) {
      action = 'bet';
      amount = Math.min(50, gameState.aiStack);
    } else if (handStrength > 5) {
      if (currentBet === 0) {
        if (Math.random() < 0.6) {
          action = 'bet';
          amount = Math.min(30, gameState.aiStack);
        } else {
          action = 'check';
        }
      } else {
        action = 'call';
        amount = currentBet;
      }
    } else if (handStrength > 3) {
      if (Math.random() < 0.4) {
        action = 'bet';
        amount = Math.min(25, gameState.aiStack);
      } else {
        if (currentBet === 0) {
          action = 'check';
        } else {
          action = 'fold';
        }
      }
    } else {
      if (Math.random() < 0.2) {
        action = 'bet';
        amount = Math.min(15, gameState.aiStack);
      } else {
        if (currentBet === 0) {
          action = 'check';
        } else {
          action = 'fold';
        }
      }
    }

    executeAction(action, amount, 'ai');
  };

  // Auto-start AI action if it goes first (only at the start of a new hand)
  useEffect(() => {
    if (!gameState.isPlayerTurn && gameState.gamePhase === 'preflop' && !gameState.playerFirst) {
      setTimeout(() => {
        aiAction();
      }, 1000);
    }
  }, [gameState.isPlayerTurn, gameState.gamePhase, gameState.playerFirst]);

  // Debug: Log state changes
  useEffect(() => {
    console.log('Game State:', {
      phase: gameState.gamePhase,
      isPlayerTurn: gameState.isPlayerTurn,
      currentBet: gameState.currentBet,
      playerFirst: gameState.playerFirst
    });
  }, [gameState.gamePhase, gameState.isPlayerTurn, gameState.currentBet, gameState.playerFirst]);

  const executeAction = (action: string, amount: number, player: 'player' | 'ai') => {
    setGameState(prev => {
      let newState = { ...prev };
      
             if (action === 'fold') {
         const winner = player === 'player' ? 'ai' : 'player';
         if (winner === 'player') {
           newState.playerStack += prev.pot;
           newState.playerWins += 1;
         } else {
           newState.aiStack += prev.pot;
           newState.aiWins += 1;
         }
         newState.pot = 0;
         newState.lastAction = `${player === 'player' ? 'You' : 'AI'} fold`;
         
         // Show AI cards briefly, then start next hand
         setTimeout(() => {
           setGameState(prev => ({
             ...prev,
             handNumber: prev.handNumber + 1,
             playerFirst: !prev.playerFirst,
             gamePhase: 'preflop',
             communityCards: [],
             pot: 0,
             currentBet: 0,
             isPlayerTurn: !prev.playerFirst,
             lastAction: '',
             showAICards: false,
           }));
           dealCards();
         }, 3000);
         
         return newState;
       }
      
      if (action === 'bet') {
        if (player === 'player') {
          newState.playerStack -= amount;
          newState.currentBet = amount;
        } else {
          newState.aiStack -= amount;
          newState.currentBet = amount;
        }
        newState.pot += amount;
        newState.lastAction = `${player === 'player' ? 'You' : 'AI'} bet $${amount}`;
      } else if (action === 'call') {
        if (player === 'player') {
          newState.playerStack -= amount;
        } else {
          newState.aiStack -= amount;
        }
        newState.pot += amount;
        newState.currentBet = 0;
        newState.lastAction = `${player === 'player' ? 'You' : 'AI'} call $${amount}`;
      } else if (action === 'check') {
        newState.currentBet = 0;
        newState.lastAction = `${player === 'player' ? 'You' : 'AI'} check`;
      }
      
      newState.isPlayerTurn = !prev.isPlayerTurn;
      
      // If both players have acted (no current bet and not player's turn), move to next phase
      // But only if we're not in showdown
      if (newState.currentBet === 0 && !newState.isPlayerTurn && newState.gamePhase !== 'showdown') {
         if (newState.gamePhase === 'preflop') {
           newState.gamePhase = 'flop';
           // Deal flop cards
           const newCommunityCards = [];
           for (let i = 0; i < 3; i++) {
             newCommunityCards.push({
               rank: ranks[Math.floor(Math.random() * ranks.length)],
               suit: suits[Math.floor(Math.random() * suits.length)],
             });
           }
           newState.communityCards = newCommunityCards;
           newState.isPlayerTurn = newState.playerFirst;
           
           // If AI goes first on flop, trigger AI action
           if (!newState.isPlayerTurn) {
             setTimeout(() => {
               aiAction();
             }, 500);
           }
         } else if (newState.gamePhase === 'flop') {
           newState.gamePhase = 'turn';
           // Deal turn card
           newState.communityCards.push({
             rank: ranks[Math.floor(Math.random() * ranks.length)],
             suit: suits[Math.floor(Math.random() * suits.length)],
           });
           newState.isPlayerTurn = newState.playerFirst;
           
           // If AI goes first on turn, trigger AI action
           if (!newState.isPlayerTurn) {
             setTimeout(() => {
               aiAction();
             }, 500);
           }
         } else if (newState.gamePhase === 'turn') {
           newState.gamePhase = 'river';
           // Deal river card
           newState.communityCards.push({
             rank: ranks[Math.floor(Math.random() * ranks.length)],
             suit: suits[Math.floor(Math.random() * suits.length)],
           });
           newState.isPlayerTurn = newState.playerFirst;
           
           // If AI goes first on river, trigger AI action
           if (!newState.isPlayerTurn) {
             setTimeout(() => {
               aiAction();
             }, 500);
           }
         } else if (newState.gamePhase === 'river') {
           newState.gamePhase = 'showdown';
           newState.showAICards = true;
           // Determine winner
           const playerStrength = getHandStrength(newState.playerCards, newState.communityCards);
           const aiStrength = getHandStrength(newState.aiCards, newState.communityCards);
           
           if (playerStrength > aiStrength) {
             newState.playerStack += newState.pot;
             newState.playerWins += 1;
             newState.lastAction = 'You win!';
           } else if (aiStrength > playerStrength) {
             newState.aiStack += newState.pot;
             newState.aiWins += 1;
             newState.lastAction = 'AI wins!';
           } else {
             newState.playerStack += newState.pot / 2;
             newState.aiStack += newState.pot / 2;
             newState.lastAction = 'Tie!';
           }
           
           newState.pot = 0;
           
           // Show AI cards briefly, then start next hand
           setTimeout(() => {
             setGameState(prev => ({
               ...prev,
               handNumber: prev.handNumber + 1,
               playerFirst: !prev.playerFirst,
               gamePhase: 'preflop',
               communityCards: [],
               pot: 0,
               currentBet: 0,
               isPlayerTurn: !prev.playerFirst,
               lastAction: '',
               showAICards: false,
             }));
             dealCards();
           }, 3000);
         }
       }
      
      return newState;
    });
  };

  const handlePlayerAction = (action: string) => {
    if (!gameState.isPlayerTurn) return;
    
    let amount = 0;
    
    if (action === 'bet') {
      const betValue = parseInt(betAmount);
      if (isNaN(betValue) || betValue <= 0 || betValue > gameState.playerStack) {
        Alert.alert('Invalid bet amount');
        return;
      }
      amount = betValue;
      setBetAmount('');
    } else if (action === 'call') {
      amount = gameState.currentBet;
    }
    
    executeAction(action, amount, 'player');
    
    // AI responds after a short delay, but only if there's a bet to call
    if (action !== 'fold' && amount > 0) {
      setTimeout(() => {
        aiAction();
      }, 1000);
    }
  };

  useEffect(() => {
    dealCards();
  }, []);

  const renderCard = (card: Card, hidden: boolean = false) => (
    <View style={[styles.card, hidden && styles.hiddenCard]}>
      <Text style={[styles.cardText, card.suit === '♥' || card.suit === '♦' ? styles.redCard : styles.blackCard]}>
        {hidden ? '?' : `${card.rank}${card.suit}`}
      </Text>
    </View>
  );

  return (
    <ScrollView style={styles.container}>
      <View style={styles.table}>
        {/* Game info */}
        <View style={styles.gameInfo}>
          <Text style={styles.handNumber}>Hand {gameState.handNumber}/10</Text>
          <Text style={styles.score}>You: {gameState.playerWins} | AI: {gameState.aiWins}</Text>
          <Text style={styles.phase}>{gameState.gamePhase.toUpperCase()}</Text>
        </View>

        {/* AI area */}
        <View style={styles.aiArea}>
          <Text style={styles.playerLabel}>AI</Text>
          <View style={styles.stackInfo}>
            <Text style={styles.stackText}>Stack: ${gameState.aiStack}</Text>
          </View>
          <View style={styles.cardsContainer}>
            {gameState.aiCards.map((card, index) => renderCard(card, !gameState.showAICards))}
          </View>
        </View>

        {/* Community cards */}
        <View style={styles.communityArea}>
          <Text style={styles.communityLabel}>Community Cards</Text>
          <View style={styles.cardsContainer}>
            {gameState.communityCards.map((card, index) => renderCard(card))}
          </View>
        </View>

        {/* Pot */}
        <View style={styles.potArea}>
          <Text style={styles.potText}>Pot: ${gameState.pot}</Text>
          {gameState.currentBet > 0 && (
            <Text style={styles.betText}>Bet to call: ${gameState.currentBet}</Text>
          )}
        </View>

        {/* Player area */}
        <View style={styles.playerArea}>
          <Text style={styles.playerLabel}>You</Text>
          <View style={styles.stackInfo}>
            <Text style={styles.stackText}>Stack: ${gameState.playerStack}</Text>
          </View>
          <View style={styles.cardsContainer}>
            {gameState.playerCards.map((card, index) => renderCard(card))}
          </View>
        </View>

        {/* Action buttons */}
        {gameState.isPlayerTurn && gameState.gamePhase !== 'showdown' && (
          <View style={styles.actionArea}>
            <Text style={styles.turnText}>Your turn</Text>
            <View style={styles.buttonRow}>
              <TouchableOpacity
                style={styles.actionButton}
                onPress={() => handlePlayerAction('fold')}
              >
                <Text style={styles.buttonText}>Fold</Text>
              </TouchableOpacity>
              
              {gameState.currentBet === 0 ? (
                <TouchableOpacity
                  style={styles.actionButton}
                  onPress={() => handlePlayerAction('check')}
                >
                  <Text style={styles.buttonText}>Check</Text>
                </TouchableOpacity>
              ) : (
                <TouchableOpacity
                  style={[styles.actionButton, gameState.currentBet > gameState.playerStack && styles.disabledButton]}
                  onPress={() => handlePlayerAction('call')}
                  disabled={gameState.currentBet > gameState.playerStack}
                >
                  <Text style={styles.buttonText}>Call ${gameState.currentBet}</Text>
                </TouchableOpacity>
              )}
              
              <TouchableOpacity
                style={styles.actionButton}
                onPress={() => handlePlayerAction('bet')}
              >
                <Text style={styles.buttonText}>Bet</Text>
              </TouchableOpacity>
            </View>
            
                         {gameState.currentBet === 0 && (
               <View style={styles.betInput}>
                 <Text style={styles.betLabel}>Bet amount:</Text>
                 <TextInput
                   style={styles.input}
                   value={betAmount}
                   onChangeText={setBetAmount}
                   placeholder="Enter amount"
                   keyboardType="numeric"
                 />
               </View>
             )}
          </View>
        )}

        {/* Last action */}
        {gameState.lastAction && (
          <View style={styles.lastAction}>
            <Text style={styles.lastActionText}>{gameState.lastAction}</Text>
          </View>
        )}

        {/* Game over */}
        {gameState.handNumber > 10 && (
          <View style={styles.gameOver}>
            <Text style={styles.gameOverTitle}>Game Over!</Text>
            <Text style={styles.gameOverText}>
              Final Score - You: {gameState.playerWins}, AI: {gameState.aiWins}
            </Text>
            <Text style={styles.gameOverText}>
              Final Stacks - You: ${gameState.playerStack}, AI: ${gameState.aiStack}
            </Text>
            <TouchableOpacity
              style={styles.newGameButton}
              onPress={() => {
                setGameState({
                  playerCards: [],
                  aiCards: [],
                  communityCards: [],
                  playerStack: 1000,
                  aiStack: 1000,
                  pot: 0,
                  currentBet: 0,
                  playerFirst: true,
                  gamePhase: 'preflop',
                  handNumber: 1,
                  playerWins: 0,
                  aiWins: 0,
                  isPlayerTurn: true,
                  lastAction: '',
                });
                dealCards();
              }}
            >
              <Text style={styles.newGameButtonText}>New Game</Text>
            </TouchableOpacity>
          </View>
        )}
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1a1a1a',
  },
  table: {
    flex: 1,
    padding: 20,
  },
  gameInfo: {
    alignItems: 'center',
    marginBottom: 20,
  },
  handNumber: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#4CAF50',
  },
  score: {
    fontSize: 16,
    color: '#ffffff',
    marginTop: 5,
  },
  phase: {
    fontSize: 14,
    color: '#cccccc',
    marginTop: 5,
  },
  aiArea: {
    alignItems: 'center',
    marginBottom: 30,
  },
  playerArea: {
    alignItems: 'center',
    marginTop: 30,
  },
  playerLabel: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#ffffff',
    marginBottom: 10,
  },
  stackInfo: {
    marginBottom: 10,
  },
  stackText: {
    fontSize: 16,
    color: '#cccccc',
  },
  cardsContainer: {
    flexDirection: 'row',
    gap: 10,
  },
  card: {
    width: 60,
    height: 80,
    backgroundColor: '#ffffff',
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: '#333333',
  },
  hiddenCard: {
    backgroundColor: '#2a2a2a',
  },
  cardText: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  redCard: {
    color: '#ff0000',
  },
  blackCard: {
    color: '#000000',
  },
  communityArea: {
    alignItems: 'center',
    marginVertical: 20,
  },
  communityLabel: {
    fontSize: 16,
    color: '#cccccc',
    marginBottom: 10,
  },
  potArea: {
    alignItems: 'center',
    marginVertical: 20,
  },
  potText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#ffd700',
  },
  betText: {
    fontSize: 14,
    color: '#ff4444',
    marginTop: 5,
  },
  actionArea: {
    alignItems: 'center',
    marginTop: 20,
  },
  turnText: {
    fontSize: 16,
    color: '#4CAF50',
    marginBottom: 15,
  },
  buttonRow: {
    flexDirection: 'row',
    gap: 10,
  },
  actionButton: {
    backgroundColor: '#4CAF50',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 8,
    minWidth: 80,
    alignItems: 'center',
  },
  disabledButton: {
    backgroundColor: '#666666',
  },
  buttonText: {
    color: '#ffffff',
    fontSize: 14,
    fontWeight: 'bold',
  },
  betInput: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 15,
  },
  betLabel: {
    fontSize: 14,
    color: '#ffffff',
    marginRight: 10,
  },
  input: {
    backgroundColor: '#ffffff',
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 4,
    minWidth: 100,
    fontSize: 14,
    color: '#000000',
  },
  lastAction: {
    alignItems: 'center',
    marginTop: 20,
  },
  lastActionText: {
    fontSize: 16,
    color: '#cccccc',
    fontStyle: 'italic',
  },
  gameOver: {
    alignItems: 'center',
    marginTop: 30,
    padding: 20,
    backgroundColor: '#2a2a2a',
    borderRadius: 12,
  },
  gameOverTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#ffd700',
    marginBottom: 15,
  },
  gameOverText: {
    fontSize: 16,
    color: '#ffffff',
    marginBottom: 10,
  },
  newGameButton: {
    backgroundColor: '#4CAF50',
    paddingHorizontal: 30,
    paddingVertical: 15,
    borderRadius: 8,
    marginTop: 15,
  },
  newGameButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: 'bold',
  },
});

export default HeadsUpScreen; 