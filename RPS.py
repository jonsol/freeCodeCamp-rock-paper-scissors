import random

def player(prev_play, opponent_history=[]):
    if prev_play:
        opponent_history.append(prev_play)
    
    if len(opponent_history) < 5:
        # Random play in the beginning
        return random.choice(["R", "P", "S"])
    
    # Let's introduce an adaptive strategy based on past opponent history
    move_prediction = predict_move(opponent_history)
    
    # Return the move that beats the predicted move
    return counter_move(move_prediction)

def predict_move(history):
    """
    Predict the opponent's next move using a basic strategy.
    For example, predict the opponent will repeat their last move most often.
    """
    # A simple strategy: check opponent's last 2 moves and predict the next one
    if len(history) > 1:
        last_two = history[-2:]
        if last_two[0] == last_two[1]:  # If last two moves are same, predict they repeat
            return last_two[0]
    return random.choice(["R", "P", "S"])

def counter_move(move):
    """Return the move that beats the predicted move."""
    beats = {"R": "P", "P": "S", "S": "R"}
    return beats[move]
