class Judge:
    def __init__(self,player):
        #カードの数字が何枚あるかなリスト
        self.many = []
        #勝負する５枚のリスト
        self.jud = []
        #何枚あるか計算する
        for i in range(13):
            self.many.append(0)
            for j in range(4):
                self.many[i] += player[j][i]
        #ストフラ９、４カード８、フルハウス７、フラッシュ６、ストレート５、３カード４、２ペア３、１ペア２、ハイカード１
        self.judnum = 0
    def judgement(self,player):
        #フラッシュを調べる
        if self.judnum<=6:
            for i in range(4):
                if sum(player[i])>= 5:
                    if self.judnum<=6:
                        self.jud = [i for i, x in enumerate(player[i]) if x == 1][:5]
                        self.judnum = 6
    #枚数系の役を調べる
        #４カードのとき
        if self.judnum<=8:
            if 4 in self.many:
                for i in range(4):
                    self.jud.append(self.many.index(4))
                self.jud.append(self.many.index(1))
                self.judnum = 8
            #３カードのとき
            elif 3 in self.many:
                if self.judnum<=4:
                    for i in range(3):
                        self.jud.append(self.many.index(3))
                    self.jud.extend([i for i, x in enumerate(self.many) if x == 1][:2])
                    self.judnum = 4
            #フルハウスか判定
            elif 3 in self.many:
                if self.judnum<=7:
                    for i in range(3):
                        self.jud.append(self.many.index(3))
                    if 2 in self.many:
                        for i in range(2):
                            self.jud.append(self.many.index(2))
                    self.judnum = 7
                
                    
            #１ペアもしくは２ペアのとき
            elif 2 in self.many:
                if self.judnum<=3:
                    if self.many.count(2) >= 2:
                        for i, x in enumerate(self.many):
                            if len(self.jud)<4:
                                if x == 2:
                                    self.jud.extend([i,i])
                        self.jud.append(self.many.index(1))
                        self.judnum = 3
                    else:
                        for i in range(2):
                            self.jud.append(self.many.index(2))
                        self.jud.extend([i for i, x in enumerate(self.many) if x == 1][:3])
                        self.judnum = 2
            else:
                if self.judnum<=1:
                    self.jud.extend([i for i, x in enumerate(self.many) if x == 1][:5])
                    self.judnum = 1
    #ストレートとストフラ調査所
        if self.many[0]>0 and all(self.many[9:13]):
                for j in range(4):
                    if sum(player[j][9:13])+player[j][0] == 5:
                        self.jud = [9,10,11,12,13]
                        self.judnum = 9
                if self.judnum<=5:
                    self.jud = [9,10,11,12,13]
                    self.judnum = 5
        for i in range(9):
            if all(self.many[i:i+5]):
                for j in range(4):
                    if sum(player[j][i:i+5]) == 5:
                        self.jud = list(range(i,i+5))
                        self.judnum = 9
                if not self.jud or self.jud[0]>=i:
                    if self.judnum<=5:
                        self.jud = list(range(i,i+5))
                        self.judnum = 5
        return self.judnum, self.jud