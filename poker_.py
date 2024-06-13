import random

MIN_PLAYERS = 5
MAX_PLAYERS = 10
# players = int(input("Please enter players: "))
# players = random.randint(2, 10)
players = random.randint(MIN_PLAYERS, MAX_PLAYERS)
while True:
    my_player = int(input("Please enter your player number: "))

    if 0 <= my_player <= players - 1:
        break
# my_player = 4

button = random.randint(0, players - 1)
winner = None
small_blind = (button + 1) % players
big_blind = (button + 2) % players

bets = [0] * players
bets[small_blind] = 1
bets[big_blind] = 2
max_bet = 2

chips = [200] * players
chips[small_blind] -= 1
chips[big_blind] -= 2

folded = [False] * players

lastraise = -1

print(
    f"info    : players: \033[31m{players}\033[0m, your player number: \033[31m{my_player}\033[0m, button: \033[31m{button}\033[0m, small blind: \033[31m{small_blind}\033[0m, big blind: \033[31m{big_blind}\033[0m"
)

print(f"bets    : {bets}")
print(f"chips   : {chips}")
print(f"folded  : {folded}")

print()
print()

pre_flop = True
closed_count = 0


while pre_flop:
    for player in range(players):
        player = (player + button + 3) % players
        if lastraise == player:
            pre_flop = False
            break
        if folded[player]:
            continue

        if player == my_player:
            while True:
                action = str(input("Please enter your action: "))

                if action in ["CALL", "RAISE", "FOLD"]:
                    break
        else:
            action = random.choices(["CALL", "RAISE", "FOLD"], weights=[10, 2, 1])[0]

        while True:
            if action == "CALL":
                bet = max_bet - bets[player]
                bets[player] += bet
                chips[player] -= bet
                closed_count += 1
                if bet == 0:
                    action = "CHECK"
                    pre_flop = False
                break

            elif action == "RAISE" and max_bet * 2 - bets[player] > chips[player]:
                action = "ALL-IN"
                bet = chips[player]
                bets[player] += bet
                max_bet = max(bets)
                chips[player] -= bet
                closed_count = 0
                lastraise = player
                break

            elif action == "RAISE" and max_bet * 2 - bets[player] <= chips[player]:
                if player == my_player:
                    while True:
                        bet = int(input("Please enter bet: "))

                        if max_bet * 2 - bets[player] <= bet <= chips[player]:
                            break
                else:
                    bet = random.randint(max_bet * 2 - bets[player], chips[player])

                bets[player] += bet
                max_bet = max(bets)
                chips[player] -= bet
                closed_count = 0
                lastraise = player
                break

            elif action == "FOLD":
                folded[player] = True
                break

        
        if folded.count(False) == closed_count - 1:
            print("closed 1")
            pre_flop = False

        if folded.count(False) == 1:
            print("winner")
            winner = folded.index(False)
            pre_flop = False

        print(
            f"info    : player: \033[31m{player}\033[0m, action: \033[31m{action}\033[0m, bet: \033[31m{bet}\033[0m, max_bet: \033[31m{max_bet}\033[0m, chips[player]: \033[31m{chips[player]}\033[0m"
        )

        print(f"bets    : {bets}")
        print(f"chips   : {chips}")
        print(f"folded  : {folded}")

        print()

        # time.sleep(1)

    if folded.count(False) == closed_count - 1:
        print("closed 2")
        pre_flop = False

    print()

print(f"winner: {winner}")
