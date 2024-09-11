import math
num1 = input("Enter the first number: ")
num2 = input("Enter the second number: ")

num1 = float(num1)
num2 = float(num2)

hypotenuse = math.sqrt(num1**2 + num2**2)

print("The hypotenuse is", round(hypotenuse, 2))