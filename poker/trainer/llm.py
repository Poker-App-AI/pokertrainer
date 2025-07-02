import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "deepseek-r1"  # Change to your preferred model

def get_llm_explanation(puzzle, user_action, correct_action, equity_result):
    print(puzzle.board_cards)
    prompt = f"""

    Task: 
    You are an expert poker trainer. You are given a poker scenario and you need to explain why the correct action is {correct_action.upper()} and what factors influenced this decision.
    Do not use any emojis. Do not ask questions at the end. 
    
    IMPORTANT RULES:
        -- The type of opponent is in the format of "standard" for a standard opponent, "tight" for a tight opponent, "loose" for a loose opponent. Use standard poker knowledge when understanding types of an opponent.
        -- Please ensure that you deduce the player's hand and the board's hand properly when making your decision. 
        -- The format of the players hand will always be 4 characters long with this regex: [2-9TJQKA][cdhs] where the first character is the rank and the second character is the suit of the first card, and the third character is the rank and the fourth character is the suit of the second card.
        -- Limit your response to 100 words.
        
    Poker scenario:
    - Your hand: {puzzle.player_hand}
    - Board: {puzzle.board_cards or 'Preflop'}
    - Pot size: {puzzle.pot_size}
    - Bet to call: {puzzle.bet_to_call}
    - Opponents: {', '.join([f'{op.type} ({op.chips_remaining} chips)' for op in puzzle.opponents])}
    - Your action: {user_action}
    - Correct action: {correct_action}
    - Equity breakdown: {equity_result}

    
    """
    data = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=data)
    response.raise_for_status()
    return response.json().get("response", "No explanation available.") 