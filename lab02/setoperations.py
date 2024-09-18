
data = [1, 2, 3, 4, 5, 5, 6, 7, 8, 9, 10]

def make_set(data):
    newSet = []
    for num in data:
        if num not in newSet:
            newSet.append(num)
    return newSet

print(data)
newSet =make_set(data)
print(newSet)

def is_set(data):
    newSet = []
    for num in data:
        if num in newSet:
            return False
        newSet.append(num)
    return True

print(is_set(data))
print(is_set(newSet))

def union(set1, set2):
    if is_set(set1) and is_set(set2):
        return set1 + set2
    else:
        return []

set1 = [1, 2, 3]
set2 = [3, 4, 5]
set3 = union(set1, set2)
print(set3)

def intersection(set1, set2):
    if is_set(set1) and is_set(set2):
        return [num for num in set1 if num in set2]
    else:
        return []

set4 = [1, 2, 3]
set5 = [3, 4, 5]
set6 = intersection(set4, set5)
print(set6)
    
