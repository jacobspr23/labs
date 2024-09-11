import math
radius = input("Enter the radius of the circle: ")
radius = float(radius)

area = math.pi * radius**2
circumference = 2 * math.pi * radius

print("The circle with radius: ", round(radius, 2), "Has an area of: ", round(area, 2), "And a perimeter of: ", round(circumference, 2))
