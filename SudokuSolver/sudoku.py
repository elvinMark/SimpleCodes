import sys

def read_file(filename):
	f = open(filename,"r")
	t = []
	for line in f:
		line = line.replace("\n","")
		line = line.replace(" ","-")
		line = line.replace("0"," ")
		t.append(line.split("-"))
	return t

def print_table(table):
	counter = 0
	for elem in t:
		if counter%3 == 0:
			print("-------------------")
		counter+=1
		print("|"+"|".join(elem)+"|")
	print("-------------------")

def check_possible_values(table,x,y):
	if table[x][y] != " ":
		return []
	poss_values = ['1','2','3','4','5','6','7','8','9']
	sx = x//3
	sy = y//3
	for i in range(9):
		if table[x][i] in poss_values:
			poss_values.remove(table[x][i])
		if table[i][y] in poss_values:
			poss_values.remove(table[i][y])
	for i in range(3):
		for j in range(3):
			if table[3*sx+i][3*sy+j] in poss_values:
				poss_values.remove(table[3*sx+i][3*sy+j])
	return poss_values 

def get_possible_values_table(table):
	tpv = []
	for i in range(9):
		tmp = []
		for j in range(9):
			tmp.append(check_possible_values(t,i,j))
		tpv.append(tmp)
	return tpv

def isSolved(table):
	for i in table:
		for j in i:
			if j==" ":
				return False
	return True

def get_solution(tpv,x,y):
	if len(tpv[x][y]) == 0 or len(tpv[x][y]) != 1:
		return None
	return None

def solve_sudoku(table):
	for i in range(81):
		if isSolved(table):
			break
		tpv = get_possible_values_table(table)
		for i in range(9):
			for j in range(9):
				if len(tpv[i][j]) == 1:
					table[i][j] = tpv[i][j][0]
	print("steps:",i)
	return table

t = read_file(sys.argv[1])
print_table(t)
st = solve_sudoku(t)
print_table(st)
