import math

input = input("Enter a distance or a weight amount followed by a space and unit of measurement: ")

input = input.split(" ")
num = float(input[0])
unit = input[1]

if unit == "in":
    print(num, "in =", round(num * 2.54, 2), "cm")
elif unit == "cm":
    print(num, "cm =", round(num / 2.54, 2), "in")
elif unit == "yd":
    print(num, "yd =", round(num * 0.9144, 2), "m")
elif unit == "m":
    print(num, "m =", round(num / 0.9144, 2), "yd")
elif unit == "oz":
    print(num, "oz =", round(num * 28.349523125, 2), "g")
elif unit == "g":
    print(num, "g =", round(num / 28.349523125, 2), "oz")
elif unit == "lb":
    print(num, "lb =", round(num * 0.45359237, 2), "kg")
elif unit == "kg":
    print(num, "kg =", round(num / 0.45359237, 2), "lb")
else:
    print("Invalid unit")