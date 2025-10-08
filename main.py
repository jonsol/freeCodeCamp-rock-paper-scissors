# This entrypoint file to be used in development. Start by reading README.md
from RPS_game import play, mrugesh, abbey, quincy, kris, human, random_player
from RPS import player
from unittest import main
from itertools import product
import random

# Uncomment line below to play interactively against a bot:
# play(human, abbey, 20, verbose=True)

# Uncomment line below to play against a bot that plays randomly:
# play(human, random_player, 1000)


# Copy Abbey as she is a 2nd order markov chain algorithm and change it to 3rd order markov with decaying factor
def player_1(
    prev_opponent_play,
    opponent_history=[],
    play_order=[{}],
    decay_rate=0.99  # how quickly old data fades (closer to 1 = slower decay)
):

    if not prev_opponent_play:
        prev_opponent_play = 'S'

    # Add to history
    opponent_history.append(prev_opponent_play)

    #Play order for 3rd order
    if not play_order[0]:
        moves = ['R', 'P', 'S']
        for seq in product(moves, repeat=4):
            play_order[0]["".join(seq)] = 0.0

    # Apply decay to all counts
    for k in play_order[0]:
        play_order[0][k] *= decay_rate

    # Update transition table if enough history
    if len(opponent_history) > 3:
        last_four = "".join(opponent_history[-4:])
        play_order[0][last_four] += 1

    # Get last 3 moves as the current state
    if len(opponent_history) >= 3:
        last_three = "".join(opponent_history[-3:])
    else:
        return random.choice(['R', 'P', 'S'])

    # Possible next moves from this state
    #potential_plays = [last_three + "R", last_three + "P", last_three + "S"]
    potential_plays = [last_three + nxt for nxt in ['R', 'P', 'S']]
    #potential_plays = [last_two + "R", last_two + "P", last_two + "S"]
    sub_order = {k: play_order[0][k] for k in potential_plays}

    # Predict opponent's next move = the one with highest decayed frequency
    prediction = max(sub_order, key=sub_order.get)[-1]

    # Choose counter move
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    return ideal_response[prediction]


play(player_1, quincy, 10000)
play(player_1, mrugesh, 10000)
play(player_1, abbey, 10000)
play(player_1, kris, 10000)


# Uncomment line below to run unit tests automatically
main(module='test_module', exit=False)