import random

# リストnumsの中に数値numが存在した場合True, しない場合Falseを返す
def ad (nums, num):
	for i in range(len(nums)):
		if num == nums[i]:
			return True
	return False

# プレイヤーAの手札格納
playerA = []
#ディラーの手札格納
master = []
# 配布するカードの識別
num = []
# 合計の配布枚数 人数*2+5にしたいね
cardsNums = 10

# 配布するカードの決定
while len(num) != 10:
	temp = random.randint(0, 52)
	while ad(num, temp):
		temp = random.randint(0, 52)
	num.append(temp)

# カードの配布 1:配布 0:未配布
for i in range(4):
	playerA.append([])
	for j in range(13):
		if ad(num, i*13+j):
			playerA[i].append(1)
		else:
			playerA[i].append(0)
	print (playerA[i])

def flash(player):
	for i in range(4):
		if sum(player[i])>= 5:
			jud = [i for i, x in enumerate(player[i]) if x == 1][:5]
			return jud
def countjudge(player):
	#数字に着目して何枚あるか調べる
	sum = []
	jud = []
	#sumに枚数の情報を追加していく
	for i in range(13):
		sum.append(0)
		for j in range(4):
			sum[i] += player[j][i]
	#４カードのとき
	if 4 in sum:
		for i in range(4):
			jud.append(sum.index(4))
		jud.append(sum.index(1))
    #３カードのとき
	elif 3 in sum:
		for i in range(3):
			jud.append(sum.index(3))
		#フルハウスか判定
		if 2 in sum:
			for i in range(2):
				jud.append(sum.index(2))
		else:
			jud.extend([i for i, x in enumerate(sum) if x == 1][:2])
	#１ペアもしくは２ペアのとき
	elif 2 in sum:
		if sum.count(2) >= 2:
			for i, x in enumerate(sum):
				if len(jud)<4:
					if x == 2:
						jud.extend([i,i])
			jud.append(sum.index(1))
		else:
			for i in range(2):
				jud.append(sum.index(2))
			jud.extend([i for i, x in enumerate(sum) if x == 1][:3])
	else:
		jud.extend([i for i, x in enumerate(sum) if x == 1][:5])
	#役をつくる５枚を返す！！！
	return jud
def straight(player):
	#数字に着目して何枚あるか調べる
	many = []
	jud = []
	for i in range(13):
		many.append(0)
		for j in range(4):
			many[i] += player[j][i]
	if many[0]>0 and all(many[9:13]):
			for j in range(4):
				if sum(player[j][9:13])+player[j][0] == 5:
					pass
			jud = [9,10,11,12,13]
	for i in range(9):
		if all(many[i:i+5]):
			for j in range(4):
				if sum(player[j][i:i+5]) == 5:
					jud = list(range(i,i+5))
					break
			if not jud or jud[0]>=i:
				jud = list(range(i,i+5))
	return jud
print(straight(playerA))
