bit_positions = [197, 198, 199, 200]
hex_position = 25

end_pos = (hex_position * 8) 
start_pos = end_pos - 7

first_four_bits = start_pos - 1
second_four_bits = start_pos + 3
for i in range(4):
    first_four_bits += 1
    #print(first_four_bits)
    second_four_bits += 1
    #print(second_four_bits)
    # Loop over each bit position in the list and check if it falls within the range of bits we're interested in
    for j in range(len(bit_positions)):
        if bit_positions[j] >= start_pos and bit_positions[j] <= end_pos:
            print("1")  # The bit falls within the range of bits we're interested in
        else:
            print("2")


## guna modulus (bit_pos)/8 get xx.yy
## then .yy * 8 = exact position