import sys

h = {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'a':10,'b':11,'c':12,'d':13,'e':14,'f':15}

def to_num(h1):
    o = 0
    for i in h1:
        o = 16*o + h[i]
    return o
def to_ascii(h):
    tmp = to_num(h)
    if tmp>31 and tmp<127:
        return chr(to_num(h))
    return '.'
def convert_to_ascii(arr):
    return [to_ascii(i) for i in arr]

def print_table(dir):
    f = open(dir,'rb')
    tmp = ''
    for chunk in f:
        tmp = tmp + chunk.hex()
    a = [tmp[i:i+2] for i in range(0,len(tmp),2)]
    b = convert_to_ascii(a)
    for i in range(len(a)//16):
        print(' '.join(a[16*i:16*i+16]) + '\t|\t' + ' '.join(b[16*i:16*i+16]))
    i = 16*(len(a)//16)
    print(' '.join(a[i:]) + '   '*(16-len(a[i:])) + '\t|\t' + ' '.join(b[i:]))

if __name__ == "__main__":
    print_table(sys.argv[1])
