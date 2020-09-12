# ==========================================================================
# semih acikgoz
# 20200609
#
# Python for Data Analysis
# ==========================================================================

# ==========================================================================
# Jupyter tricks
# ==========================================================================
# Generated additional matplotlib instance
# %matplotlob inline

# ==========================================================================
# Chapter 1
# ==========================================================================
# data types
a = 5
type(a)

# check data type
isinstance(a, int)

# for multiple data type check use tuple
b = 10.5
isinstance(b, (int, float))

# check if two references refer to the same object
a is b

# integer division
3 / 2   # 1.5
3 // 2  # 1, returns only integer

# convert to string
str(a)
int(str(a))
float(a)

# formatting text
print("{0:d} dummy {1:s}".format(1, "text"))

# null check
a is not None

# string to datetime functions
from datetime import datetime

dt = datetime.strptime("20200610", "%Y%m%d")

# replace date
dt.replace(day = 15)

# range between 0 and 9
range(10)

# backwards range between 5 and 1
range(5, 0, -1)

# ternary expression = single line if expression
"true value" if a > 0 else "negative"

# mutable object in tuple
tup = ("asd", 100, [1, 2, 3], 500)
tup[2].append(3)

# unpacking sequences
seq = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]

for a, b, c in seq:
    print("a = {0}, b = {1}, c = {2}".format(a, b, c))

# enumerate function
# automatic loop counter
for i, value in enumerate(tup):
    print("{0}th element is: {1}".format(i, value))

# zip creates a list of tuples
# zip can take an arbitrary number of sequences, and the number of elements it produces is determined by the shortest sequence:
seq1 = ["topu", "tutun", "lan"]
seq2 = ["lan", "kime", "diyorum"]
seq3 = ["oldu mu", "simdi"]

zip(seq1, seq2)
zip(seq1, seq2, seq3)

# simultaneously iterating over multiple sequences
for i, (a, b) in enumerate(zip(seq1, seq2)):
    print("{0}: {1}, {2}".format(i, a, b))

# numpy boolean indexing
import numpy as np

names = np.array(['Bob', 'Joe', 'Will', 'Bob', 'Will', 'Joe', 'Joe'])
data = np.random.randn(7, 4)

# python keywords and and or do not work with boolean arrays, use & (and) and | (or) instead
mask = (names == 'Bob') | (names == 'Will')
print(mask)