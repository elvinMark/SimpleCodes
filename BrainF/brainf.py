import sys

arr = [0]*1000

def run_code(s):
    idx = []
    i = 0
    ptr = 0
    while i < len(s):
        if s[i]=='>':
            ptr += 1
        elif s[i]=='<':
            ptr -= 1
        elif s[i] == '+':
            arr[ptr] += 1
        elif s[i] == '-':
            arr[ptr] -= 1
        elif s[i] == '.':
            print(chr(arr[ptr]),end='')
        elif s[i] == ',':
            arr[ptr] = ord(input()[0])
        elif s[i] == '[':
            idx.append(i)
        elif s[i] == ']':
            if arr[ptr] == 0:
                idx.pop()
                pass
            else:
                i = idx[-1]
        else:
            pass
        i += 1
if __name__ == "__main__":
    f = open(sys.argv[1])
    s = ""
    for line in f:
         s = s + line
    run_code(s)
