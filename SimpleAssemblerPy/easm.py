import sys

ope = ["mov","add","sub","mul","div","jmp","call","cmp","ret"]
regs = {"%rax":0,"%rbx":0,"%rcx":0,"%rdx":0,"%rsi":0,"%rip":0,"%rsp":0,"%rbp":0,"%rflags":0}
pile = []
labels={}

def mov_fun(op1,op2):
    if op1[0] == "$":
        regs[op2] = int(op1[1:])
    elif op1[0] == "%":
        regs[op2] = regs[op1]
def add_fun(op1,op2):
    if op1[0] == "$":
        regs[op2] = int(op1[1:]) + regs[op2]
    elif op1[0] == "%":
        regs[op2] = regs[op1] + regs[op2]
def sub_fun(op1,op2):
    if op1[0] == "$":
        regs[op2] = regs[op2] - int(op1[1:])
    elif op1[0] == "%":
        regs[op2] = regs[op2] - regs[op1]
def mul_fun(op1,op2):
    if op1[0] == "$":
        regs[op2] = regs[op2] * int(op1[1:])
    elif op1[0] == "%":
        regs[op2] = regs[op2] * regs[op1]
def div_fun(op1,op2):
    if op1[0] == "$":
        regs[op2] = regs[op2] //  int(op1[1:])
    elif op1[0] == "%":
        regs[op2] = regs[op2] // regs[op1]
def cmp_fun(op1,op2):
    if op1[0] == "$":
        regs["%rflags"] = 0 if regs[op2] ==  int(op1[1:]) else (regs[op2] -  int(op1[1:]))//abs(regs[op2] - int(op1[1:])) 
    elif op1[0] == "%":
        regs["%rflags"] = 0 if regs[op2] == regs[op1]  else (regs[op2] - regs[op1])//abs(regs[op2] - regs[op1])

def run_code(l):
    flag = 0
    tmp = 0
    while 1:
        curr_l = l[regs["%rip"]]
        if len(curr_l)==1 and curr_l[0] in labels.keys():
            flag +=1
        else:
            if curr_l[0] == "add":
                add_fun(curr_l[1],curr_l[2])
            elif curr_l[0] == "sub":
                sub_fun(curr_l[1],curr_l[2])
            elif curr_l[0] == "mul":
                mul_fun(curr_l[1],curr_l[2])
            elif curr_l[0] == "div":
                div_fun(curr_l[1],curr_l[2])
            elif curr_l[0] == "mov":
                mov_fun(curr_l[1],curr_l[2])
            elif curr_l[0] == "jmp":
                regs["%rip"] = labels[curr_l[1]]+1
                continue
            elif curr_l[0] == "cmp":
                cmp_fun(curr_l[1],curr_l[2])
            elif curr_l[0] == "call":
                tmp = regs["%rip"] + 1
                regs["%rip"] = labels[curr_l[1]]
                continue
            elif curr_l[0] == "ret":
                if flag > 1:
                    regs["%rip"] = tmp
                flag -= 1
                if not flag:
                    break
                else:
                    continue
            elif curr_l[0] == "jg":
                if regs["%rflags"] == 1:
                    regs["%rip"] = labels[curr_l[1]]+1
                    continue
            elif curr_l[0] == "jl":
                if regs["%rflags"] == -1:
                    regs["%rip"] = labels[curr_l[1]]+1
                    continue
            elif curr_l[0] == "je":
                if regs["%rflags"] == 0:
                    regs["%rip"] = labels[curr_l[1]]+1
                    continue
        regs["%rip"] += 1
                    
if __name__ == "__main__":
    f = open(sys.argv[1])
    c = 0
    for line in f:
        pile.append(line.split())
        if len(pile[-1]) == 1 and not (pile[-1][0] in ope):
           labels[pile[-1][0]] = c
        c += 1
    run_code(pile)
    print(regs)
