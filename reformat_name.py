import sys

result = ""
for i in sys.argv[1].split(" "):
    result += i
    result += "\ "
print(result[:-2])
