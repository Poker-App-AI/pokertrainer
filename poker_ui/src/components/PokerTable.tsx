import React from 'react';
import { View, Text, StyleSheet, Dimensions } from 'react-native';
import Card from './Card';
import { Puzzle } from '../context/PuzzleContext';

interface PokerTableProps {
  puzzle: Puzzle;
  showdownHands?: string[] | null; // If present, show these opponent hands
}

const TABLE_WIDTH = Dimensions.get('window').width - 100;
const TABLE_HEIGHT = Math.round(TABLE_WIDTH * 0.4);


const PokerTable: React.FC<PokerTableProps> = ({ puzzle, showdownHands }) => {
  // Helper to render a hand (array of 2 cards)
  const renderHand = (hand: string, size: 'small' | 'medium' | 'large' | 'xlarge' = 'medium') => {
    if (!hand || hand.length !== 4) return null;
    return (
      <View style={styles.cardsContainer}>
        <Card card={hand.slice(0, 2)} size={size} />
        <Card card={hand.slice(2, 4)} size={size} />
      </View>
    );
  };

  // Board cards in the center
  const renderBoard = () => {
    if (!puzzle.board_cards) return null;
    const cards = [];
    for (let i = 0; i < puzzle.board_cards.length; i += 2) {
      cards.push(puzzle.board_cards.slice(i, i + 2));
    }
    return (
      <View style={styles.boardCardsRow}>
        {cards.map((card, idx) => (
          <Card key={idx} card={card} size="xlarge" />
        ))}
      </View>
    );
  };

  // Player's cards at bottom center, above name/chips
  const renderPlayer = () => (
    <View style={styles.playerAreaAbs}>
      {renderHand(puzzle.player_hand, 'xlarge')}
      <Text style={styles.playerName}>You</Text>
      <Text style={styles.chips}>${puzzle.player_chips_remaining}</Text>
    </View>
  );

  // Opponents spaced around the top arc (absolute)
  const renderOpponents = () => {
    const n = puzzle.opponents.length;
    const angleStart = 200; // degrees
    const angleEnd = -20; // degrees
    const radius = TABLE_HEIGHT / 2 - 30;
    return puzzle.opponents.map((opponent, idx) => {
      const angle = angleStart + (angleEnd - angleStart) * (n === 1 ? 0.5 : idx / (n - 1));
      const rad = (angle * Math.PI) / 180;
      const x = (TABLE_WIDTH / 2) + radius * Math.cos(rad) - 50;
      const y = (TABLE_HEIGHT / 2) + radius * Math.sin(rad) - 40;
      return (
        <View key={idx} style={[styles.seat, { position: 'absolute', left: x, top: y, alignItems: 'center' }]}> 
          {showdownHands && showdownHands[idx]
            ? renderHand(showdownHands[idx], 'large')
            : (
              <View style={styles.cardsContainer}>
                <Card card="XX" size="large" />
                <Card card="XX" size="large" />
              </View>
            )}
          <Text style={styles.seatLabel}>{opponent.type.charAt(0).toUpperCase() + opponent.type.slice(1)}</Text>
          <Text style={styles.chips}>${opponent.chips_remaining}</Text>
        </View>
      );
    });
  };

  // Pot info in center below board
  const renderPotInfo = () => (
    <View style={styles.potInfoCenter}>
      <Text style={styles.potLabel}>Pot: <Text style={styles.potValue}>${puzzle.pot_size}</Text></Text>
      <Text style={styles.potLabel}>To Call: <Text style={styles.potValue}>${puzzle.bet_to_call}</Text></Text>
    </View>
  );

  return (
    <View style={styles.rootContainer}>
      {/* Poker table oval */}
      <View style={styles.tableOval}>
        <View style={styles.innerOval} />
        {/* Board cards in center */}
        <View style={styles.boardCenter}>
          {renderBoard()}
          {renderPotInfo()}
        </View>
        {/* Opponents (absolute) */}
        {renderOpponents()}
      </View>
      {/* Player's cards and info at bottom center, outside oval */}
      {renderPlayer()}
    </View>
  );
};

const styles = StyleSheet.create({
  rootContainer: {
    width: TABLE_WIDTH,
    height: TABLE_HEIGHT + 120,
    alignSelf: 'center',
    marginVertical: 24,
  },
  tableOval: {
    width: TABLE_WIDTH,
    height: TABLE_HEIGHT,
    backgroundColor: '#226b2a',
    borderRadius: TABLE_HEIGHT / 2,
    borderWidth: 12,
    borderColor: '#6b3e1b',
    justifyContent: 'center',
    alignItems: 'center',
    overflow: 'hidden',
  },
  innerOval: {
    position: 'absolute',
    width: TABLE_WIDTH - 32,
    height: TABLE_HEIGHT - 32,
    top: 16,
    left: 16,
    borderRadius: (TABLE_HEIGHT - 32) / 2,
    borderWidth: 2,
    borderColor: '#fff2',
    backgroundColor: '#1a3c1a88',
    zIndex: 1,
  },
  boardCenter: {
    position: 'absolute',
    top: '38%',
    left: 0,
    width: '100%',
    alignItems: 'center',
    zIndex: 2,
  },
  boardCardsRow: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 8,
  },
  potInfoCenter: {
    backgroundColor: 'rgba(0,0,0,0.5)',
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 8,
    marginTop: 8,
    alignItems: 'center',
  },
  potLabel: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  potValue: {
    color: '#ffd700',
    fontWeight: 'bold',
  },
  seat: {
    backgroundColor: 'rgba(0,0,0,0.25)',
    borderRadius: 16,
    padding: 8,
    minWidth: 90,
    alignItems: 'center',
    zIndex: 3,
  },
  playerAreaAbs: {
    position: 'absolute',
    left: TABLE_WIDTH / 2 - 70,
    top: TABLE_HEIGHT + 18,
    alignItems: 'center',
    zIndex: 10,
  },
  playerName: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
    marginTop: 2,
  },
  seatLabel: {
    color: '#fff',
    fontSize: 14,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  chips: {
    color: '#ffd700',
    fontSize: 13,
    fontWeight: 'bold',
    marginTop: 2,
  },
  cardsContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    marginVertical: 2,
  },
});

export default PokerTable; 