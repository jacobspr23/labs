from functools import reduce

def filter_with_reduce(f, target_list):
   
    return reduce(
        lambda acc, x: acc + [x] if f(x) else acc,
        target_list,
        []
    )


print(filter_with_reduce(lambda x: x > 3, [1, 2, 3, 4, 5]))    # [4, 5]
print(filter_with_reduce(lambda x: x % 2 == 0, [1, 2, 3, 4]))  # [2, 4]
print(filter_with_reduce(lambda x: len(x) > 2, ["hi", "dog", "me"]))  # ["dog"]
print(filter_with_reduce(lambda x: x < 0, []))                # []