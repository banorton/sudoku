import random

def hard(num=0, rand=False):
    assert isinstance(num, int)
    examples = dict()
    # fmt: off
    examples[0] = [0,0,0,0,0,7,0,0,6,0,9,4,0,3,0,0,0,0,0,0,0,0,0,1,2,0,0,1,0,0,0,8,0,0,0,0,0,0,0,0,0,2,8,3,1,7,0,0,0,1,0,0,4,9,0,0,0,0,0,0,0,0,5,5,0,1,9,0,0,0,6,3,0,7,0,0,6,0,9,2,8]
    # fmt: on

    if rand:
        return random.choice(examples)
    
    return examples[num]