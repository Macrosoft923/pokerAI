import random
import time

MIN_PLAYERS = 5
MAX_PLAYERS = 10
# players = int(input("Please enter players: "))
# players = random.randint(2, 10)
players = random.randint(MIN_PLAYERS, MAX_PLAYERS)
# while True:
#     my_player = int(input("Please enter your player: "))

#     if MIN_PLAYERS <= players <= MAX_PLAYERS:
#         break
my_player = 4

dealer = random.randint(0, players - 1)
winner = None
small_blind = (dealer + 1) % players
big_blind = (dealer + 2) % players

bets = [0] * players
bets[small_blind] = 1
bets[big_blind] = 2
max_bet = 2

chips = [200] * players
chips[small_blind] -= 1
chips[big_blind] -= 2

fold = [False] * players

print(
    f"players: {players}, your player: {my_player}, dealer: {dealer}, small_blind: {small_blind}, big_blind: {big_blind}"
)
print(bets)
print(fold)

print()
print()

pre_flop = True
while pre_flop:
    for player in range(players):
        player = (player + dealer + 3) % players

        if fold[player]:
            continueß
        if chips[player] < max_bet:
             action = "FOLD"
        else:
            action = random.choices(["CALL", "RAISE", "FOLD"], weights=[1, 1, 6])[0]

        if action == "CALL":
            bet = max_bet - bets[player]
            bets[player] += bet
            chips[player] -= bet

        if action == "RAISE":
            # if player == my_player:
            #     while True:
            #         bet = int(input("Please enter bet: "))

            #         if max_bet * 2 - bets[player] <= bet <= chips[player]:
            #             break
            # else:
            #     bet = random.randint(max_bet * 2 - bets[player], chips[player])

            bet = random.randint(max_bet * 2 - bets[player], chips[player])
            bets[player] += bet
            max_bet = max(bets)
            chips[player] -= bet

        if action == "FOLD":
            bet = 0
            bets[player] = bet
            fold[player] = True

        if fold.count(False) == 1:
            winner = fold.index(False)
            pre_flop = False

        print(
            f"player: {player}, action: {action}, bet: {bet}, max_bet: {max_bet}, chips[player]: {chips[player]}"
        )

        print(bets)
        print(chips)
        print(fold)

        print()

        # time.sleep(1)

    if bets.count(max_bet) == fold.count(False):
        pre_flop = False

    print()

print(f"winner: {winner}")
