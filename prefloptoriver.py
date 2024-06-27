import random
from PlayingCard import PlayingCard as pc
from judclass3 import Judge
pc = pc()
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

#オリジナルレイザーを保持
lastraise = -1

#それぞれベットとチェックが行われたかを保持しておくリスト
hvbet = False
hvcehck = 0

bord = None
playercard = pc.ty_get_card(players, 2)
result = []
result1 = []
result2 = []
pre_flop = True
allin = False
flop = not pre_flop
PLAY = True
print(
    f"info    : players: \033[31m{players}\033[0m, your player number: \033[31m{my_player}\033[0m, button: \033[31m{button}\033[0m, small blind: \033[31m{small_blind}\033[0m, big blind: \033[31m{big_blind}\033[0m"
)

print(f"bets    : {bets}")
print(f"chips   : {chips}")
print(f"folded  : {folded}")

print()
print()


while PLAY:
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
                    print("your hand is")
                    print(pc.cardprint(playercard[player]))
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
    bord = pc.ty_get_card(1, 3)
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
                    turn = pc.ty_get_card(1, 1)
                    bord[0] += turn[0]
                    print("flop finish")
                    print()
                elif postflop == 3:
                    river = pc.ty_get_card(1, 1)
                    bord[0] += river[0]
                    print("turn finish")
                    print()
                if postflop == 4:
                    postflop = False
                    break
            if folded[player]:
                continue
            if sum(allined) == players - sum(folded):
                print("みんなオール・イン")
                if postflop == 2:
                    turn = pc.ty_get_card(1, 1)
                    bord[0] += turn[0]
                if postflop == 3:
                    river = pc.ty_get_card(1, 1)
                    bord[0] += river[0]
                postflop = False
                break
            if allined[player]:
                continue
            if player == my_player:
                while True:
                    print("your hand is")
                    print(pc.cardprint(playercard[player]))
                    print("bord card is")
                    print(pc.cardprint(bord[0]))
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
                        bet = chips[player]
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
                    if max_bet - bets[player] < chips[player]:
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


            print()

        print()
    for i in playercard:
        i += bord[0]
        jd = Judge(i) 
        result.append(jd.judge_hand())
    for i, j in result:
        result1.append(i)
        result2.append(j)
    for i in range(players):
        if folded[i]:
            result1[i] = -1

    print(result)
    print(result1)
    print(result2)
    winner = pc.judall(result1,result2)
    if len(winner)==1:
        print(f"winner: {winner}")
        chips[winner[0]] += pot
        pot = 0
    else:
        print(f"chop: {winner}")
        for i in winner:
            chips[i]+=pot/len(winner)
        pot = 0
    print(f"chips   : {chips}")

    button += 1
    winner = None
    small_blind = (button + 1) % players
    big_blind = (button + 2) % players

    bets = [0] * players
    bets[small_blind] = 1
    bets[big_blind] = 2
    max_bet = 2
    pot = 0

    chips[small_blind] -= 1
    chips[big_blind] -= 2

    folded = [False] * players
    allined = [False] * players

    lastraise = -1

    hvbet = False
    hvcehck = 0

    bord = None
    playercard = pc.ty_get_card(players, 2)
    result = []
    result1 = []
    result2 = []
    pre_flop = True
    allin = False
    flop = not pre_flop
    pc.counter = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]
    for i in range(players):
        if chips[i] <= 2:
            chips[i] = 200
        