import random


def impossible(num=0, rand=False):
    assert isinstance(num, int)
    examples = dict()
    # fmt: off
    examples[0] = [8,0,0,0,0,0,0,0,0,0,0,3,6,0,0,0,0,0,0,4,0,0,9,0,2,0,0,0,5,0,0,0,7,0,0,0,0,0,0,0,4,5,7,0,0,0,0,0,1,0,0,0,3,0,0,0,1,0,0,0,0,6,8,0,0,8,5,0,0,0,1,0,0,9,0,0,0,0,4,0,0]
    # fmt: on

    if rand:
        return random.choice(examples)

    return examples[num]
