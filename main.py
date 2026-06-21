import numpy as np
import random

"""
0: none
1: cross
2: circle
cross goes first
"""

class Node:
    def __init__(self, state, turn, parent=None):
        self.state = state
        self.turn = turn
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
        self.untried_moves = get_valid_moves(state)
        self.loss = 0

def select(node):
    while node.untried_moves == [] and node.children != []:
        C = 30
        node = max(node.children, key=lambda c:
                   c.wins / c.visits + C * np.sqrt(np.log(node.visits) / c.visits) - 5 * c.loss)
    return node

def expand(node):
    move = random.choice(node.untried_moves)
    node.untried_moves.remove(move)
    new_state = apply_move(node.state, move, node.turn)
    next_turn = 3 - node.turn
    child = Node(new_state, next_turn, parent=node)
    node.children.append(child)
    return child

def simulate(state, turn):
    current = state
    current_turn = turn
    while not is_terminal(current):
        moves = get_valid_moves(current)
        move = random.choice(moves)
        current = apply_move(current, move, current_turn)
        current_turn = 3 - current_turn
    return get_winner(current)

def backpropagate(node, winner, player):
    while node:
        node.visits += 1
        if winner == player:
            node.wins += 1
        elif winner != 0:
            node.loss += 1
        node = node.parent

def mcts(root_state, iterations=5000, turn=1):
    root = Node(root_state, turn)

    for _ in range(iterations):
        node = select(root)
        if not is_terminal(node.state):
            node = expand(node)

        winner = simulate(node.state, node.turn)
        backpropagate(node, winner, turn)
    return max(root.children, key=lambda c: c.visits).state

def state_creation(size=3):
    table = {}
    for i in range(size):
        for j in range(size):
            table[(i, j)] = 0
    return table

def get_winner(state):
    lines = [
        [(0,0), (0,1), (0,2)],
        [(1,0), (1,1), (1,2)],
        [(2,0), (2,1), (2,2)],
        [(0,0), (1,0), (2,0)],
        [(0,1), (1,1), (2,1)],
        [(0,2), (1,2), (2,2)],
        [(0,0), (1,1), (2,2)],
        [(0,2), (1,1), (2,0)],
    ]
    for line in lines:
        vals = [state[p] for p in line]
        if vals[0] != 0 and vals[0] == vals[1] == vals[2]:
            return vals[0]
    return 0

def is_terminal(state):
    lines = [
        [(0,0), (0,1), (0,2)],
        [(1,0), (1,1), (1,2)],
        [(2,0), (2,1), (2,2)],
        [(0,0), (1,0), (2,0)],
        [(0,1), (1,1), (2,1)],
        [(0,2), (1,2), (2,2)],
        [(0,0), (1,1), (2,2)],
        [(0,2), (1,1), (2,0)],
    ]
    for line in lines:
        vals = [state[p] for p in line]
        if vals[0] != 0 and vals[0] == vals[1] == vals[2]:
            return True
    if len(get_valid_moves(state)) == 0:
        return True
    return False

def get_valid_moves(state):
    return [coord for coord in state if state[coord] == 0]

def apply_move(state, move, turn):
    new_state = state.copy()
    new_state[move] = turn
    return new_state

def print_board(state):
    symbols = {0: '.', 1: 'X', 2: 'O'}
    for i in range(3):
        row = [symbols[state[(i, j)]] for j in range(3)]
        print(' '.join(row))

# ============================================================
# PLAY
# ============================================================
state = state_creation()
turn = 1

while not is_terminal(state):
    if turn == 1:
        state = mcts(state, iterations=5000, turn=1)
    else:
        state = mcts(state, iterations=5000, turn=2)
    
    turn = 3 - turn
    print_board(state)
    print()

winner = get_winner(state)
print(f"Winner: {winner}")




import matplotlib.pyplot as plt
import numpy as np

plt.style.use('dark_background')
fig, (ax_board, ax_stats) = plt.subplots(1, 2, figsize=(12, 6))
fig.patch.set_facecolor('#0d0d1a')

wins_cross, wins_circle, draws = 0, 0, 0
games = 50

for game in range(games):
    state = state_creation()
    turn = 1
    
    while not is_terminal(state):
        # Update board
        ax_board.clear()
        ax_board.set_facecolor('#0d0d1a')
        ax_board.set_xlim(0, 3)
        ax_board.set_ylim(0, 3)
        ax_board.set_xticks([0.5, 1.5, 2.5])
        ax_board.set_yticks([0.5, 1.5, 2.5])
        ax_board.set_xticklabels([])
        ax_board.set_yticklabels([])
        ax_board.invert_yaxis()
        
        # Draw grid lines
        for i in range(1, 3):
            ax_board.axhline(i, color='white', linewidth=2)
            ax_board.axvline(i, color='white', linewidth=2)
        
        # Draw X's and O's in CENTER of cells
        for (i, j), val in state.items():
            if val == 1:
                ax_board.text(j + 0.5, i + 0.5, 'X', fontsize=40, color='#00d4ff',
                             ha='center', va='center', fontweight='bold')
            elif val == 2:
                ax_board.text(j + 0.5, i + 0.5, 'O', fontsize=40, color='#ff6b6b',
                             ha='center', va='center', fontweight='bold')
        
        ax_board.set_title(f'Game {game + 1}', fontsize=14, color='white', fontweight='bold')
        
        # Update stats
        ax_stats.clear()
        ax_stats.set_facecolor('#0d0d1a')
        bars = ax_stats.bar(['Cross (X)', 'Circle (O)', 'Draws'], 
                           [wins_cross, wins_circle, draws],
                           color=['#00d4ff', '#ff6b6b', '#888888'],
                           edgecolor='white', linewidth=1.5)
        ax_stats.set_ylabel('Count', fontsize=12, color='white')
        ax_stats.set_title(f'Stats ({game + 1} games)', fontsize=14, color='white', fontweight='bold')
        ax_stats.tick_params(colors='white')
        ax_stats.set_ylim(0, max(wins_cross, wins_circle, draws, 1) + 1)
        for bar, count in zip(bars, [wins_cross, wins_circle, draws]):
            ax_stats.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                         str(count), ha='center', color='white', fontweight='bold')
        
        # MCTS move
        state = mcts(state, iterations=5000, turn=turn)
        turn = 3 - turn
        
        plt.draw()
        plt.pause(0.2)
    
    winner = get_winner(state)
    if winner == 1:
        wins_cross += 1
    elif winner == 2:
        wins_circle += 1
    else:
        draws += 1

plt.show()
print(f"\nFinal: X={wins_cross}, O={wins_circle}, Draws={draws}")






"""state = state_creation()
turn = 1

while not is_terminal(state):
    print_board(state)
    print()
    
    if turn == 1:
        while True:
            move = input("Enter row,col (0-2): ")
            row, col = map(int, move.split(','))
            if (row, col) in get_valid_moves(state):
                break
            print("Invalid move. Try again.")
        state = apply_move(state, (row, col), turn)
    else:
        print("MCTS is thinking...")
        state = mcts(state, iterations=5000, turn=2)
    
    turn = 3 - turn

print_board(state)
winner = get_winner(state)
print(f"Winner: {winner}")"""