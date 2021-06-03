import random
import numpy as np 

MOVES = ['UP','RIGHT','LEFT','DOWN']

def copy_array(arr):
    out = [[i for i in j] for j in arr]
    return out

def insert_element(arr,new_element,solved):
    if len(arr)==0:
        return [new_element]
    if new_element.cost(solved)>=arr[0].cost(solved):
        return [new_element] + arr
    for i in range(len(arr)-1):
        if arr[i].cost(solved)>=new_element.cost(solved) and arr[i+1].cost(solved)<=new_element.cost(solved):
            return arr[:i+1] + [new_element] + arr[i+1:]
    return arr + [new_element]
class puzzle: 
    def __init__(self,board=None,pos=None):
        if board == None and pos == None:
            self.board = [['1','2','3'],['4','5','6'],['7','8',' ']]
            self.x = 2
            self.y = 2
        else:
            self.board = board
            self.x, self.y = pos
    def set_board(self,b,pos):
        self.board = b
        self.x, self.y  = pos
    def move(self,opt):
        newp = puzzle(copy_array(self.board),(self.x,self.y))
        if opt == 'UP':
            if newp.x > 0:
                newp.board[newp.x][newp.y], newp.board[newp.x-1][newp.y] =newp.board[newp.x-1][newp.y], newp.board[newp.x][newp.y]
                newp.x = newp.x - 1
                return newp
            else:
                return None
        if opt == 'DOWN':
            if newp.x < 2:
                newp.board[newp.x][newp.y], newp.board[newp.x+1][newp.y] =newp.board[newp.x+1][newp.y], newp.board[newp.x][newp.y]
                newp.x = newp.x + 1
                return newp
            else:
                return None
        if opt == 'RIGHT':
            if newp.y < 2:
                newp.board[newp.x][newp.y], newp.board[newp.x][newp.y+1] =newp.board[newp.x][newp.y+1], newp.board[newp.x][newp.y]
                newp.y = newp.y + 1
                return newp
            else:
                return None
        if opt == 'LEFT':
            if newp.y > 0:
                newp.board[newp.x][newp.y], newp.board[newp.x][newp.y-1] =newp.board[newp.x][newp.y-1], newp.board[newp.x][newp.y]
                newp.y = newp.y - 1
                return newp
            else:
                return None
    def random(self):
        count = 0
        for i in self.board:
            random.shuffle(i)
            if ' ' in i:
                self.x, self.y = count,i.index(' ')
            count += 1
    def __str__(self):
        s = ''
        for i in self.board:
            s = s + ' '.join(i)+'\n'
        return s
    def is_equal(self,p):
        for i,j in zip(self.board,p.board):
            if not i==j:
                return False
        return True
    def compare(self,p):
        s = 0
        for i in range(len(self.board)):
            for j in range(len(p.board)):
                s += not (self.board[i][j] == p.board[i][j])
        return s
    def find_pos(self,num):
        count = 0
        for i in self.board:
            if num in i:
                return [count,i.index(num)]
            count += 1
    def manhattan_distance(self,g):
        x = 0
        y = 0
        s = 0
        for i in self.board:
            y = 0
            for j in i:
                if j != ' ':
                    tmp = g.find_pos(j)
                    s = s + abs(tmp[0] - x) + abs(tmp[1] - y)
                y += 1
            x += 1
        return s
    def cost(self,solved):
        #return self.compare(solved)
        return self.manhattan_distance(solved)
    def generate_nodes(self):
        self.nodes = []
        for i in MOVES:
            tmp = self.move(i)
            if tmp!=None:
                self.nodes.append(tmp)
    def solve(self,N=20,depth=10,solved=None):
        if solved == None:
            solved = puzzle()
        arr = []
        old = []
        arr.append(self)
        for i in range(N):
            try:
                tmp = arr.pop()
            except:
                print("No solution")
                break
            #print(tmp)
            old.append(tmp)
            if tmp.is_equal(solved):
                print("Number of steps: "+str(i))
                return tmp
            tmp.generate_nodes()
            for i in tmp.nodes:
                flag = 1
                for j in arr:
                    if i.is_equal(j):
                        flag = 0
                        break
                for j in old:
                    if i.is_equal(j):
                        flag = 0
                        break
                if flag:    
                    arr = insert_element(arr,i,solved)
        print("No Solution")
        return tmp
        
if __name__ == "__main__":
    p = puzzle(board=[['5','1','2'],['6','8','3'],['7','4',' ']],pos=(2,2))
    #p = puzzle()
    #p.random()
    #p = p.move('UP')
    #p = p.move('LEFT')
    #p = p.move('DOWN')
    g = puzzle()
    print(p)
    print(g)
    z = p.solve(N=500,solved=g)
    print(z)
