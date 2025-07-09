import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

interface CardProps {
  card: string;
  size?: 'small' | 'medium' | 'large' | 'xlarge';
}

const Card: React.FC<CardProps> = ({ card, size = 'medium' }) => {
  const getCardColor = (suit: string) => {
    return suit === 'h' || suit === 'd' ? '#ff4444' : '#000000';
  };

  const getSuitSymbol = (suit: string) => {
    switch (suit) {
      case 'h': return '♥';
      case 'd': return '♦';
      case 'c': return '♣';
      case 's': return '♠';
      default: return '';
    }
  };

  const getSizeStyles = () => {
    switch (size) {
      case 'small':
        return { width: 30, height: 42, fontSize: 12 };
      case 'large':
        return { width: 48, height: 66, fontSize: 17 };
      case 'xlarge':
        return { width: 60, height: 82, fontSize: 22 };
      default:
        return { width: 38, height: 54, fontSize: 13 };
    }
  };

  const sizeStyles = getSizeStyles();
  const rank = card[0];
  const suit = card[1];
  const color = getCardColor(suit);
  const suitSymbol = getSuitSymbol(suit);

  return (
    <View style={[styles.card, sizeStyles, { borderColor: color }]}>
      <Text style={[styles.rank, { color }, { fontSize: sizeStyles.fontSize }]}>
        {rank}
      </Text>
      <Text style={[styles.suit, { color }, { fontSize: sizeStyles.fontSize * 0.8 }]}>
        {suitSymbol}
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#ffffff',
    borderWidth: 2,
    borderRadius: 6,
    justifyContent: 'center',
    alignItems: 'center',
    marginHorizontal: 2,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  rank: {
    fontWeight: 'bold',
    marginBottom: -2,
  },
  suit: {
    fontWeight: 'bold',
  },
});

export default Card; 