import json

if __name__ == "Agent":
    from utils.game import *
    from utils.network import *
else:
"""An Agent that chooses a valid response at random."""

import sys, random

if "." not in __name__:
    from utils.game import *
#     from utils.network import *
    from Agent import Agent
else:
    from .utils.game import *
#     from .utils.network import *
    from .Agent import Agent

class RandomAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def decide_action(self, options):
        possible_actions = possible_responses(options)
        action = random.choice(possible_actions)
        if isinstance(options[action], list):
            target = random.choice(options[action])
            return convert(action, target)
        return convert(action)

if __name__ == "__main__":
    start(RandomAgent(), sys.argv[1])
