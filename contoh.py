fruits = {"apple", "banana", "cherry"}

fruits = list(fruits)
fruits.sort()
#fruits.append(fruits)

for i in fruits:
    print(''.join((i)), end='')
    