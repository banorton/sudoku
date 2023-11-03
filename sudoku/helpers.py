from math import ceil
from itertools import chain


def p2b(ppos, bdimo=(3, 3), bdimi=(3, 3)):
    brow = ceil((ppos[0] + 1) / bdimi[0]) - 1
    bcol = ceil((ppos[1] + 1) / bdimi[1]) - 1
    return (brow * bdimo[1]) + bcol


def transpose(arr):
    if not isinstance(arr[0], list):
        return [[el] for el in arr]
    else:
        return list(map(list, (zip(*arr))))


def flatten(arr):
    return list(chain.from_iterable(arr))
