import random

def player(prev_play, history=[]):
    """
    RPS bot with:
      1) Cycle detector for short, exact repeats
      2) Variable‐order Markov patterns (4 → 3 → 2)
      3) Frequency analysis fallback
      4) 5% random noise
    """
    # Record last move
    if prev_play:
        history.append(prev_play)

    # Warm up with pure randomness until we have enough data
    if len(history) < 6:
        return random.choice(["R","P","S"])

    # Quick counter map
    counter = {"R":"P", "P":"S", "S":"R"}

    # 1) Cycle detection: check for an exact repeat of the last L‐move block
    for L in range(2, 7):  # look for cycles of length 2 up to 6
        if len(history) >= 2 * L:
            if history[-L:] == history[-2*L:-L]:
                # They just played a block of length L twice in a row → assume they’ll repeat it
                guess = history[-L]   # the first move of that block
                return counter[guess]

    # 2) Variable-order Markov: try patterns of length 4, then 3, then 2
    for seq_len in (4, 3, 2):
        if len(history) >= seq_len + 1:
            pattern = "".join(history[-seq_len:])
            following = [
                history[i+seq_len]
                for i in range(len(history)-seq_len)
                if "".join(history[i:i+seq_len]) == pattern
            ]
            if following:
                guess = max(set(following), key=following.count)
                return counter[guess]

    # 3) Frequency fallback
    counts = {m: history.count(m) for m in ("R","P","S")}
    most = max(counts, key=counts.get)
    play = counter[most]

    # 4) A dash of unpredictability
    if random.random() < 0.05:
        return random.choice(["R","P","S"])
    return play