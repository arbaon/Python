#!/usr/local/bin/python
import sys

#example 1
x = lambda a : a + 10
print (x(5))

#example 2 (multiple arguments)
y = lambda a,b : a * b
print (y(5,6))

#example 3 (usage)
def myfunc(n):
    return lambda a : a * n
printone = myfunc(10) #printone becomes the function with initial value
print(printone(2)) #second value added to the function

# This example shows how both values are given to the function, the printone var because "50 * n"
printone = myfunc(50)
printtwo = printone(2)
printthree = printone(3)
print(printtwo, printthree)
