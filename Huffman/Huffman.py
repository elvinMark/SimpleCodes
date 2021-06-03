import sys

class nodeTree:
    def __init__(self,freq,data):
        self.freq = freq
        self.data = data
        self.right = None
        self.left = None
    def greater_than(self,nodet):
        return self.freq > nodet.freq
    def __str__(self):
        return str(self.freq)+ '.' +str(self.data)
    def print_tree(self,space=0):
        if(self.right != None):
            self.right.print_tree(space = space+10)
        print(' '*space + str(self))
        if(self.left != None):
            self.left.print_tree(space = space+10)

class nodeList:
    def __init__(self,nodet):
        self.node_tree = nodet 
        self.next_node = None
    def __str__(self):
        return str(self.node_tree)

class mylist:
    def __init__(self,head=None):
        self.node_head = head
    def insert_node(self,nodel):
        if self.node_head == None:
            self.node_head = nodel
        else:
            if self.node_head.node_tree.greater_than(nodel.node_tree):
                self.node_head.node_tree, nodel.node_tree = nodel.node_tree, self.node_head.node_tree
                nodel.next_node = self.node_head.next_node
                self.node_head.next_node = nodel
                return None
            tmp = self.node_head
            while tmp.next_node!=None:
                if nodel.node_tree.greater_than(tmp.next_node.node_tree):
                    tmp = tmp.next_node
                else:
                    break
            nodel.next_node = tmp.next_node
            tmp.next_node = nodel
    def print_list(self):
        tmp = self.node_head
        while tmp!=None:
            print(str(tmp) + ' ',end='')
            tmp = tmp.next_node
        print('')
    def pop(self):
        tmp = self.node_head
        self.node_head = self.node_head.next_node
        return tmp

class huffman:
    def __init__(self,m):
        self.m = m #Original Message
        self.ft = {} #Frequency Table
        for i in m:
            if i in self.ft.keys():
                self.ft[i] += 1
            else:
                self.ft[i] = 1
        l = mylist(None)
        for i in self.ft:
            l.insert_node(nodeList(nodeTree(self.ft[i],i)))
        tmp = None
        count = 0
        while(1):
            tmp = l.pop().node_tree
            if l.node_head == None:
                l.insert_node(nodeList(tmp))
                break
            tmp1 = l.pop().node_tree
            tmp2 = nodeTree(tmp.freq + tmp1.freq,None)
            tmp2.right = tmp
            tmp2.left = tmp1
            l.insert_node(nodeList(tmp2))
        self.bt = l.pop().node_tree #binary tree for encoding and decoding
        self.c = {}
    def visit_tree(self,t,b):
        if t == None:
            return None
        if t.data != None:
            self.c[t.data] = b
            return None
        self.visit_tree(t.right,b+'1')
        self.visit_tree(t.left,b+'0')
    def generate_code(self):
        self.visit_tree(self.bt,'')
    def encode(self):
        em = ''
        for i in self.m:
            em += self.c[i]
        return em
    def get_symbol(self,b):
        tmp = self.bt
        for i in b:
            if i == 0:
                tmp = tmp.left
            elif i == 1:
                tmp = tmp.right
        return tmp.data
    def decode(self,msg):
        dm = ''
        tmp = self.bt
        for i in msg:
            if tmp.data in self.ft.keys():
                dm = dm + tmp.data
                tmp = self.bt
            if i == '0':
                tmp = tmp.left
            elif i == '1':
                tmp = tmp.right
        return dm+tmp.data
if __name__ == "__main__":
    h = huffman(sys.argv[1])
    h.bt.print_tree()
    h.generate_code()
    print(h.c)
    m = h.encode()
    print(m)
    print(h.decode(m))
