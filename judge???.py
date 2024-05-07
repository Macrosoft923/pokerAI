import random
from PlayingCard import PlayingCard
import timeout_decorator
import collections



class Judge:
    def __init__(self):
            self.pyi = PlayingCard()
            self.comcard =[]
            self.plycard = []
            self.many = []#要素数
            self.judge = []#約判定リスト
            self.revply = []

    def Jud(self,num):
        self.comcard = self.pyi.getCard(5).copy()
        for i in range(num):
          #self.plycard.append([])
          self.plycard.append(self.pyi.getCard(2))
          self.judge.append([])
          self.plycard[i]+=self.comcard
          self.revply.append(sorted(self.plycard[i], reverse=True))#降順に並べた
          self.many.append(collections.Counter(self.revply[i]))
          
          for k in self.many[i]:
            if self.many[i][k] == 3:
              self.judge[i].append(104)
              self.judge[i].append(k)
            elif self.many[i][k] == 2:
              self.judge[i].append(102)
              self.judge[i].append(k)

            elif self.many[i][k] == 4:
              pass
            if self.judge[i].count(102) >=2:
              self.judge[i][0] = 103
            if 102 in self.judge[i]:
              if 104 in self.judge[i]:
                self.judge[i][0] = 106
          if not self.judge[i]:
            self.judge[i] = self.revply[i]
          #for l in self.many[i]:
            #if self.many[i][l] == 1:
              #self.judge[i].append(l)
        return self.judge

jud = Judge()

print(jud.Jud(3))