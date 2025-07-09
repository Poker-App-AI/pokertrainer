import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

export interface Puzzle {
  id: number;
  player_hand: string;
  board_cards: string;
  pot_size: number;
  bet_to_call: number;
  player_chips_remaining: number;
  opponents: Array<{
    type: string;
    chips_remaining: number;
  }>;
  current_player_to_act_index: number;
  question: string;
}

interface PuzzleContextType {
  puzzles: Puzzle[];
  currentPuzzle: Puzzle | null;
  loading: boolean;
  error: string | null;
  setCurrentPuzzle: (puzzle: Puzzle) => void;
  fetchPuzzles: () => Promise<void>;
}

const PuzzleContext = createContext<PuzzleContextType | undefined>(undefined);

export const usePuzzle = () => {
  const context = useContext(PuzzleContext);
  if (!context) {
    throw new Error('usePuzzle must be used within a PuzzleProvider');
  }
  return context;
};

export const PuzzleProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [puzzles, setPuzzles] = useState<Puzzle[]>([]);
  const [currentPuzzle, setCurrentPuzzle] = useState<Puzzle | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchPuzzles = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get('http://localhost:8000/puzzles/');
      const puzzlePromises = response.data.map(async (puzzle: any) => {
        const fullPuzzle = await axios.get(`http://localhost:8000/puzzles/${puzzle.id}`);
        return fullPuzzle.data;
      });
      const fullPuzzles = await Promise.all(puzzlePromises);
      setPuzzles(fullPuzzles);
    } catch (err) {
      setError('Failed to fetch puzzles');
      console.error('Error fetching puzzles:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPuzzles();
  }, []);

  return (
    <PuzzleContext.Provider
      value={{
        puzzles,
        currentPuzzle,
        loading,
        error,
        setCurrentPuzzle,
        fetchPuzzles,
      }}
    >
      {children}
    </PuzzleContext.Provider>
  );
}; 