#Digital Ocean Python Tutorial                  #
#Conversions & Variables & String Formatters    #
#https://www.digitalocean.com/community/tutorials/how-to-use-string-formatters-in-python-3

#Conversions
float(5)
int(29.8)
str(45.62)

print("coco got " + str(45.7) + " points.")

print(tuple(["tosunum", "nerdesin"]))

#immutable
tuple("hadi bakalim")

#mutable
list("hopidik")

#Variables
#multiple assignment

x = y = z = 0

print(x)
print(z)

a, b, c = "hobaa", 3, False

print(c)
print(a)


def new_func():
    #local variable
    new = 1

    #global variable
#    global var
    var = 2

    print(new)

#print(var)
new_func()


#String formatters
print("the quick {} fox jumps over lazy dog".format("brown"))

love = "open source"

print("sammy loves {}".format(love))


print("{} x {} equls to 4".format(2, 2))

#index of tuple
print("buradan {1} atli gecti, {0} kardas".format(1, "hele"))

#key arguments
print("tosunu nedion {} sen ole {vr}".format("oralarda", vr = "bi basina"))

print("bu fasulya {0:.2f} lira".format(75))
print("bu fasulya {0:.0f} lira".format(7.5))

#{index:character_count}
#adds space as specified amount - variable size before variable
print("hadi {0:5} gulum {1:5} yandan".format("be", "ne"))

#{index:<character_count}
#adds space as specified amount - variable size after variable
#{index:^character_count}
#adds space as specified amount - variable size and centers variable
print("hadi {:^5} gulum {1:^15} yandan".format("be", "ne"))

#{index:*^character_count}
#adds * (or specified character) as specified amount - variable size and centers variable
print("hadi {:$^5} gulum {1:!^15} yandan".format("be", "ne"))


for i in range(2, 10):
    print("{:2d} {:4d} {:5d}".format(i, i*i, i*i*i))