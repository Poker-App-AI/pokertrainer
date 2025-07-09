import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import Card from './Card';
import { Puzzle } from '../context/PuzzleContext';

interface PokerTableProps {
  puzzle: Puzzle;
}

const PokerTable: React.FC<PokerTableProps> = ({ puzzle }) => {
  const renderPlayerHand = () => {
    const cards = [puzzle.player_hand.slice(0, 2), puzzle.player_hand.slice(2, 4)];
    return (
      <View style={styles.playerHand}>
        <Text style={styles.sectionTitle}>Your Hand</Text>
        <View style={styles.cardsContainer}>
          {cards.map((card, index) => (
            <Card key={index} card={card} size="large" />
          ))}
        </View>
      </View>
    );
  };

  const renderBoard = () => {
    if (!puzzle.board_cards) return null;
    
    const cards = [];
    for (let i = 0; i < puzzle.board_cards.length; i += 2) {
      cards.push(puzzle.board_cards.slice(i, i + 2));
    }

    return (
      <View style={styles.board}>
        <Text style={styles.sectionTitle}>Board</Text>
        <View style={styles.cardsContainer}>
          {cards.map((card, index) => (
            <Card key={index} card={card} size="medium" />
          ))}
        </View>
      </View>
    );
  };

  const renderPotInfo = () => (
    <View style={styles.potInfo}>
      <View style={styles.potItem}>
        <Text style={styles.potLabel}>Pot Size:</Text>
        <Text style={styles.potValue}>${puzzle.pot_size}</Text>
      </View>
      <View style={styles.potItem}>
        <Text style={styles.potLabel}>Bet to Call:</Text>
        <Text style={styles.potValue}>${puzzle.bet_to_call}</Text>
      </View>
      <View style={styles.potItem}>
        <Text style={styles.potLabel}>Your Chips:</Text>
        <Text style={styles.potValue}>${puzzle.player_chips_remaining}</Text>
      </View>
    </View>
  );

  const renderOpponents = () => (
    <View style={styles.opponents}>
      <Text style={styles.sectionTitle}>Opponents</Text>
      {puzzle.opponents.map((opponent, index) => (
        <View key={index} style={styles.opponent}>
          <Text style={styles.opponentType}>{opponent.type}</Text>
          <Text style={styles.opponentChips}>${opponent.chips_remaining}</Text>
        </View>
      ))}
    </View>
  );

  return (
    <View style={styles.container}>
      <View style={styles.table}>
        {renderBoard()}
        {renderPotInfo()}
        {renderOpponents()}
      </View>
      {renderPlayerHand()}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1a1a1a',
  },
  table: {
    flex: 1,
    backgroundColor: '#2d5a2d',
    borderRadius: 20,
    margin: 20,
    padding: 20,
    justifyContent: 'space-between',
  },
  sectionTitle: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 10,
    textAlign: 'center',
  },
  cardsContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
  },
  board: {
    alignItems: 'center',
    marginBottom: 20,
  },
  potInfo: {
    backgroundColor: 'rgba(0, 0, 0, 0.3)',
    borderRadius: 10,
    padding: 15,
    marginBottom: 20,
  },
  potItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 5,
  },
  potLabel: {
    color: '#ffffff',
    fontSize: 14,
  },
  potValue: {
    color: '#ffd700',
    fontSize: 14,
    fontWeight: 'bold',
  },
  opponents: {
    alignItems: 'center',
  },
  opponent: {
    flexDirection: 'row',
    backgroundColor: 'rgba(0, 0, 0, 0.3)',
    borderRadius: 8,
    padding: 8,
    marginBottom: 5,
    minWidth: 120,
    justifyContent: 'space-between',
  },
  opponentType: {
    color: '#ffffff',
    fontSize: 12,
    textTransform: 'capitalize',
  },
  opponentChips: {
    color: '#ffd700',
    fontSize: 12,
    fontWeight: 'bold',
  },
  playerHand: {
    backgroundColor: '#2a2a2a',
    padding: 20,
    alignItems: 'center',
  },
});

export default PokerTable; 