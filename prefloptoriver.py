import random

players = 6
while True:
    my_player = int(input("Please enter your player number: "))

    if 0 <= my_player <= players - 1:
        break

button = random.randint(0, players - 1)
winner = None
small_blind = (button + 1) % players
big_blind = (button + 2) % players

bets = [0] * players
bets[small_blind] = 1
bets[big_blind] = 2
max_bet = 2
pot = 0

chips = [200] * players
chips[small_blind] -= 1
chips[big_blind] -= 2

folded = [False] * players
allined = [False] * players

lastraise = -1

hvbet = False
hvcehck = 0

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
allin = False
flop = not pre_flop

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
            """
            アクションの判断基準を作るファイルを作ってここに追加してアップデートかな
            """
        while True:
            if action == "CALL":
                if max_bet >= bets[player]+chips[player]:
                    action = "ALL-IN CALL"
                    bet = max_bet - bets[player]
                    bets[player] += bet
                    chips[player] -= bet
                    allined[player] = True
                else:
                    bet = max_bet - bets[player]
                    bets[player] += bet
                    chips[player] -= bet
                    if bet == 0:
                        action = "CHECK"
                        pre_flop = False #プリフロリンプでBBまで回ってきたときだけこのCheck使うかな
                break

            elif action == "RAISE" and max_bet * 2 - bets[player] > chips[player]:
                if max_bet < chips[player] + bets[player]:
                    action = "RAISE ALL-IN"
                    bet = chips[player]
                    bets[player] += bet
                    max_bet = max(bets)
                    chips[player] -= bet
                    lastraise = player
                    allined[player] = True
                    break
                else:
                    action = "ALL-IN CALL"
                    bet = chips[player]
                    bets[player] += bet
                    max_bet = max(bets)
                    chips[player] -= bet
                    allined[player] = True
                    break

            elif action == "RAISE" and max_bet * 2 - bets[player] <= chips[player]:
                if player == my_player:
                    while True:
                        bet = int(input("Please enter bet: "))

                        if max_bet * 2 - bets[player] <= bet <= chips[player]:
                            break
                else:
                    bet = random.randint(max_bet * 2 - bets[player], chips[player])
                    if bet == chips[player]:
                        action = "RAISE ALL-IN"
                        allined[player] = True

                bets[player] += bet
                max_bet = max(bets)
                chips[player] -= bet
                lastraise = player
                break

            elif action == "FOLD":
                bet = 0
                folded[player] = True
                break


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

    print()

print(f"winner: {winner}")
print("preflop finish")
lastraise = -1
pot += sum(bets)
bets = [0 for _ in bets]
postflop = 1
max_bet = 0

while postflop:
    for player in range(players):
        player = (player + button + 1) % players
        if lastraise == player:
            lastraise = -1
            pot += sum(bets)
            bets = [0 for _ in bets] 
            max_bet = 0
            hvcehck = 0
            postflop +=1
            hvbet = False
            if postflop == 2:
                print("flop finish")
                print()
            elif postflop == 3:
                print("turn finish")
                print()
            if postflop == 4:
                postflop = False
                break
        if folded[player]:
            continue

        if sum(allined) == players - sum(folded) or sum(allined) == players - sum(folded)-1:
            print("みんなオール・イン")
            postflop = False
            break
        if player == my_player:
            while True:
                action = str(input("Please enter your action: "))

                if hvbet:
                    if action in ["CALL", "RAISE", "FOLD"]:
                        break
                else:
                    if action in ["CHECK", "BET", "FOLD"]:
                        break
        else:
            """
            アクションの判断基準を作るファイルを作ってここに追加してアップデートかな
            """
            if hvbet:
                action = random.choices(["CALL", "RAISE", "FOLD"], weights=[10, 2, 1])[0]
            else:
                action = random.choices(["CHECK", "BET", "FOLD"], weights=[2, 2, 0])[0]
        
            
        while True:
            if action == "CALL":
                if max_bet >= bets[player]+chips[player]:
                    action = "ALL-IN CALL"
                    bet = max_bet - bets[player]
                    bets[player] += bet
                    chips[player] -= bet
                    allined[player] = True
                else:
                    bet = max_bet - bets[player]
                    bets[player] += bet
                    chips[player] -= bet
                    if bet == 0:
                        action = "CHECK"
                        pre_flop = False #プリフロリンプでBBまで回ってきたときだけこのCheck使うかな
                break

            elif action == "RAISE" and max_bet * 2 - bets[player] > chips[player]:
                if max_bet <chips[player]:
                    action = "RAISE ALL-IN"
                    bet = chips[player]
                    bets[player] += bet
                    max_bet = max(bets)
                    chips[player] -= bet
                    lastraise = player
                    allined[player] = True
                else:
                    action = "ALL-IN CALL"
                    bet = max_bet - bets[player]
                    bets[player] += bet
                    chips[player] -= bet
                    allined[player] = True
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
                lastraise = player
                break
           
            elif action == "CHECK":
                hvcehck += 1
                if hvcehck == 1:
                    lastraise = player
                break

            elif action == "BET":
                if player == my_player:
                    while True:
                        bet = int(input("Please enter bet: "))

                        if bet < chips[player]:
                            break
                        elif bet == chips[player]:
                            action == "ALL-in"
                            allined[player] = True
                            break
                else:
                    bet = random.randint(1,chips[player])
                bets[player] += bet
                max_bet = max(bets)
                chips[player] -= bet
                lastraise = player
                hvbet = True
                break

            elif action == "FOLD":
                folded[player] = True
                break
        if folded.count(False) == 1:
            print("winner")
            winner = folded.index(False)
            pre_flop = False

        print(
            f"info    : player: \033[31m{player}\033[0m, action: \033[31m{action}\033[0m, bet: \033[31m{bet}\033[0m, max_bet: \033[31m{max_bet}\033[0m, chips[player]: \033[31m{chips[player]}\033[0m, pot: \033[31m{pot}\033[0m"
        )
        print(f"bets    : {bets}")
        print(f"chips   : {chips}")
        print(f"folded  : {folded}")
        print(f"aaaa  : {allined}")


        print()

    print()

print(f"winner: {winner}")
