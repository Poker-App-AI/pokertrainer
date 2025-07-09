# Poker Trainer App

A React Native application for practicing poker skills through interactive puzzles. The app features a sleek, modern UI that works on both mobile devices and web browsers.

## Features

- **Interactive Poker Puzzles**: Practice with real poker scenarios
- **Visual Poker Table**: See your cards and the board clearly
- **AI Explanations**: Get detailed explanations for each puzzle
- **Cross-Platform**: Works on iOS, Android, and web browsers
- **Modern UI**: Sleek, dark theme with intuitive controls

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Expo CLI (`npm install -g @expo/cli`)

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

3. Run on your preferred platform:
- **Web**: Press `w` in the terminal or visit the URL shown
- **iOS**: Press `i` in the terminal (requires iOS Simulator)
- **Android**: Press `a` in the terminal (requires Android Emulator)

### Backend Setup

Make sure your Python backend server is running:

```bash
cd poker/server
uvicorn main:app --reload
```

The app will connect to `http://localhost:8000` by default.

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Card.tsx        # Poker card display
│   ├── PokerTable.tsx  # Poker table layout
│   └── ActionButtons.tsx # Action buttons (fold/call/raise)
├── screens/            # Screen components
│   ├── HomeScreen.tsx  # Puzzle list
│   └── PuzzleScreen.tsx # Individual puzzle view
└── context/           # State management
    └── PuzzleContext.tsx # Puzzle data and API calls
```

## Usage

1. **Browse Puzzles**: View all available poker puzzles on the home screen
2. **Select Puzzle**: Tap on any puzzle to start
3. **Analyze Situation**: Review your cards, the board, and pot information
4. **Make Decision**: Choose to fold, call, or raise
5. **Get Explanation**: Receive AI-powered analysis of your decision
6. **Continue**: Move to the next puzzle or try again

## API Endpoints

The app connects to these backend endpoints:

- `GET /puzzles/` - List all puzzles
- `GET /puzzles/{id}` - Get specific puzzle details
- `POST /llm/explanation/` - Get AI explanation for user action

## Technologies Used

- **React Native**: Cross-platform mobile development
- **Expo**: Development platform and tools
- **TypeScript**: Type-safe JavaScript
- **React Navigation**: Screen navigation
- **Axios**: HTTP client for API calls

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on multiple platforms
5. Submit a pull request

## License

This project is licensed under the MIT License.