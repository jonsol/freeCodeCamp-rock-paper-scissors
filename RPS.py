def player(prev_play, opponent_history=[]):
    # Append the opponent's last move to the history
    opponent_history.append(prev_play)

    # Define the number of games after which we analyze patterns
    ANALYSIS_THRESHOLD = 10

    # Define the winning moves
    WINNING_MOVES = {"R": "P", "P": "S", "S": "R"}

    # Strategy: Play randomly for the first few moves to gather data
    if len(opponent_history) <= ANALYSIS_THRESHOLD:
        return "R"  # Default to "R" for the first few moves

    # Strategy 1: Detect Repetitive Patterns
    if len(opponent_history) > ANALYSIS_THRESHOLD:
        # Check if the opponent repeats the same move
        last_moves = opponent_history[-ANALYSIS_THRESHOLD:]
        if len(set(last_moves)) == 1:  # All moves are the same
            return WINNING_MOVES[last_moves[0]]

    # Strategy 2: Detect Cyclic Patterns
    if len(opponent_history) > ANALYSIS_THRESHOLD:
        # Check for a cycle of length 2 or 3
        cycle_length_2 = opponent_history[-2:] == opponent_history[-4:-2]
        cycle_length_3 = opponent_history[-3:] == opponent_history[-6:-3]

        if cycle_length_2:
            predicted_move = opponent_history[-1]  # Predict the next move in the cycle
            return WINNING_MOVES[predicted_move]

        if cycle_length_3:
            predicted_move = opponent_history[-1]  # Predict the next move in the cycle
            return WINNING_MOVES[predicted_move]

    # Strategy 3: Frequency Analysis
    if len(opponent_history) > ANALYSIS_THRESHOLD:
        # Count the frequency of each move
        move_counts = {"R": 0, "P": 0, "S": 0}
        for move in opponent_history:
            if move in move_counts:
                move_counts[move] += 1

        # Predict the most frequent move and counter it
        most_frequent_move = max(move_counts, key=move_counts.get)
        return WINNING_MOVES[most_frequent_move]

    # Default Strategy: Random Guess (fallback)
    import random
    return random.choice(["R", "P", "S"])
