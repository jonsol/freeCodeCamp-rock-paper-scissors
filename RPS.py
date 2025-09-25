# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.

def player(prev_play, opponent_history=[]):
   
    if prev_play != "":
        opponent_history.append(prev_play)

    
    if not opponent_history:
        return "R"

    
    freq = {"R": 0, "P": 0, "S": 0}
    for move in opponent_history:
        freq[move] += 1
    predicted = max(freq, key=freq.get)

  
    counter = {"R": "P", "P": "S", "S": "R"}
    return counter[predicted]
