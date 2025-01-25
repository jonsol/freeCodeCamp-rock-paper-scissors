# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.

def player(prev_play, opponent_history=[]):
    # Add the opponent's previous move to history
    if prev_play:
        opponent_history.append(prev_play)

    # Define the counter for each move
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}

    # Use pattern recognition by tracking last two plays
    if len(opponent_history) >= 2:
        last_two = "".join(opponent_history[-2:])
    else:
        last_two = ""

    # Predict the next move based on historical patterns
    play_order = {
        "RR": 0,
        "RP": 0,
        "RS": 0,
        "PR": 0,
        "PP": 0,
        "PS": 0,
        "SR": 0,
        "SP": 0,
        "SS": 0,
    }

    # Update play order frequencies
    for i in range(len(opponent_history) - 1):
        pair = "".join(opponent_history[i:i + 2])
        if pair in play_order:
            play_order[pair] += 1

    # Predict the opponent's next move
    potential_plays = [last_two[-1:] + "R", last_two[-1:] + "P", last_two[-1:] + "S"]
    prediction = max(potential_plays, key=lambda play: play_order.get(play[:2], 0))[-1:]

    # Return the ideal response to the predicted move
    return ideal_response[prediction] if prediction else "R"

