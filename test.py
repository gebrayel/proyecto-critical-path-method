list1 = [1, 2, 3, 4,"2", 5]
list2 = [0, 2, 4, 6]

set1 = set(list1)
set2 = set(list2)

set3 = (set1 - set2) | (set2 - set1)
list3 = list(set3)

# print(list3)

print(list1.index("2"))