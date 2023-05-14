bit_positions = [193, 194, 195, 196]
hex_position = 25

for i in bit_positions:
    pos = i % 8
    # Excluding 5 (1-4)
    if pos in range(1, 5):
        print("First 4-bits")
    # (5-0) 0 which is '8'
    else:
        print("Second 4-bits")


## guna modulus (bit_pos)/8 get xx.yy
## then .yy * 8 = exact position