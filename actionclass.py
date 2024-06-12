class action:
    def __init__(self,bet,stack,fold):
        self.Bet = False
        self.Raise = False
        self.newmaxbet = 0
        self.oldmaxbet = 0
        self.bets = bet
        self.stack = stack
        self.folded = fold

    def check(self):
        if not self.Bet:
            return 
        
    def bet(self,player,size):
        if not self.Bet:
            self.Bet = True
            self.newmaxbet = size
            self.bets[player] = size
            self.stack
    
    def call(self,player):
        self.bets[player] += self.newmaxbet - self.bets[player]
        self.chips[player] -= bet
        closed_count += 1


    def _raise(self,bet,stack,size):
        if self.Bet:
            if 2*self.newmaxbet - self.oldmaxbet <= size < bet+stack :
                return size
            elif size == bet + stack:
                self.allin()
            
    def fold(self):
        return False
    
    def allin(self):
        return True