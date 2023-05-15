bit_positions = [238]
for i in bit_positions:
    pos = i % 8
    print(pos)
    # Excluding 5 (1-4)
    if pos in range(1, 5):
        print("First 4-bits")
    # (5-0) 0 which is '8'
    else:
        print("Second 4-bits")

fruits = []
print("1" + str(fruits))
for i in range(10):
    fruits.append("Orange")
    print(fruits)

print(fruits)
for i in range(4):
    fruits.append("Apple")
    print(fruits)