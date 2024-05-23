from PlayingCard import PlayingCard
from judclass2 import Judge
playingcard = PlayingCard()
#Judge = Judge()
dealerhands, playerhands = playingcard.getPokerHands(10)

print(dealerhands)
print(playerhands)

