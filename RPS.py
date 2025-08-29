# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.
import random

def analyze_transitions(history):
    
    transitions = {'R': {'R': 0, 'P': 0, 'S': 0},
                   'P': {'R': 0, 'P': 0, 'S': 0},
                   'S': {'R': 0, 'P': 0, 'S': 0}}

    for i in range(len(history) - 1):
        current_move = history[i]
        next_move = history[i+1]
        if current_move in transitions and next_move in transitions[current_move]:
            transitions[current_move][next_move] += 1

    return transitions

def predict_next_move_from_transitions(last_move, transitions):
    
    if last_move in transitions:
        next_moves = transitions[last_move]
        # Find the move with the maximum count
        if any(next_moves.values()):
            predicted_move = max(next_moves, key=next_moves.get)
            return predicted_move
        else:
            # No transitions recorded for this last move
            return None
    else:
        # Last move not in transition keys (shouldn't happen with R, P, S)
        return None

###################################_STRATEGY_#########################################

def player(prev_play, opponent_history=[]):
    opponent_history.append(prev_play)

    #STRATEGY 0: random choice
    moves = ['R', 'P', 'S']
    guess = random.choice(moves)
    
    #STRATEGY I: if the move is the same
    if len(opponent_history) > 2:
        #guess = opponent_history[-2]
        if opponent_history[-1] == opponent_history[-2]:
            likely_opponent_move = opponent_history[-1]
      # Return the move that beats the likely opponent move
            
            if likely_opponent_move == 'R':
                guess ='P'
            elif likely_opponent_move == 'P':
                guess = 'S'
            else: # likely_opponent_move == 'S'
                guess = 'R' 

    return guess
    
    #STRATEGY II: if there is a pattern
    if len(opponent_history) >= 3:
      last_three = opponent_history[-3:]
      # Check for R, P, S pattern
      if last_three == ['R', 'P', 'S']: #likely_opponent_move = 'R'
          guess = 'P'
      # Check for P, S, R pattern
      elif last_three == ['P', 'S', 'R']: #likely_opponent_move = 'P'
          guess = 'S'
      # Check for S, R, P pattern
      elif last_three == ['S', 'R', 'P']: #likely_opponent_move = 'S'
          guess = 'R'
    return guess

    
    #STRATEGY III: trying to predict the move
    if len(opponent_history) >= 4:
        transitions = analyze_transitions(opponent_history)
        last_move = opponent_history[-1]
        
        next_move_guess = predict_next_move_from_transitions(last_move, transitions)
        
        if next_move_guess == 'R':
            guess ='P'
        elif next_move_guess == 'P':
            guess = 'S'
        else: # likely_opponent_move == 'S'
            guess = 'R'

    return guess
