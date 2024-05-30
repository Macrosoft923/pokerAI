from judclass3 import Judge
from PlayingCard import PlayingCard as pc

pc = pc()
plynum = 3
dealercards= pc.get_dealer_cards()
playerhands = pc.get_player_hands(dealercards,plynum)

# judclass2 = Judge(playerhands)
# judclass2.judgement(playerhands)

print(dealercards)
print(playerhands)
print(playerhands.shape)
for i in range(plynum):
    ju = Judge(playerhands[i])
    print(ju.judge_hand())
import numpy as np
from PlayingCard import PlayingCard as pc

pc = pc()

dealercards = pc.get_dealer_cards()
playerhands = pc.get_player_hands(dealercards, 10)

print(np.zeros(13))
