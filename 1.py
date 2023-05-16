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


# create an empty array
my_array = []

# define the calculation
def my_calculation(input_value):
    # perform some calculation on the input value
    result = input_value * 2
    return result

# perform the calculation and insert the result into the array
for i in range(10):
    # replace 10 with the number of times you want to perform the calculation
    input_value = i * 3 # replace 3 with the value you want to use for the calculation
    result = my_calculation(input_value)
    my_array.append(result)

# print the array to verify the results
print(my_array)


import configparser

config = configparser.ConfigParser()
config.read('configsample.ini')

section_name = 'temp'
if section_name in config:
    num_keys = len(config[section_name])
    for i in range(num_keys):
        tempinput.append(input1)
    print(input1)

