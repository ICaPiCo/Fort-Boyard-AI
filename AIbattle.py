from random import *
import time

# Game configuration
INITIAL_STICKS = 21
CHOICES = [1, 2, 3]
TRAINING_GAMES = 10000

# Initialize two AI agents with their own weights (with slight random variations)
ai1_weights = [[1 + random()*0.1, 1 + random()*0.1, 1 + random()*0.1] for _ in range(INITIAL_STICKS)]
ai2_weights = [[1 + random()*0.1, 1 + random()*0.1, 1 + random()*0.1] for _ in range(INITIAL_STICKS)]

# Track wins for reporting
ai1_wins = 0
ai2_wins = 0

def play_game(ai1_w, ai2_w, is_training=True, player_goes_first=False):
    """Play a complete Nim game between two AIs or AI vs player"""
    board = ["|" for _ in range(INITIAL_STICKS)]
    ai1_steps = []  # Will store tuples of (board_size, move_index)
    ai2_steps = []  # Will store tuples of (board_size, move_index)
    
    current_turn = not player_goes_first if not is_training else True
    
    if not is_training:
        print(f"\nInitial board: {''.join(board)} ({len(board)} sticks)")
    
    while len(board) > 0:
        board_size = len(board)
        
        if is_training:
            if current_turn:  # AI1's turn
                weights = ai1_w[board_size - 1]
                valid_choices = [c for c in CHOICES if c <= board_size]
                valid_weights = [max(1, weights[CHOICES.index(c)]) for c in valid_choices]
                choice = choices(valid_choices, valid_weights, k=1)[0]
                ai1_steps.append((board_size, CHOICES.index(choice)))
            else:  # AI2's turn
                weights = ai2_w[board_size - 1]
                valid_choices = [c for c in CHOICES if c <= board_size]
                valid_weights = [max(1, weights[CHOICES.index(c)]) for c in valid_choices]
                choice = choices(valid_choices, valid_weights, k=1)[0]
                ai2_steps.append((board_size, CHOICES.index(choice)))
        else:
            if current_turn:  # Player's turn
                print("\nYour turn!")
                print("Choose sticks to remove (1, 2, or 3):")
                
                valid_move = False
                while not valid_move:
                    try:
                        choice = int(input("> "))
                        if choice not in CHOICES:
                            print(f"Invalid choice. Please enter {', '.join(map(str, CHOICES))}:")
                        elif choice > board_size:
                            print(f"Too many! Only {board_size} sticks remaining. Try again:")
                        else:
                            valid_move = True
                    except ValueError:
                        print("Please enter a valid number.")
            else:  # AI's turn
                print("\nAI's turn...")
                time.sleep(0.5)
                
                weights = ai1_w[board_size - 1]
                valid_choices = [c for c in CHOICES if c <= board_size]
                valid_weights = [max(1, weights[CHOICES.index(c)]) for c in valid_choices]
                choice = choices(valid_choices, valid_weights, k=1)[0]
                print(f"AI removes {choice} stick(s)")
        
        # Remove sticks
        for _ in range(choice):
            board.pop()
        
        if not is_training:
            if len(board) > 0:
                print(f"Board: {''.join(board)} ({len(board)} sticks remaining)")
            else:
                print("Board: (empty)")
        
        if len(board) == 0:
            if is_training:
                if current_turn:  # AI1 took the last stick and lost
                    # Update AI1's weights (penalize)
                    for size, step in ai1_steps:
                        if ai1_w[size - 1][step] > 0:
                            ai1_w[size - 1][step] -= 1
                    
                    # Update AI2's weights (reward)
                    for size, step in ai2_steps:
                        ai2_w[size - 1][step] += 1
                    
                    return 2  # AI2 wins
                else:  # AI2 took the last stick and lost
                    # Update AI2's weights (penalize)
                    for size, step in ai2_steps:
                        if ai2_w[size - 1][step] > 0:
                            ai2_w[size - 1][step] -= 1
                    
                    # Update AI1's weights (reward)
                    for size, step in ai1_steps:
                        ai1_w[size - 1][step] += 1
                    
                    return 1  # AI1 wins
            else:
                if current_turn:
                    print("\nGame over! You took the last stick, so you lose!")
                    return "AI"
                else:
                    print("\nGame over! AI took the last stick, so you win!")
                    return "Player"
        
        current_turn = not current_turn

# Train the AIs
print(f"Training AIs against each other for {TRAINING_GAMES:,} games...")
progress_step = max(1, TRAINING_GAMES // 100)  # Show progress at 1% intervals
start_time = time.time()

for game in range(TRAINING_GAMES):
    if game % progress_step == 0 or game == TRAINING_GAMES - 1:
        current_time = time.time()
        elapsed = current_time - start_time
        progress = (game + 1) / TRAINING_GAMES * 100
        games_per_sec = (game + 1) / elapsed if elapsed > 0 else 0
        remaining_games = TRAINING_GAMES - (game + 1)
        eta = remaining_games / games_per_sec if games_per_sec > 0 else 0
        eta_str = time.strftime("%H:%M:%S", time.gmtime(eta)) if eta > 0 else "--:--:--"
        
        print(f"Progress: {progress:.1f}% ({game + 1:,}/{TRAINING_GAMES:,}) | "
              f"Speed: {games_per_sec:,.0f} games/sec | "
              f"Elapsed: {time.strftime('%H:%M:%S', time.gmtime(elapsed))} | "
              f"ETA: {eta_str}")
    
    winner = play_game(ai1_weights, ai2_weights)
    
    if winner == 1:
        ai1_wins += 1
    else:
        ai2_wins += 1

training_time = time.time() - start_time

# Training results
print("\n--- Training completed ---")
print(f"Training time: {training_time:.2f} seconds ({training_time/60:.1f} minutes)")
print(f"Average speed: {TRAINING_GAMES/training_time:,.0f} games/second")
print(f"AI 1 wins: {ai1_wins:,} ({ai1_wins / TRAINING_GAMES * 100:.1f}%)")
print(f"AI 2 wins: {ai2_wins:,} ({ai2_wins / TRAINING_GAMES * 100:.1f}%)")

# Determine the winner
winner_weights = ai1_weights if ai1_wins >= ai2_wins else ai2_weights
winner_name = "AI 1" if ai1_wins >= ai2_wins else "AI 2"
print(f"\nThe winner is {winner_name}! You will play against this AI.")

# Player vs AI
player_first = input("\nDo you want to go first? (y/n): ").lower().startswith('y')

print(f"\n--- Playing against {winner_name} ---")
print("The goal is to avoid taking the last stick.")
print("On each turn, you can take 1, 2, or 3 sticks.")

game_result = play_game(winner_weights, ai2_weights, is_training=False, player_goes_first=player_first)

# Display learned strategy
print("\n--- Game Statistics ---")
print("\nLearned strategy (weights) for the winning AI:")
print("Sticks | Weight for taking 1 | Weight for taking 2 | Weight for taking 3")
print("-------|---------------------|---------------------|---------------------")
for i in range(1, min(11, INITIAL_STICKS + 1)):
    print(f"{i:6d} | {winner_weights[i-1][0]:19.1f} | {winner_weights[i-1][1]:19.1f} | {winner_weights[i-1][2]:19.1f}")
print("\nHint: In Nim with this setup, the optimal strategy is to leave a multiple of 4 sticks for your opponent!")