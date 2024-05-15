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


