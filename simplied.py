from random import *
import time

board = ["|" for _ in range(21)]
possible_moves = [1, 2, 3]  # Changed from 'choices' to avoid conflict
weights = [[1, 1, 1] for _ in range(len(board))]
claude_moves = []  # Track (sticks_remaining, move_index)
current_sticks = len(board)
player_turn = False  # Start with Claude's turn

def show_board():
    print(f"\nBoard: {''.join(board)} ({len(board)} sticks left)")

def update_weights(win):
    """Update weights based on whether Claude won (win=True) or lost (win=False)"""
    for sticks, move in claude_moves:
        if win:
            weights[sticks-1][move] += 1  # Reward winning moves
        else:
            weights[sticks-1][move] = max(1, weights[sticks-1][move] - 1)  # Penalize losing moves

def claude_play():
    global current_sticks
    sticks_left = len(board)
    valid_choices = [c for c in possible_moves if c <= sticks_left]
    valid_weights = [weights[sticks_left-1][possible_moves.index(c)] for c in valid_choices]
    
    choice = choices(valid_choices, weights=valid_weights, k=1)[0]  # Explicitly named parameter
    claude_moves.append((sticks_left, possible_moves.index(choice)))
    
    for _ in range(choice):
        if board:
            board.pop()
    current_sticks = len(board)
    
    print(f"\nClaude removes {choice} stick(s)")
    show_board()
    return current_sticks == 0

def player_play():
    global current_sticks
    print("\nYour turn!")
    while True:
        try:
            choice = int(input("Remove sticks (1-3): "))
            if choice in possible_moves and choice <= len(board):
                break
            print(f"Invalid! Choose 1-3 (max {len(board)}):")
        except ValueError:
            print("Please enter a number 1-3:")
    
    for _ in range(choice):
        if board:
            board.pop()
    current_sticks = len(board)
    
    show_board()
    return current_sticks == 0

def reset():
    global board, weights, claude_moves, current_sticks, player_turn
    board = ["|" for _ in range(21)]
    claude_moves = []
    current_sticks = len(board)
    player_turn = choice(False,True)

# Main game loop
print("NIM Game - Don't take the last stick!")
print("Start with 21 sticks, take 1-3 each turn")
show_board()

while True:
    if player_turn:
        game_over = player_play()
        if game_over:
            print("\nYou took the last stick - Claude wins!")
            update_weights(True)  # Claude wins
            if input("Play again? (y/n): ").lower() != 'y':
                break
            else:
                reset()
    else:
        game_over = claude_play()
        if game_over:
            print("\nClaude took the last stick - You win!")
            update_weights(False)  # Claude loses
            if input("Play again? (y/n): ").lower() != 'y':
                break
            else:
                reset()
    
    player_turn = not player_turn

# Show final weights
print("\nClaude's learned weights:")
print("Sticks || 1 | 2 | 3")
print("=======||===|===|===")
for i in range(min(10, len(weights))):  # Show first 10 positions
    print(f"{i+1:6} || {weights[i][0]} | {weights[i][1]} | {weights[i][2]}")
    print("-------||---|---|---")