def group_by(f, target_list):
    grouped = {}
    for key, value in map(lambda x: (f(x), x), target_list):
        grouped.setdefault(key, []).append(value)
    return grouped



print(group_by(len, ["hi", "dog", "me", "bad", "good"]))  # {2: ['hi', 'me'], 3: ['dog', 'bad'], 4: ['good']}
print(group_by(lambda x: x % 2, [1, 2, 3, 4, 5]))        # {1: [1, 3, 5], 0: [2, 4]}
print(group_by(str.upper, ["a", "A", "b", "B", "c"]))    # {'A': ['a', 'A'], 'B': ['b', 'B'], 'C': ['c']}