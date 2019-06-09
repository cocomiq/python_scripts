#Digital Ocean Python Tutorial  #
#Strings                        #
#https://www.digitalocean.com/community/tutorials/an-introduction-to-working-with-strings-in-python-3

#String Concatenation
print("Sharpy is a" + " " + "shark")

#string replication
print("bark" * 2)

#multiple line
print("""
This is 
multiple line 
input
""")

#multiple line v2
print("this is\nmultiple\nline")

#escape character
print("tosun\'s balloon is red")

#raw strings
#ignores all special characters
print(r"this is\n a \"raw\"\n string")

#string index
st = "this is a string! Yea"

print(st[5])
print(st[-5])

#slicing strings
print(st[5:7])
print(st[-3:-1])

##beginning to point X
print(st[:4])
print(st[:-4])

##point x to end
print(st[18:])
print(st[-3:])

#stride parameter
print(st[:18:2])
print(st[::-2])

#reverse the string with stride
print(st[::-1])

#lenght of string
len(st)

#character count in string
#characters are case sensitive
st.count(" ")

st2 = "dandanakanda akan kan"

#finding a character's first index
st2.find("a")
st2.find("akan")

#start search from a string index to end index
st2.find("kan", 12)
st2.find("an", 12, 18)
st2.find("an", 12, -4)

#making characters lower or upper
st2.lower()
st2.upper()

#if all chracters are capital istitle() returns TRUE
st2.istitle()

#length of the string
len(st2)

#reversal form of string
reversed(st2)

#join() method combines string with element of input string
" ".join(st2)

#split() method splits data based on input
st2.split(" ")
st2.split("a")