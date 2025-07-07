import streamlit as st
from puzzles import puzzles
import random
from poker_engine import calculate_multi_way_equity
from poker_table_ui import render_poker_table

random.shuffle(puzzles)

# Initialize session state
if "puzzle_index" not in st.session_state:
    st.session_state.puzzle_index = 0
if "show_result" not in st.session_state:
    st.session_state.show_result = False
if "user_action" not in st.session_state:
    st.session_state.user_action = None

# Load current puzzle
puzzle = puzzles[st.session_state.puzzle_index]

st.title("🃏 Poker Trainer – Puzzle Mode")

st.markdown(f"### Puzzle {st.session_state.puzzle_index + 1}: {puzzle['question']}")

# --- Display Text Info ---
st.markdown("#### **Your Hand:**")
st.write(puzzle["player_hand"])

st.markdown("#### **Board Cards:**")
st.write(puzzle["board_cards"] if puzzle["board_cards"] else "No board yet (preflop)")

st.markdown("#### **Pot & Bet Info:**")
st.write(f"Pot size: {puzzle['pot_size']} | Bet to call: {puzzle['bet_to_call']} | Your chips: {puzzle['player_chips_remaining']}")

st.markdown("#### **Opponents:**")
for i, op in enumerate(puzzle["opponents"]):
    st.write(f"Opponent {i+1}: Type = {op['type']}, Chips = {op['chips_remaining']}")

# --- Display Poker Table ---
player_hand_cards = [puzzle["player_hand"][i:i+2] for i in range(0, len(puzzle["player_hand"]), 2)]
board_card_list = [puzzle["board_cards"][i:i+2] for i in range(0, len(puzzle["board_cards"]), 2)] if puzzle["board_cards"] else []
render_poker_table(puzzle, player_hand_cards, board_card_list)

# --- Action Buttons ---
st.markdown("### **Choose your action:**")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Fold"):
        st.session_state.user_action = "fold"
        st.session_state.show_result = True
with col2:
    if st.button("Call"):
        st.session_state.user_action = "call"
        st.session_state.show_result = True
with col3:
    if st.button("Raise"):
        st.session_state.user_action = "raise"
        st.session_state.show_result = True

# --- Process Result ---
if st.session_state.show_result:
    opponent_types = [op["type"] for op in puzzle["opponents"]]

    equity_result = calculate_multi_way_equity(
        puzzle["player_hand"],
        puzzle["board_cards"],
        opponent_types,
        num_simulations=5000
    )

    pot_odds_percentage = (puzzle["bet_to_call"] / (puzzle["pot_size"] + puzzle["bet_to_call"])) * 100
    player_equity = equity_result["player_win_percentage"] + equity_result["tie_percentage"] / 2

    if player_equity > pot_odds_percentage + 15:
        correct_action = "raise"
    elif player_equity > pot_odds_percentage:
        correct_action = "call"
    else:
        correct_action = "fold"

    st.markdown("### ✅ **Result:**")
    if st.session_state.user_action == correct_action:
        st.success(f"Correct! The optimal action is **{correct_action.upper()}**.")
    else:
        st.error(f"Incorrect. The correct action was **{correct_action.upper()}**.")

    st.markdown(f"**Your equity (win + tie/2):** {player_equity:.2f}%")
    st.markdown(f"**Pot odds required:** {pot_odds_percentage:.2f}%")

    with st.expander("See Full Equity Breakdown"):
        st.json(equity_result)

    # --- Next Puzzle Button ---
    if st.button("Next Puzzle"):
        st.session_state.puzzle_index = (st.session_state.puzzle_index + 1) % len(puzzles)
        st.session_state.show_result = False
        st.session_state.user_action = None

# --- Reset State if first load ---
if st.session_state.user_action is None:
    st.session_state.show_result = False
