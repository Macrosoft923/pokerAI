from PlayingCard import PlayingCard as pc
from judclass2 import Judge

pc = pc()
dealercards, playerhands = pc.getPokerHands(5)

# judclass2 = Judge(playerhands)
# judclass2.judgement(playerhands)

print(dealercards)
print(playerhands)
print(playerhands.shape)
