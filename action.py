import numpy as np
import playingcard as pc


class Action:
    def __init__(self):
        self.pc = pc.PlayingCard()
        self.pots = np.zeros(13)

    def fold(self, playerhands, N):
        playerhands[N, :, :] = 0
        return playerhands

    def call(self):
        print("call")

    def raise_(self):
        print("raise")
