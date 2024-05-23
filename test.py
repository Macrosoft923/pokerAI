from PlayingCard import PlayingCard as pc

pc = pc()
dealercards, playerhands = pc.getPokerHands(10)

print(dealercards)
print(playerhands)
