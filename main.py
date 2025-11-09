num_tapes = 0
max_steps = 0
tape_length = 0
tape_length = 0
alphabet = []
states = []
start_state = []
accept_state = []
reject_state = []
tape_alphabet = []
stored_transitions = {}

f = open("TM1.txt")
line_counter = 1
for line in f:
    temp_arr = []
    temp_str = ""
    for ch in line.strip():
        if ch == ",":
            temp_arr.append(temp_str)
            temp_str = ""
        else:
            temp_str += ch
    temp_arr.append(temp_str)

    if line_counter == 1:
        machine_name = temp_arr[0]
        num_tapes = int(temp_arr[1])
        max_steps = int(temp_arr[2])
        tape_length = int(temp_arr[3])

    elif line_counter == 2:
        alphabet = temp_arr
        print("Alphabet:", alphabet)

    elif line_counter == 3:
        states = temp_arr
        print("States:", states)

    elif line_counter == 4:
        start_state = temp_arr[0]
        print("Start state:", start_state)

    elif line_counter == 5:
        accept_state = temp_arr
        print("Accept states:", accept_state)

    elif line_counter == 6:
        tape = temp_arr
        print("Tape:", tape)


    else:
        stored_transitions[(temp_arr[0],temp_arr[1])] = (temp_arr[2], temp_arr[3], temp_arr[4])
    line_counter+=1



input_string = "helloworld:HELLOWORLD:h_"
current_state = start_state
new_str = ""
i=0
while input_string[i] != "_":
    if (current_state, input_string[i]) in stored_transitions:
        next_state, write_symbol, direction = stored_transitions[current_state, input_string[i]]
        new_str = new_str + write_symbol
        if direction == 'R':
            i+=1
        elif direction=='L':
            i-=1
        current_state = next_state
print(new_str) 