import sys
import json

tape = []
ptr = 0

if __name__ == '__main__':
    aux = open(sys.argv[1])
    data = json.load(aux)
    in_tape = sys.argv[2]

    tape = list(in_tape)

    curr_state = data['q_states'][0]
    ptr = 0

    while curr_state != data['q_states'][-1]:
        print("Current State :"+curr_state)
        print('\t'.join(tape))
        print('\t'*ptr + '^')
        
        mv = data['trans_states'][curr_state][tape[ptr]]
        curr_state = mv[0]
        tape[ptr] = mv[1]
        if mv[2] == "R":
            ptr += 1
        elif mv[2] == "L":
            ptr -= 1
        if ptr < 0:
            tape = [data['sym_dict'][0]] + tape
            ptr = 0;
        elif ptr == len(tape):
            tape = tape + [data['sym_dict'][0]] 

        print("Next State : "+ curr_state)
        print('# '*len(tape))
        
    print(tape)
