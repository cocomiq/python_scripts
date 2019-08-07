
# date and time manipulations
import datetime as dt

print(dt.date())

# formats date as specified                  #
print(dt.date().strftime("%Y-%m-%d %H:%M"))

# reads date from string
# print(dt.strptime('20190131', '%Y%m%d'))

# ternary expressions                        #
x = 10

print("negative" if x < 0 else "positive")

# modify mutable object in tuple             #
tup = tuple("aboo", [1, 2], True)

# add element 3 in list which is 2nd element of tuple
tup[1].append(3)

tup = (4, 5, (6, 7))

# assigning variables from tuples
a, b, (c, d) = tup
print(d)

# concatenation by addition is expensive operation since a new list must be created and the objects copied over
print([1, 2, 3, 4] + ["hadii", 5, 6])

x = [1, 2, 3, 4]
x.extend(["hadii", 5, 6])

# enumerate
# automatic incremenals
lister = ["a", "b", "c", "d"]

for i, a in enumerate(lister):
        print(i, a)

# zip
# pairs items from 2 lists to create a list of tuples

lister2 = ["one", "two", "three", "four"]

print(zip(lister, lister2))

lister3 = ["one", "two", "three"]

print(zip(lister, lister3))


for i, (a, b) in enumerate(zip(lister, lister2)):
    print("{0}: {1}, {2}".format(i, a, b))

# dictionaries
# the keys generally have to be immutable objects like scalar types (int, float, string) or tuples (all the objects in the tuple need to be immutable, too)
# all keys should be hashable

d1 = {"a" : "some value", "b" : [1, 2, 3, 4]}
d1["dummy"] = "another value"

# pop
# you can delete values either using the del keyword or the pop method (which simultaneously returns the value and deletes the key)
ret = d1.pop("dummy")

d1.keys()
d1.values()

# update
# you can merge one dict into another using the update method
d1.update({"c" : "foo", 5 : 123})

# get, pop return default value if the key is empty
# get by default will return None if the key is not present, while pop will raise an exception
val = d1.get("b", "oops")

# setdefault
by_letter = {}
words = ['apple', 'bat', 'bar', 'atom', 'book']

for word in words:
        letter = word[0]
        by_letter.setdefault(letter, []).append(word)

# defaultdict
from collections import defaultdict

by_letter = defaultdict(list)

for word in words:
        by_letter[word[0]].append(word)