import logging


def power(base, exponent):
    if exponent > 1000:
        logging.warn('Large power used.')
    if exponent < 0:
        raise ValueError(
            'Negative exponent unsupported')
    result = 1
    for _ in xrange(exponent):
        result *= base
    return result
