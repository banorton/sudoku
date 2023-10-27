import random

def easy(num=0, rand=False):
    assert isinstance(num, int)
    examples = dict()
    # fmt: off
    examples[0] = [9,0,0,3,0,2,6,0,0,4,0,7,0,0,8,9,1,3,6,0,3,1,0,0,0,5,4,0,3,0,0,8,0,4,7,0,0,0,8,0,3,0,1,6,0,0,0,4,2,0,0,5,0,0,8,7,1,9,0,6,0,4,5,3,0,0,0,5,0,0,0,0,2,0,0,4,0,0,0,0,1]
    # fmt: on

    if rand:
        return random.choice(examples)
    
    return examples[num]