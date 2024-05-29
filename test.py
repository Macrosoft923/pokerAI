from PlayingCard import PlayingCard
from judclass3 import Judge
playingcard = PlayingCard()

dealerhands, playerhands = playingcard.getPokerHands(10)
from PlayingCard import PlayingCard as pc

pc = pc()
plynum = 10
dealercards, playerhands = pc.getPokerHands(plynum)

# judclass2 = Judge(playerhands)
# judclass2.judgement(playerhands)

print(dealercards)
print(playerhands)
print(playerhands.shape)
for i in range(plynum):
    ju = Judge(playerhands[i])
    print(ju.judge_hand())