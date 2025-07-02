from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from poker.trainer.puzzles import PUZZLES
from poker.trainer.engine import calculate_multi_way_equity
from poker.trainer.llm import get_llm_explanation

app = FastAPI()

class EquityRequest(BaseModel):
    player_hand: str
    board_cards: str = ""
    opponent_types: List[str]
    num_simulations: int = 1000

class LLMExplanationRequest(BaseModel):
    puzzle_id: int
    user_action: str
    correct_action: str

@app.get("/puzzles/")
def list_puzzles():
    return [{"id": i, "question": puzzle.question} for i, puzzle in enumerate(PUZZLES)]

@app.get("/puzzles/{puzzle_id}")
def get_puzzle(puzzle_id: int):
    try:
        puzzle = PUZZLES[puzzle_id]
        return puzzle
    except IndexError:
        raise HTTPException(status_code=404, detail="Puzzle not found")

@app.post("/equity/")
def calculate_equity(req: EquityRequest):
    result = calculate_multi_way_equity(
        req.player_hand,
        req.board_cards,
        req.opponent_types,
        req.num_simulations
    )
    return result

@app.post("/llm/explanation/")
def llm_explanation(req: LLMExplanationRequest):
    try:
        puzzle = PUZZLES[req.puzzle_id]
    except IndexError:
        raise HTTPException(status_code=404, detail="Puzzle not found")
    equity_result = calculate_multi_way_equity(
        puzzle.player_hand, puzzle.board_cards, [op.type for op in puzzle.opponents], 1000
    )
    explanation = get_llm_explanation(puzzle, req.user_action, req.correct_action, equity_result)
    return {"explanation": explanation} 