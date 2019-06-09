
#date and time manipulations
import datetime as dt

print(dt.date())

#formats date as specified                  #
print(dt.date().strftime("%Y-%m-%d %H:%M"))

#reads date from string
#print(dt.strptime('20190131', '%Y%m%d'))

#ternary expressions                        #
x = 10

print("negative" if x < 0 else "positive")

#modify mutable object in tuple             #
tup = tuple("aboo", [1, 2], True)

#add element 3 in list which is 2nd element of tuple
tup[1].append(3)

tup = (4, 5, (6, 7))

#assigning variables from tuples
a, b, (c, d) = tup
print(d)

#concatenation by addition is expensive operation since a new list must be created and the objects copied over
print([1, 2, 3, 4] + ["hadii", 5, 6])

x = [1, 2, 3, 4]
x.extend(["hadii", 5, 6])

#enumerate
#automatic incremenals
lister = ["a", "b", "c", "d"]

for i, a in enumerate(lister):
        print(i, a)

#zip
#pairs items from 2 lists

lister2 = ["one", "two", "three", "four"]

print(zip(lister, lister2))

lister3 = ["one", "two", "three"]

print(zip(lister, lister3))


for i, (a, b) in enumerate(zip(lister, lister2)):
    print("{0}: {1}, {2}".format(i, a, b))

