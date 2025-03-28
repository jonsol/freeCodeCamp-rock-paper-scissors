# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.

def player(prev_play, opponent_history=[], my_history=[], 
            play_order=[{
              "RR": 0,
              "RP": 0,
              "RS": 0,
              "PR": 0,
              "PP": 0,
              "PS": 0,
              "SR": 0,
              "SP": 0,
              "SS": 0,
             }]):

    if not my_history:
        my_history += ['R', 'S']
        return 'S'

    last_two = "".join(my_history[-2:])
    if len(last_two) == 2:
        play_order[0][last_two] += 1

    my_prev_play = my_history[-1]

    potential_plays = [
        my_prev_play + "R",
        my_prev_play + "P",
        my_prev_play + "S"
    ]git push --set-upstream origin

    sub_order = {
        k : play_order[0][k] for k in potential_plays if k in play_order[0]
    }

    next_play = min(sub_order, key=sub_order.get)[-1:]
    
    my_history.append(next_play)

    return next_play


# listabc = ['P', 'R', 'S']
# cde = listabc[-1]
# print(cde)