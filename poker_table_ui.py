# poker_table_ui.py
"""
Poker table UI rendering for Streamlit Poker Trainer
"""
import streamlit as st

def card_html(card):
    rank = card[0]
    suit = card[1]
    suit_symbols = {'h': '♥', 'd': '♦', 'c': '♣', 's': '♠'}
    color_class = 'card red' if suit in ['h', 'd'] else 'card'
    return f'<span class="{color_class}">{rank}{suit_symbols.get(suit, suit)}</span>'

def blank_card_html():
    return '<span class="blank-card">🂠</span>'

def opponent_box_html(i, op, pos_style):
    return (
        f'<div style="{pos_style};text-align:center;">'
        f'<div class="opponent-label" style="margin-bottom:8px;position:relative;z-index:2;max-width:120px;">Opponent #{i+1}</div>'
        f"<div style='margin:8px 0 0 0;'>" + blank_card_html()*2 + "</div>"
        f"<div class='info-text' style='margin-top:4px;'>(Type: {op['type']})</div>"
        '</div>'
    )

def render_poker_table(puzzle, player_hand_cards, board_card_list):
    st.markdown(
        """
    <style>
    .poker-table-simple {
      position:relative;
      min-height:520px;
      max-width:900px;
      width:90vw;
      margin:auto;
      background:#2e7d3a; /* green felt */
      border:6px solid #8B5C2A; /* brown border */
      border-radius:48% / 40%;
      box-shadow:0 8px 32px 0 rgba(0,0,0,0.25), 0 1.5px 0 #7a4a1a;
      padding:0;
      font-family:'Segoe UI', Arial, sans-serif;
      overflow:hidden;
      transition:box-shadow 0.2s;
    }
    .poker-table-simple:hover {
      box-shadow:0 12px 48px 0 rgba(0,0,0,0.32), 0 2px 0 #7a4a1a;
    }
    .poker-table-simple .opponent-label {
      background:#f5f5f5;
      color:#222;
      border-radius:7px;
      padding:4px 18px;
      font-size:1.08em;
      font-weight:600;
      border:1.5px solid #bbb;
      margin-bottom:4px;
      display:inline-block;
      box-shadow:0 1px 2px #bbb2;
    }
    .poker-table-simple .pot-label {
      background:#f7e8b0;
      border:1.5px solid #e2c96c;
      border-radius:7px;
      color:#222;
      font-size:1.08em;
      font-weight:700;
      padding:5px 24px;
      margin-top:4px;
      margin-bottom:12px;
      display:inline-block;
      box-shadow:0 1px 2px #e2c96c44;
    }
    .poker-table-simple .card {
      display:inline-block;
      border:2px solid #bbb;
      border-radius:7px;
      padding:6px 16px;
      margin:4px;
      font-size:2em;
      color:#222;
      background:#fff;
      font-family:'Segoe UI', Arial, sans-serif;
      box-shadow:0 2px 6px #0001;
      transition:transform 0.12s, box-shadow 0.12s;
    }
    .poker-table-simple .card.red { color:#c33; }
    .poker-table-simple .card:focus, .poker-table-simple .card:hover {
      outline:none;
      transform:scale(1.08) rotate(-2deg);
      box-shadow:0 4px 16px #0002;
      z-index:2;
    }
    .poker-table-simple .blank-card {
      display:inline-block;
      border:2px solid #ddd;
      border-radius:7px;
      padding:6px 16px;
      margin:4px;
      font-size:2em;
      color:#bbb;
      background:#2e7d3a;
      font-family:'Segoe UI', Arial, sans-serif;
      box-shadow:0 1px 2px #0001;
    }
    .poker-table-simple .info-text {
      color:#eee;
      font-size:1.08em;
      margin-bottom:4px;
      letter-spacing:0.01em;
    }
    </style>""", unsafe_allow_html=True)

    # Determine opponent positions for up to 4
    opp_html = []
    num_opps = len(puzzle['opponents'])
    if num_opps == 1:
        opp_html.append(opponent_box_html(0, puzzle['opponents'][0], "position:absolute;left:50%;top:48px;transform:translateX(-50%);") )
    elif num_opps == 2:
        opp_html.append(opponent_box_html(0, puzzle['opponents'][0], "position:absolute;left:22%;top:48px;") )
        opp_html.append(opponent_box_html(1, puzzle['opponents'][1], "position:absolute;right:22%;top:48px;") )
    elif num_opps == 3:
        opp_html.append(opponent_box_html(0, puzzle['opponents'][0], "position:absolute;left:13%;top:48px;") )
        opp_html.append(opponent_box_html(1, puzzle['opponents'][1], "position:absolute;right:13%;top:48px;") )
        opp_html.append(opponent_box_html(2, puzzle['opponents'][2], "position:absolute;left:4%;top:54%;transform:translateY(-50%);") )
    elif num_opps >= 4:
        opp_html.append(opponent_box_html(0, puzzle['opponents'][0], "position:absolute;left:13%;top:48px;") )
        opp_html.append(opponent_box_html(1, puzzle['opponents'][1], "position:absolute;right:13%;top:48px;") )
        opp_html.append(opponent_box_html(2, puzzle['opponents'][2], "position:absolute;left:2.5%;top:54%;transform:translateY(-50%);") )
        opp_html.append(opponent_box_html(3, puzzle['opponents'][3], "position:absolute;right:2.5%;top:54%;transform:translateY(-50%);") )
    st.markdown(
        '<div class="poker-table-simple">'
        + ''.join(opp_html)
        # Board cards and pot row (centered, no overlap)
        + '<div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);display:flex;flex-direction:column;align-items:center;pointer-events:none;width:100%;">'
        + '<div style="display:flex;flex-direction:row;align-items:center;gap:16px;justify-content:center;width:100%;margin-bottom:8px;">'
        + '<span>' + ''.join([card_html(c) for c in board_card_list]) + '</span>'
        + '</div>'
        + '<div class="pot-label" style="margin-top:0;">Pot: ' + str(puzzle['pot_size']) + '</div>'
        + '</div>'
        # Player hand and label row (always below board)
        + '<div style="position:absolute;left:50%;top:66%;transform:translate(-50%,0);display:flex;flex-direction:column;align-items:center;width:100%;">'
        + "<div class='info-text' style='margin-bottom:8px;font-weight:bold;'>You</div>"
        + '<div style="display:flex;flex-direction:row;align-items:center;gap:16px;margin-bottom:0;justify-content:center;width:100%;">'
        + '<span>' + ''.join([card_html(c) for c in player_hand_cards]) + '</span>'
        + '</div>'
        + '</div>'
        # Chips at the bottom
        + '<div style="position:absolute;left:50%;bottom:18px;transform:translateX(-50%);text-align:center;">'
        + '<div class="info-text" style="margin-top:2px;">(Chips: ' + str(puzzle['player_chips_remaining']) + ')</div>'
        + '</div>'
        # Bet info at the very bottom
        + '<div style="position:absolute;left:50%;bottom:-32px;transform:translateX(-50%);text-align:center;font-size:1em;">'
        + '<b>Bet to call:</b> ' + str(puzzle['bet_to_call']) + ' | <b>Your chips:</b> ' + str(puzzle['player_chips_remaining'])
        + '</div>'
        + '</div>',
        unsafe_allow_html=True
    )
