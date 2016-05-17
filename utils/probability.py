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
    # Seems important (can fuck things up though on the right edge)
    idx = bs.bisect(cdf_vals, x)
    return idx

def randomly_draw(values, probabilities):
    """ Changes probability into reality """
    idx = choice(probabilities)

    if idx >= len(values):
        idx = len(values)-1
        idx = 0
        print 'halp | randomly_draw()'
    return values[idx]

def cauchy_pdf(x0, gamma):
    """ Create probability density function """
    def pdf(x):
        part_a = ((x - x0) / gamma)**2
        part_b = (1.0 + part_a)

        return 1.0 / part_b

    return pdf

def tomek_pdf(x0):
    """ Creates pdf of my design """
    gamma = 5
    def pdf(x):
        if x0 < 0:
            return 1
        else:
            cauchy = cauchy_pdf(x0, gamma)
            part_a = 0.1 + np.sqrt(gamma)/10.0
            part_b = cauchy(x)

            return part_a + part_b

    return pdf
