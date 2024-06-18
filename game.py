import random

MIN_PLAYERS = 5
MAX_PLAYERS = 10
POINTS = 200

players = random.randint(MIN_PLAYERS, MAX_PLAYERS)
# gamer = random.randint(0, players - 1)
button = random.randint(0, players - 1)

winner = None

small_blind = (button + 1) % players
big_blind = (button + 2) % players

bets = [0] * players
bets[small_blind] = 1
bets[big_blind] = 2
max_bet = 2

banks = [POINTS] * players
banks[small_blind] -= 1
banks[big_blind] -= 2

folded = [False] * players

print(
    f"info    : players: \033[31m{players}\033[0m, your player number: \033[31m[gamer]\033[0m, button: \033[31m{button}\033[0m, small blind: \033[31m{small_blind}\033[0m, big blind: \033[31m{big_blind}\033[0m"
)
print(f"bets    : {bets}")
print(f"banks   : {banks}")
print(f"folded  : {folded}")

print()
print("-" * 90)
print()


def play_game():
    global pre_flop, last_raise, closed_count, max_bet, winner

    for i in range(players):
        player = (i + button + 3) % players

        if last_raise == player:
            return False

        if folded[player]:
            continue

        # if player == gamer:
        #     while True:
        #         action = str(input("Please enter your action: "))

        #         if action in ["CALL", "RAISE", "FOLD"]:
        #             break
        # else:
        #     action = random.choices(["CALL", "RAISE", "FOLD"], weights=[10, 2, 1])[0]

        action = random.choices(["CALL", "RAISE", "FOLD"], weights=[1, 2, 10])[0]

        if action == "CALL":
            bet = max_bet - bets[player]
            bets[player] += bet
            banks[player] -= bet
            closed_count += 1

            if bet == 0:
                action = "CHECK"
                return False

        elif action == "RAISE" and banks[player] < max_bet * 2 - bets[player]:
            action = "ALL-IN"
            bet = banks[player]
            bets[player] += bet
            max_bet = max(bets)
            banks[player] -= bet
            closed_count = 0
            last_raise = player

        elif action == "RAISE" and banks[player] >= max_bet * 2 - bets[player]:
            # if player == gamer:
            #     while True:
            #         bet = int(input("Please enter bet: "))

            #         if max_bet * 2 - bets[player] <= bet <= banks[player]:
            #             break
            # else:
            #     bet = random.randint(max_bet * 2 - bets[player], banks[player])

            bet = random.randint(max_bet * 2 - bets[player], banks[player])
            bets[player] += bet
            max_bet = max(bets)
            banks[player] -= bet
            closed_count = 0
            last_raise = player

        else:
            bet = 0
            folded[player] = True

        print(
            f"info    : player: \033[31m{player}\033[0m, action: \033[31m{action}\033[0m, bet: \033[31m{bet}\033[0m, max_bet: \033[31m{max_bet}\033[0m, banks[{player}]: \033[31m{banks[player]}\033[0m"
        )
        print(f"bets    : {bets}")
        print(f"banks   : {banks}")
        print(f"folded  : {folded}")

        print()

        if folded.count(False) == closed_count - 1:
            pre_flop = False
            return False

        if folded.count(False) == 1:
            winner = folded.index(False)
            pre_flop = False
            return False

    return True


def play_game_stage(stage_name):
    global last_raise, closed_count, max_bet
    print(f"STAGE  : {stage_name}")
    print()
    print("-" * 90)
    print()
    stage_active = True
    last_raise = -1
    closed_count = 0

    while stage_active:
        stage_active = play_game()

    print("-" * 90)
    print()
    print(f"End of {stage_name}")
    print()


pre_flop = True
play_game_stage("Pre-Flop")

# フロップ、ターン、リバーラウンドの進行
if not winner:
    play_game_stage("Flop")

if not winner:
    play_game_stage("Turn")

if not winner:
    play_game_stage("River")

# 勝者の表示
print(f"winner: {winner}")
