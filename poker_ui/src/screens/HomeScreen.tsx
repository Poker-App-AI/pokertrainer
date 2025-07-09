import React from 'react';
import {
  View,
  Text,
  FlatList,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  RefreshControl,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { usePuzzle } from '../context/PuzzleContext';

const HomeScreen: React.FC = () => {
  const navigation = useNavigation();
  const { puzzles, loading, error, fetchPuzzles } = usePuzzle();

  const renderPuzzleItem = ({ item, index }: { item: any; index: number }) => (
    <TouchableOpacity
      style={styles.puzzleItem}
      onPress={() => {
        // @ts-ignore
        navigation.navigate('Puzzle', { puzzleId: index });
      }}
    >
      <View style={styles.puzzleHeader}>
        <Text style={styles.puzzleNumber}>Puzzle #{index + 1}</Text>
        <Text style={styles.puzzleHand}>{item.player_hand}</Text>
      </View>
      <Text style={styles.puzzleQuestion} numberOfLines={2}>
        {item.question}
      </Text>
      <View style={styles.puzzleInfo}>
        <Text style={styles.potSize}>Pot: ${item.pot_size}</Text>
        <Text style={styles.betSize}>Bet: ${item.bet_to_call}</Text>
      </View>
    </TouchableOpacity>
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#4CAF50" />
        <Text style={styles.loadingText}>Loading puzzles...</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>{error}</Text>
        <TouchableOpacity style={styles.retryButton} onPress={fetchPuzzles}>
          <Text style={styles.retryButtonText}>Retry</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Poker Trainer</Text>
      <Text style={styles.subtitle}>Test your poker skills with these puzzles</Text>
      <FlatList
        data={puzzles}
        renderItem={renderPuzzleItem}
        keyExtractor={(_, index) => index.toString()}
        contentContainerStyle={styles.listContainer}
        refreshControl={
          <RefreshControl refreshing={loading} onRefresh={fetchPuzzles} />
        }
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1a1a1a',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#1a1a1a',
  },
  loadingText: {
    color: '#ffffff',
    fontSize: 16,
    marginTop: 10,
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#1a1a1a',
    padding: 20,
  },
  errorText: {
    color: '#ff4444',
    fontSize: 16,
    textAlign: 'center',
    marginBottom: 20,
  },
  retryButton: {
    backgroundColor: '#4CAF50',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 8,
  },
  retryButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#ffffff',
    textAlign: 'center',
    marginTop: 20,
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 16,
    color: '#cccccc',
    textAlign: 'center',
    marginBottom: 20,
  },
  listContainer: {
    padding: 20,
  },
  puzzleItem: {
    backgroundColor: '#2a2a2a',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  puzzleHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  puzzleNumber: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#4CAF50',
  },
  puzzleHand: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#ffd700',
  },
  puzzleQuestion: {
    fontSize: 14,
    color: '#ffffff',
    marginBottom: 12,
    lineHeight: 20,
  },
  puzzleInfo: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  potSize: {
    fontSize: 12,
    color: '#cccccc',
  },
  betSize: {
    fontSize: 12,
    color: '#cccccc',
  },
});

export default HomeScreen; 