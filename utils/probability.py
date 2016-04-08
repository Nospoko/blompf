import numpy as np
import bisect as bs

def cdf(weights):
    """ Cumulative distribution function """
    # Normalization, container, iterator
    total = sum(weights)
    result = []
    cumsum = 0.0

    # Construct
    for w in weights:
        cumsum += w
        result.append(cumsum / total)

    # Give back
    return result

def choice(normalized_weights):
    """ Returns id of randomly chosen weight """
    cdf_vals = cdf(normalized_weights)
    x = np.random.random()
    # Seems important
    idx = bs.bisect(cdf_vals, x)
    return idx

def randomly_draw(values, probabilities):
    """ Changes probability into reality """
    idx = choice(probabilities)
    return values[idx]

