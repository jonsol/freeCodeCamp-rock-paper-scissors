import random

def player(prev_play, opponent_history=[], my_history=[]):
    if prev_play:
        opponent_history.append(prev_play)

    if hasattr(player, "last_move"):
        my_history.append(player.last_move)

    if not hasattr(player, "patterns"):
        player.patterns = {}

    if not hasattr(player, "reactive_mode"):
        player.reactive_mode = False
        player.reactive_count = 0

    patterns = player.patterns

    if len(opponent_history) < 3:
        guess = random.choice(["R", "P", "S"])
        player.last_move = guess
        return guess

    last_two = "".join(opponent_history[-2:])

    if last_two not in patterns:
        patterns[last_two] = {"R": 0, "P": 0, "S": 0}

    if len(opponent_history) >= 4:
        last_three = "".join(opponent_history[-3:-1])
        next_move = opponent_history[-1]
        if last_three not in patterns:
            patterns[last_three] = {"R": 0, "P": 0, "S": 0}
        patterns[last_three][next_move] += 1

    prediction = max(patterns[last_two], key=patterns[last_two].get)
    counter_moves = {"R": "P", "P": "S", "S": "R"}
    guess = counter_moves[prediction]

    # Detect reactive bot
    if len(my_history) >= 10:
        counter = {"R": "P", "P": "S", "S": "R"}
        beaten = sum(1 for my, opp in zip(my_history[-10:], opponent_history[-10:]) if opp == counter[my])

        if beaten >= 7:
            # Switch to random for next few rounds to break Abbey
            player.reactive_mode = True
            player.reactive_count = 5

    if player.reactive_mode:
        guess = random.choice(["R", "P", "S"])
        player.reactive_count -= 1
        if player.reactive_count <= 0:
            player.reactive_mode = False

    player.last_move = guess
    return guess
