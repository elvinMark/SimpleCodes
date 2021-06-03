import random
#To indicate the rotations we are going to use a 3 element array like this:
# w = [1,0,0] -> this means that we are going to rotate the first level counter-clockwise and around x-axis.
# w = [0,-2,0] -> this means that we are going to rotate the second level of rubik's cube clockwise and around the y-axis
MOVES = []
for i in range(3):
    for j in range(2):
        MOVES.append([0]*i + [j+1] + [0]*(2-i))
        MOVES.append([0]*i + [-j-1] + [0]*(2-i))

def myabs(x):
    return x if x>0 else -x

def insert_element(arr,elem):
    if len(arr) == 0:
        return [elem]
    if arr[0].cost() < elem.cost():
        return [elem] + arr
    for i in range(len(arr)-1):
        if arr[i].cost() > elem.cost() and elem.cost()>arr[i+1].cost():
            return arr[:i+1]+[elem] + arr[i+1:]
    return arr + [elem]
def check_elem(arr,elem):
    for tmp in arr:
        if elem.compare(tmp):
            return True
    return False
class rubik:
    def __init__(self,cube=None):
        if cube!=None:
            self.r = cube
        else:
            self.r = [[[1,2],[3,4]],[[5,6],[7,8]]]
        self.moved = [0,0,0]
        self.generation = 0
    def move(self,v):
        new_cube = self.copy()
        if v[0]!=0:
            tmp = new_cube.r[myabs(v[0])-1]
            if v[0]<0:
                tmp[0][0],tmp[0][1],tmp[1][0],tmp[1][1] = tmp[1][0],tmp[0][0],tmp[1][1],tmp[0][1]
            else:
                tmp[0][0],tmp[0][1],tmp[1][0],tmp[1][1] = tmp[0][1],tmp[1][1],tmp[0][0],tmp[1][0]
        elif v[1]!=0:
            tmp0 = new_cube.r[0]
            tmp1 = new_cube.r[1]
            i = myabs(v[1])-1
            if v[1]>0:
                tmp0[0][i],tmp0[1][i],tmp1[0][i],tmp1[1][i] = tmp1[0][i],tmp0[0][i],tmp1[1][i],tmp0[1][i]
            else:
                tmp0[0][i],tmp0[1][i],tmp1[0][i],tmp1[1][i] = tmp0[1][i],tmp1[1][i],tmp0[0][i],tmp1[0][i]
        elif v[2]!= 0:
            i = myabs(v[2])-1
            tmp = [new_cube.r[1][i],new_cube.r[0][i]]
            if v[2]<0:
                tmp[0][0],tmp[0][1],tmp[1][0],tmp[1][1] = tmp[1][0],tmp[0][0],tmp[1][1],tmp[0][1]
            else:
                tmp[0][0],tmp[0][1],tmp[1][0],tmp[1][1] = tmp[0][1],tmp[1][1],tmp[0][0],tmp[1][0]
        new_cube.moved = v
        new_cube.generation = self.generation + 1
        return new_cube
    def __str__(self):
        s = "Layer 1:\n"+ str(self.r[0]) + "\nLayer 2:\n"+ str(self.r[1]) + '\n\n'
        return s
    def compare(self,r1):
        for i,j in zip(self.r,r1.r):
            for k,l in zip(i,j):
                if k!=l:
                    return False
        return True
    def copy(self):
        tmp = [[i.copy() for i in j] for j in self.r]
        return rubik(cube=tmp)
    def abs_diff(self):
        self.diff = [[[0,0],[0,0]],[[0,0],[0,0]]]
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    self.diff[i][j][k] = abs(self.r[i][j][k] - self.r[(i+1)%2][j][k]) + abs(self.r[i][j][k] - self.r[i][(j+1)%2][k]) + abs(self.r[i][j][k] - self.r[i][j][(k+1)%2]) 
    def grad(self):
        self.mgrad = [[[0,0],[0,0]],[[0,0],[0,0]]]
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    self.mgrad[i][j][k] = abs(self.diff[i][j][k] - self.diff[(i+1)%2][j][k]) + abs(self.diff[i][j][k] - self.diff[i][(j+1)%2][k]) + abs(self.diff[i][j][k] - self.diff[i][j][(k+1)%2]) 
    def is_solve(self):
        self.abs_diff()
        self.grad()
        for i in self.mgrad:
            for j in i:
                for k in j:
                    if k!=0:
                        return False
        return True
    def manhattan_distance(self):
        x1 = 0
        s = 0
        for i in self.r:
            y1 = 0
            for j in i:
                z1 = 0
                for k in j:
                    x2 = (k-1)//4
                    tmp = (k-1)%4
                    y2 = tmp//2
                    z2 = tmp%2
                    s += abs(x2-x1) + abs(y2-y1) + abs(z2-z1)
                    z1+=1
                y1 += 1
            x1 += 1
        return s
    def cost(self):
        '''
        s = 0
        self.abs_diff()
        self.grad()
        for i in self.mgrad:
            for j in i:
                for k in j:
                    s += k
        '''
        s = self.manhattan_distance()
        return s
        #return random.random()
    def solve(self,N=20):
        arr = []
        old = []
        solution=[0]*13
        arr.append(self)
        for i in range(N):
            if len(arr)==0:
                print('Failed: No Solution')
                break
            tmp = arr.pop()
            solution[tmp.generation] = tmp
            old.append(tmp)
            #print(tmp)
            if tmp.is_solve():
                print('Solved')
                return solution
            if tmp.generation > 11:
                continue
            for j in MOVES:
                tmp1 = tmp.move(j)
                if not check_elem(arr,tmp1) and not check_elem(old,tmp1):
                    arr = insert_element(arr,tmp1)
        print('No Solution')
        return None
if __name__=="__main__":
    r = rubik()
    for i in range(10):
        r = r.move(MOVES[int(12*random.random())])
    r.generation = 0
    s = r.solve(N=2000)
    if s != None:
        print(r)
        for i in s:
            try:
                print('Step '+str(i.generation))
                print(i)
            except:
                print('finish')
                break
