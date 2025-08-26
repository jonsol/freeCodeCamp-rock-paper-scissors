def player(prev_play, opponent_history=[], 
           play_order=[{"RR": 0, "RP": 0, "RS": 0,
                        "PR": 0, "PP": 0, "PS": 0,
                        "SR": 0, "SP": 0, "SS": 0}],
           strategy_scores=[0, 0, 0, 0],
           player_history=[]):
    
    # Initialize on first move
    if prev_play == '':
        opponent_history.clear()
        player_history.clear()
        play_order[0] = {k: 0 for k in play_order[0]}
        strategy_scores[:] = [0] * 4  # Reset scores: [Quincy, Mrugesh, Kris, Abbey]
        return "P"  # Start with Paper

    opponent_history.append(prev_play)
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}

    # -----------------------------
    # Strategy 1: Counter Quincy (predictable cycle: R, R, P, P, S)
    # -----------------------------
    quincy_moves = ["R", "R", "P", "P", "S"]
    quincy_choice = quincy_moves[len(opponent_history) % 5]
    if ideal_response[quincy_choice] == prev_play:
        strategy_scores[0] += 1  # We beat Quincy → this strategy works
    else:
        strategy_scores[0] -= 1

    # -----------------------------
    # Strategy 2: Counter Mrugesh (beat most frequent in last 10)
    # -----------------------------
    last_ten = opponent_history[-10:]
    if len(last_ten) >= 1 and '' not in last_ten:
        most_frequent = max(['R','P','S'], key=last_ten.count)
        mrugesh_choice = ideal_response[most_frequent]
    else:
        mrugesh_choice = "P"
    
    if ideal_response[mrugesh_choice] == prev_play:
        strategy_scores[1] += 1
    else:
        strategy_scores[1] -= 1

    # -----------------------------
    # Strategy 3: Counter Kris (always counters your last move)
    # -----------------------------
    if len(player_history) > 0:
        kris_choice = ideal_response[player_history[-1]]
    else:
        kris_choice = "S"  # Kris assumes you start with R → plays S
    if ideal_response[kris_choice] == prev_play:
        strategy_scores[2] += 1
    else:
        strategy_scores[2] -= 1

    # -----------------------------
    # Strategy 4: Counter Abbey (Markov chain of pairs)
    # -----------------------------
    if len(opponent_history) > 1:
        last_two = "".join(opponent_history[-2:])
        play_order[0][last_two] += 1

        potential_plays = [
            opponent_history[-1] + "R",
            opponent_history[-1] + "P",
            opponent_history[-1] + "S"
        ]
        sub_order = {k: play_order[0].get(k, 0) for k in potential_plays}
        prediction = max(sub_order, key=sub_order.get)[-1]
        abbey_choice = ideal_response[prediction]
    else:
        abbey_choice = "P"

    if ideal_response[abbey_choice] == prev_play:
        strategy_scores[3] += 1
    else:
        strategy_scores[3] -= 1

    # Keep only recent performance (last 20 rounds)
    if len(opponent_history) > 20:
        # Normalize score decay to avoid overflow
        strategy_scores[:] = [score - min(strategy_scores) for score in strategy_scores]

    # Choose the best-performing strategy
    best_strategy_idx = strategy_scores.index(max(strategy_scores))

    # Now predict what that bot will do next, and counter it
    if best_strategy_idx == 0:
        # Quincy: deterministic cycle
        next_opponent_play = quincy_moves[(len(opponent_history) + 1) % 5]
    elif best_strategy_idx == 1:
        # Mrugesh: most frequent in last 10
        last_ten = opponent_history[-10:]
        most_freq = max(['R','P','S'], key=lambda x: last_ten.count(x))
        next_opponent_play = most_freq
    elif best_strategy_idx == 2:
        # Kris: counters your last move
        my_last = player_history[-1] if player_history else "R"
        next_opponent_play = ideal_response[my_last]
    else:  # best_strategy_idx == 3
        # Abbey: Markov prediction
        if len(opponent_history) > 0:
            hist = opponent_history[-1]
            potential = [hist + "R", hist + "P", hist + "S"]
            sub = {k: play_order[0].get(k, 0) for k in potential}
            next_opponent_play = max(sub, key=sub.get)[-1]
        else:
            next_opponent_play = "R"

    # Beat the predicted move
    guess = ideal_response[next_opponent_play]

    # Record your own move for next round (Kris & Abbey depend on it)
    player_history.append(guess)

    return guess
