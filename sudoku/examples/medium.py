import random

def medium(num=0, rand=False):
    assert isinstance(num, int)
    examples = dict()
    # fmt: off
    examples[0] = [0,0,6,4,1,0,0,7,0,5,0,0,0,6,3,4,0,0,0,3,0,0,0,0,0,0,0,0,6,4,0,0,1,0,0,0,0,0,3,6,0,2,0,0,0,0,8,2,5,0,9,0,1,3,0,4,0,0,0,0,8,0,0,0,2,0,0,0,0,0,0,0,3,7,0,2,8,4,1,0,0]
    # fmt: on

    if rand:
        return random.choice(examples)
    
    return examples[num]