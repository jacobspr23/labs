def zipmap(key_list, value_list, override=False):
    # Check for duplicate keys if override is False
    if not override and len(set(key_list)) != len(key_list):
        return None  # Abort if duplicates exist
    
    # Fill missing values with None
    complete_pairs = map(lambda k, v: (k, v), key_list, value_list + [None] * (len(key_list) - len(value_list)))
    return dict(complete_pairs)



print(zipmap(['a', 'b', 'c', 'd'], [1, 2, 3, 4]))       # {'a': 1, 'b': 2, 'c': 3, 'd': 4}
print(zipmap([1, 2, 3], [4, 5, 6, 7, 8]))              # {1: 4, 2: 5, 3: 6}
print(zipmap([1, 3, 5, 7], [2, 4, 6]))                 # {1: 2, 3: 4, 5: 6, 7: None}
print(zipmap([1, 2, 3, 2], [4, 5, 6, 7], override=False))  # None
print(zipmap([1, 2, 3, 2], [4, 5, 6, 7], override=True))   # {1: 4, 2: 7, 3: 6}
