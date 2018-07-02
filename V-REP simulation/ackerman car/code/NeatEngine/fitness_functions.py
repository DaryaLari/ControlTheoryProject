def distance(states):
    fitness = 0
    for state in states:
        fitness += state[0] * state[1]

    return fitness