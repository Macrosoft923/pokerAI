import numpy as np


def isclosed(active_players, pots, stacks):
    if np.count_nonzero(active_players) == 0:
        return True
    if all([pot == pots[active_players][0] for pot in pots[active_players]]):
        return True
    if all([stack == 0 for stack in stacks[active_players]]):
        return True


ACTIVE_PLAYERS = np.zeros(6, dtype=bool)
MIN_BET = 40
pots = np.zeros(6, dtype=np.int64)
pots[0] += MIN_BET // 2
pots[1] += MIN_BET

stacks = np.ones(6, dtype=np.int64) * MIN_BET * 100
stacks[0] -= MIN_BET // 2
stacks[1] -= MIN_BET

print(isclosed(ACTIVE_PLAYERS, pots, stacks))
