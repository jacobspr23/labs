import functools
import time

def cache_decorator(func):
    cache = {}

    @functools.wraps(func)
    def wrapper(n):
        if n in cache:
            return cache[n]
        result = func(n)
        cache[n] = result
        return result
    
    return wrapper

def recur_fibo(n):
    if n <= 1:
        return n
    return recur_fibo(n - 1) + recur_fibo(n - 2)

@cache_decorator
def optimized_fibo(n):
    if n <= 1:
        return n
    else:
        return optimized_fibo(n - 1) + optimized_fibo(n - 2)
    
def compare_execution_time(n):
    """
    Compare the execution time of the standard and optimized Fibonacci functions.
    """
    # Measure time for the standard recursive function
    start_time = time.time()
    try:
        print(f"Standard Fibonacci ({n}): {recur_fibo(n)}")
    except RecursionError:
        print("Standard Fibonacci failed due to recursion depth limit.")
    end_time = time.time()
    standard_time = end_time - start_time
    print(f"Execution time for standard Fibonacci: {standard_time:.4f} seconds")

    # Measure time for the optimized function
    start_time = time.time()
    print(f"Optimized Fibonacci ({n}): {optimized_fibo(n)}")
    end_time = time.time()
    optimized_time = end_time - start_time
    print(f"Execution time for optimized Fibonacci: {optimized_time:.4f} seconds")

    print(f"Optimized function is {standard_time / optimized_time if optimized_time > 0 else 'inf'} times faster.")

# Example usage:
if __name__ == "__main__":
    compare_execution_time(35)