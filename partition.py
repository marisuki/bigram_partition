f = open("icwb2-data/gold/PickDawnBlossomsAtDusk.utf8", encoding="utf-8")
line = f.readline()
tmp = []
pos = 0
for i in range(len(line)):
    if line[i] == "，" or line[i] == "。" or line[i] == "”" or line[i] == "；" or line[i] == "？" or line[i] == "！":
        tmp.append(line[pos:i+1])
        pos = i+1
f = open("icwb2-data/gold/partitions.utf8", "w", encoding="utf8")
for item in tmp:
    f.write(item)
    f.write("\n")
