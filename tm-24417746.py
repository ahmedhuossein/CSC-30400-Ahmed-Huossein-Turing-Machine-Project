import sys

num_tapes = 0
max_steps = 0
tape_length = 0
alphabet = []
states = []
start_state = ""
accept_state = ""
reject_state = ""
tape_alphabet = []
stored_transitions = {}

Description = sys.argv[1]
Tape_test = sys.argv[2]
f = open(Description, "r")
g = open(Tape_test, "r")
line_counter = 1
current_rule_number = 1

for line in f:
    temp_arr = line.strip().split(",")

    if line_counter == 1:
        machine_name = temp_arr[0]
        num_tapes = int(temp_arr[1])
        tape_length = int(temp_arr[2])
        max_steps = int(temp_arr[3])

    elif line_counter == 2:
        alphabet = temp_arr

    elif line_counter == 3:
        states = temp_arr

    elif line_counter == 4:
        start_state = temp_arr[0]

    elif line_counter == 5:
        accept_state = temp_arr[0]
        reject_state = temp_arr[1]

    elif 6 <= line_counter <= 5 + num_tapes:
        tape_alphabet.append(temp_arr)
    else:
        # Example transition:
        # q0,0,_,q1,x,_,R,S      for 2 tapes
        # q0,0,:,:,q2,0,:,:,S,R,R for 3 tapes

        state = temp_arr[0]
        read_syms = temp_arr[1 : 1 + num_tapes]
        next_state = temp_arr[1 + num_tapes]
        write_to_tape = temp_arr[2 + num_tapes : 2 + 2*num_tapes]
        direction = temp_arr[2 + 2*num_tapes : 2 + 3*num_tapes]        #works for any k

        stored_transitions[current_rule_number] = {
            "state": state,
            "read": read_syms,
            "next": next_state,
            "write": write_to_tape,
            "move": direction
        }

        current_rule_number += 1

    line_counter += 1

print(f"\n====================================================")
print(f" MACHINE: {machine_name}")
print(f" TAPES: {num_tapes}, MAX STEPS: {max_steps}")
print(f"====================================================\n")

while True:
    tapes = []

    for t in range(num_tapes):
        line = g.readline().strip()
        if not line:
            tapes = []
            break
        if t == 0:
            print("Input:", line)
        while len(line) < tape_length:
            line+="_"
        tapes.append(line)

    if not tapes:
        break
    for i in range(num_tapes):
        print(f"Tape {i+1}: {tapes[i].rstrip('_')}_")
    current_state = start_state
    heads = [0] * num_tapes
    step = 1

    while True:

        current_symbols = []

        for i in range(num_tapes):
            head = heads[i]
            symbol = tapes[i][head]
            current_symbols.append(symbol)

            # illegal symbol check
            if symbol not in tape_alphabet[i] and symbol != "_":
                print("Error: Illegal symbol:", symbol)
 
 
        for rule_number, rule in stored_transitions.items():

            if rule["state"] != current_state:
                continue

            for i in range(num_tapes):
                if rule["read"][i] != "*" and rule["read"][i] != current_symbols[i]: #handle wildcard
                    break 
            else:
                next_state = rule["next"]
                write_to_tape = rule["write"]
                direction = rule["move"]

                print(
                step, ",",
                rule_number, ",",
                ",".join(str(x) for x in heads), ",", #.join (needed for arrays) only works for string must convert each element to int
                current_state, ",",
                ",".join(current_symbols), ",",
                next_state, ",",
                ",".join(write_to_tape), ",",
                ",".join(direction),
                sep=""
            )

                break
        else:
            print("Error: No transition found")
            break


        for i in range(num_tapes):
            if write_to_tape[i] != "*":
                tapes[i] = tapes[i][:heads[i]] + write_to_tape[i] + tapes[i][heads[i]+1:]
            # else: DO NOTHING


        for i in range(num_tapes):
            if direction[i] == "R":
                heads[i] += 1
            elif direction[i] == "L":
                heads[i] -= 1
            # S -> stay still (do nothing)


        current_state = next_state
        step += 1

        if step >= max_steps:
            print("Error: max steps exceeded")
            break


    if current_state == accept_state:
        print("Accepted")
    elif current_state == reject_state:
        print("Rejected")
    else:
        print("Error")


    for i in range(num_tapes):
        print(f"Tape {i+1}: {tapes[i].rstrip('_')}_")
    print("--------------------------------------------------") 
    
