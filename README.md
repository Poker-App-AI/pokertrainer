# Poker Trainer – Developer Documentation

Welcome to the Poker Trainer backend! This document will help you understand the folder structure, the purpose of each module, and how to contribute or extend the codebase.

---

## **Setup Instructions**

1. **Clone the repository**
2. **Create and activate a virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Set up Ollama (for LLM explanations):**
   - [Install Ollama](https://ollama.com/download)
   - Start Ollama and pull your desired model, e.g.:
     ```sh
     ollama run llama3
     # or for deepseek
     ollama run deepseek
     ```
   - Make sure Ollama is running at `http://localhost:11434` (default)
5. **Run the FastAPI server:**
   ```sh
   uvicorn poker.server.main:app --reload
   ```
   - Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive API documentation.

---

## **Folder Structure Overview**

```
poker/
  trainer/
    server/
      main.py           # FastAPI app: HTTP endpoints only, no business logic
    engine.py           # Poker equity and simulation logic
    llm.py              # LLM (Ollama) integration for explanations
    utils.py            # Poker utility functions (parsing, hand evaluation, etc.)
    models/
      __init__.py
      card.py           # Card class
      deck.py           # Deck class
      puzzle.py         # Puzzle and Opponent dataclasses
    puzzles/
      __init__.py
      default_puzzles.py # List of Puzzle objects (the scenarios)
```

---

## **Module Responsibilities**

### **API Layer**
- **server/main.py**  
  - FastAPI app.
  - Defines HTTP endpoints for puzzles, equity calculation, and LLM explanations.
  - Should only handle HTTP, validation, and call into the core logic.

### **Core Poker Logic**
- **engine.py**  
  - Contains the main poker simulation and equity calculation logic.
  - Defines opponent ranges and pre-processes them for simulation.

- **utils.py**  
  - Utility functions for parsing hands, evaluating hand strength, and generating hand permutations.

- **llm.py**  
  - Handles communication with the local Ollama LLM server.
  - Generates explanations for poker decisions.

### **Data Models**
- **models/card.py**  
  - `Card` class: represents a playing card.

- **models/deck.py**  
  - `Deck` class: represents a shuffled deck and card dealing logic.

- **models/puzzle.py**  
  - `Puzzle` dataclass: represents a poker scenario.
  - `Opponent` dataclass: represents an opponent in a puzzle.

- **models/__init__.py**  
  - Exposes all model classes for easy import.

### **Puzzles**
- **puzzles/default_puzzles.py**  
  - Contains a list of `Puzzle` objects (the scenarios for the trainer).

- **puzzles/__init__.py**  
  - Exposes the puzzles for import.

---

## **How to Add or Modify Puzzles**

- Edit `poker/trainer/puzzles/default_puzzles.py`.
- Add a new `Puzzle` object to the `PUZZLES` list.
- Each `Puzzle` requires:
  - `player_hand`, `board_cards`, `pot_size`, `bet_to_call`, `player_chips_remaining`, `opponents`, `current_player_to_act_index`, `question`.

---

## **How to Add New Features or Logic**

- **Poker logic:**  
  Add or modify functions in `engine.py` or `utils.py`.

- **LLM features:**  
  Update `llm.py` for new prompt strategies or LLM models.

- **Data models:**  
  Add new dataclasses to `models/`.

- **API endpoints:**  
  Add new routes to `server/main.py`.  
  Keep endpoints thin—call into the core logic, don't duplicate it.

---

## **Import Conventions**

- Always import models and utilities using the full package path, e.g.:
  ```python
  from poker.trainer.models import Card, Deck, Puzzle, Opponent
  from poker.trainer.utils import parse_hand_string
  ```

---

## **Best Practices**

- **Do not duplicate logic** between API and core modules.
- **Write tests** for new logic (consider a `tests/` folder).
- **Document** new endpoints and features in this file.

---

## **Contact**

For questions or to propose major changes, please open an issue or pull request.

---

**Happy contributing!**