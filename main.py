from random import*
from random import randint

class game:
    def __init__(self,num_sticks):
        self.board = ["|" for i in range(num_sticks)]
        pass

class player:
    def __init__():
        pass

class bot:
    def __init__(self,actions,game):
        self.actions = actions
        max_actions  =  len(game.board) // max(actions)
        self.points = [[1 for i in range(len(actions))] for j in range(max_actions)]
    def play(self,rem_sticks):
        if rem_sticks != 1:
            pass


    



newgame = game(21)
claude = bot([1,2,3],newgame)
def cleanList(ls):
    return "".join(ls)


length = len(newgame.board)

print(cleanList(newgame.board))