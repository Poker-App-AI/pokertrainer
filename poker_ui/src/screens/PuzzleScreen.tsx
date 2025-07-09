import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { useRoute, useNavigation } from '@react-navigation/native';
import { usePuzzle } from '../context/PuzzleContext';
import PokerTable from '../components/PokerTable';
import ActionButtons from '../components/ActionButtons';
import axios from 'axios';

const PuzzleScreen: React.FC = () => {
  const route = useRoute();
  const navigation = useNavigation();
  const { puzzles, setCurrentPuzzle } = usePuzzle();
  const [selectedAction, setSelectedAction] = useState<string | null>(null);
  const [explanation, setExplanation] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [showResult, setShowResult] = useState(false);
  const [showExplanation, setShowExplanation] = useState(false);
  const [showdownHands, setShowdownHands] = useState<string[] | null>(null);
  const [resultText, setResultText] = useState<string | null>(null);
  const [correctAction, setCorrectAction] = useState<string | null>(null);

  // @ts-ignore
  const puzzleId = route.params?.puzzleId || 0;
  const puzzle = puzzles[puzzleId];

  useEffect(() => {
    if (puzzle) {
      setCurrentPuzzle(puzzle);
    }
  }, [puzzle, setCurrentPuzzle]);

  const handleAction = async (action: string) => {
    setSelectedAction(action);
    setLoading(true);
    setShowResult(false);
    setShowExplanation(false);
    setShowdownHands(null);
    setResultText(null);
    setExplanation(null);
    // Determine correct action
    const correct = determineCorrectAction(puzzle);
    setCorrectAction(correct);
    // Show result
    let result;
    if (action === correct) {
      result = 'Correct!';
    } else {
      result = `Incorrect. Correct action: ${correct.toUpperCase()}`;
    }
    setResultText(result);
    setShowResult(true);
    // Fetch showdown hands
    try {
      const showdownResp = await axios.get(`http://localhost:8000/puzzles/${puzzleId}/showdown/`);
      setShowdownHands(showdownResp.data.opponents);
    } catch (e) {
      setShowdownHands(null);
    }
    setLoading(false);
  };

  const handleShowExplanation = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/llm/explanation/', {
        puzzle_id: puzzleId,
        user_action: selectedAction,
        correct_action: correctAction,
      });
      setExplanation(response.data.explanation);
      setShowExplanation(true);
    } catch (error) {
      setExplanation('Unable to get AI explanation at this time.');
      setShowExplanation(true);
    } finally {
      setLoading(false);
    }
  };

  const determineCorrectAction = (puzzle: any): string => {
    // Simple logic - in reality this would be more sophisticated
    const potOdds = puzzle.bet_to_call / (puzzle.pot_size + puzzle.bet_to_call);
    
    if (potOdds < 0.2) {
      return 'call';
    } else if (potOdds > 0.4) {
      return 'fold';
    } else {
      return 'raise';
    }
  };

  const resetPuzzle = () => {
    setSelectedAction(null);
    setExplanation(null);
    setShowResult(false);
    setShowExplanation(false);
    setShowdownHands(null);
    setResultText(null);
    setCorrectAction(null);
  };

  const nextPuzzle = () => {
    if (puzzleId < puzzles.length - 1) {
      // @ts-ignore
      navigation.replace('Puzzle', { puzzleId: puzzleId + 1 });
      resetPuzzle();
    } else {
      Alert.alert('Congratulations!', 'You\'ve completed all puzzles!');
    }
  };

  if (!puzzle) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#4CAF50" />
        <Text style={styles.loadingText}>Loading puzzle...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <ScrollView style={styles.scrollView}>
        <View style={styles.questionContainer}>
          <Text style={styles.question}>{puzzle.question}</Text>
        </View>
        <PokerTable puzzle={puzzle} showdownHands={showdownHands} />
        {/* Result and Show Explanation button */}
        {showResult && (
          <View style={styles.resultContainer}>
            <Text style={styles.resultText}>{resultText}</Text>
            {!showExplanation && (
              <TouchableOpacity style={styles.showExplanationButton} onPress={handleShowExplanation} disabled={loading}>
                <Text style={styles.buttonText}>Show AI Explanation</Text>
              </TouchableOpacity>
            )}
          </View>
        )}
        {/* AI Explanation */}
        {showExplanation && explanation && (
          <View style={styles.explanationContainer}>
            <Text style={styles.explanationTitle}>AI Explanation</Text>
            <Text style={styles.explanationText}>{explanation}</Text>
          </View>
        )}
      </ScrollView>
      {/* Action buttons only if not acted yet */}
      {!selectedAction && (
        <ActionButtons
          onAction={handleAction}
          disabled={loading}
        />
      )}
      {/* Try Again/Next buttons if result shown */}
      {showResult && (
        <View style={styles.resultButtons}>
          <TouchableOpacity style={styles.button} onPress={resetPuzzle}>
            <Text style={styles.buttonText}>Try Again</Text>
          </TouchableOpacity>
          <TouchableOpacity style={[styles.button, styles.nextButton]} onPress={nextPuzzle}>
            <Text style={styles.buttonText}>Next Puzzle</Text>
          </TouchableOpacity>
        </View>
      )}
      {loading && (
        <View style={styles.loadingOverlay}>
          <ActivityIndicator size="large" color="#4CAF50" />
          <Text style={styles.loadingText}>Loading...</Text>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1a1a1a',
  },
  scrollView: {
    flex: 1,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#1a1a1a',
  },
  loadingOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    color: '#ffffff',
    fontSize: 16,
    marginTop: 10,
  },
  questionContainer: {
    backgroundColor: '#2a2a2a',
    margin: 20,
    padding: 16,
    borderRadius: 12,
  },
  question: {
    color: '#ffffff',
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'center',
    lineHeight: 24,
  },
  explanationContainer: {
    backgroundColor: '#2a2a2a',
    margin: 20,
    padding: 16,
    borderRadius: 12,
  },
  explanationTitle: {
    color: '#4CAF50',
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  explanationText: {
    color: '#ffffff',
    fontSize: 14,
    lineHeight: 20,
  },
  resultButtons: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    padding: 20,
    backgroundColor: '#2a2a2a',
  },
  button: {
    backgroundColor: '#4CAF50',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 8,
    minWidth: 100,
    alignItems: 'center',
  },
  nextButton: {
    backgroundColor: '#ff9800',
  },
  buttonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  resultContainer: {
    margin: 20,
    padding: 16,
    borderRadius: 12,
    backgroundColor: '#2a2a2a',
    alignItems: 'center',
  },
  resultText: {
    color: '#ffffff',
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 10,
  },
  showExplanationButton: {
    backgroundColor: '#ff9800',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 8,
  },
});

export default PuzzleScreen; 