# a = int(input())
# b = int(input())
#
# res = a * b if a * b > 1000 else a + b
# print(res)
from functools import reduce

#list(lambda x: x[0] * x[1] if x[0] * x[1] > 1000 else x[0] + x[1], [int(input()), int(input())])


# print('any([True, False])', any([True, False]))
# print('any([False, False])', any([False, False]))
# print('any([True, True])', any([True, True]))
# print('any([10, 100, 1000])', any([10, 100, 1000]))
# print('any([10, 100, 0, 1000])', any([10, 100, 0, 1000]))
# print("any(['Python', 'C#'])", any(['Python', 'C#']))
# print("any(['school', '', 'language'])", any(['school', '', 'language']))
# print('any([(1, 2, 3), []])', any([(1, 2, 3), []]))
# print('any([])', any([]))
# print('any([[], []])', any([[], []]))
# print("any({0: 'Monday', 1: 'Tuesday', 2: 'Wednesday'})", any({0: 'Monday', 1: 'Tuesday', 2: 'Wednesday'}))
# print("any({0: 'Monday'})", any({0: 'Monday'}))
# print("any({'name': 'Timur', 'age': 28})", any({'name': 'Timur', 'age': 28}))
# print("any({'': 'None', 'age': 28})", any({'': 'None', 'age': 28}))


print('any([True, False])', any([True, False]))
print('any([False, False])', any([False, False]))
print('any([True, True])', any([True, True]))
print('any([10, 100, 1000])', any([10, 100, 1000]))
print('any([0, 0, 0, 0])', any([0, 0, 0, 0]))
print("any(['Python', 'C#'])", any(['Python', 'C#']))
print("any(['', '', 'language'])", any(['', '', 'language']))
print('any([(1, 2, 3), []])', any([(1, 2, 3), []]))
print('any([])', any([]))
print('any([[], []])', any([[], []]))
print("any({0: 'Monday', 1: 'Tuesday', 2: 'Wednesday'})", any({0: 'Monday', 1: 'Tuesday', 2: 'Wednesday'}))
print("any({0: 'Monday'})", any({0: 'Monday'}))
print("any({'name': 'Timur', 'age': 28})", any({'name': 'Timur', 'age': 28}))
print("any({'': 'None', 'age': 28})", any({'': 'None', 'age': 28}))
