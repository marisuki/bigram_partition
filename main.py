import forwardMatching
import backwardMatching
import bigramMatching
import configparser

config = configparser.ConfigParser()
config.read_file(open("config.ini"))


def tt():
    test_path = config.get("GlobalTestingSet", "test_file")
    f_test = open(test_path, encoding="utf8")
    BM = backwardMatching.backwardtree()
    FM = forwardMatching.forwardtree()
    ansB, ansF, cnt = [], [], 0
    for line in f_test:
        cnt += 1
        # print(line)
        ansB.append(BM.single_step(line))
        ansF.append(FM.single_step(line))
        # print(ansB[len(ansB)-1])
        # print(ansF[len(ansF)-1])
        if cnt % 100 == 0:
            print("%d/3985" % cnt)
    return ansB, ansF


def examine(ans):
    rule = config.get("GlobalTestingSet", "test_rule")
    f = open(rule, encoding="utf8")
    correct, tot, pos = 0, 0, 0
    for line in f:
        line = line.split()
        tmp, test = [0], ans[pos]
        print(line)
        for item in line:
            tmp.append(tmp[len(tmp)-1]+len(item))
        print(tmp[1:])
        print(test)
        tmp = {i for i in tmp[1:]}
        for i in range(len(test)):
            if test[i] in tmp:
                correct += 1
        correct -= abs(len(tmp) - len(test))
        tot += len(tmp)
        pos += 1
    print("accuracy=%.5f" % (correct/tot))


def newPart():
    f = open("icwb2-data/gold/partitions.utf8", "r", encoding="utf8")
    fw = open("res.utf8", "w", encoding="utf8")
    FM = forwardMatching.forwardtree()
    ans = []
    for line in f:
        ans.append(FM.single_step(line))
        line = line.split()[0]
        s, last = "", 0
        for i in ans[len(ans)-1]:
            s += line[last: i]
            s += "|"
            last = i
        s += line[last:]
        fw.write(s)
        fw.write("\n")


if __name__ == "__main__":
    bg = bigramMatching.biGram()
    anss = bg.find_diff()
    # ans1, ans2 = tt()
    examine(anss)  # test res: 0.8948 -> 0.9420/0.98->0.99
    #newPart()