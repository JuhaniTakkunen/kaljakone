import operator

position = 10, 30
a = tuple(map(operator.add, position, (1, -1)))
print(a)
