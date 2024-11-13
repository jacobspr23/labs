def product_of_digits(n):
    n = abs(n)
    if n < 10:
        return n
    else:
        return (n % 10) * product_of_digits(n // 10)
    
def array_to_string(a, index=0):
    if len(a) == 0:
        return ""
    if index == len(a) - 1:
        return str(a[index])
    else:
        return str(a[index]) + ", " + array_to_string(a, index + 1)
    
def log(base, value):
    if base <= 1 or value <= 0:
        raise ValueError("base must be > 1 and value must be > 0.")
    if value < base:
        return 0
    else:
        return 1 + log(base, value // base)
    
def main():
    print("product_of_digits(5) =", product_of_digits(5))
    print("product_of_digits(-12) =", product_of_digits(-12))  
    print("product_of_digits(0) =", product_of_digits(0))

    print("array_to_string([1, 2, 3, 4, 5]) =", array_to_string([1, 2, 3, 4, 5]))  
    print("array_to_string([7]) =", array_to_string([7]))                          
    print("array_to_string([]) =", array_to_string([]))

    print("log(2, 64) =", log(2, 64))           
    print("log(10, 4567) =", log(10, 4567))    
    print("log(2, 1) =", log(2, 1)) 

if __name__ == "__main__":
    main()