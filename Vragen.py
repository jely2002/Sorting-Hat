d = {}
with open("BusinessManagement.txt") as f:
    lines = f.read().split("\n")
for line in lines:
    split = line.split("\t")
    vraag = split.pop(0)
    d[vraag] = split
print (d)
