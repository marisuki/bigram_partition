import forwardMatching
import backwardMatching
import configparser
import numpy as np

config = configparser.ConfigParser()
config.read_file(open("config.ini"))


class biGram(object):
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read_file(open("config.ini"))
        self.Forward = forwardMatching.forwardtree()
        self.Backward = backwardMatching.backwardtree()
        self.stopwords = {"，", "‘", "’", "。", "“", "”", "：", "；", "《", "》", "？", "！", "￥", "（", "）", "【", "】"}
        self.dic = {}
        self.sum = 0
        self.construct_tree()

    def find_diff(self):
        f = open(config.get("GlobalTestingSet", "test_file"), encoding="utf8")
        ans = []
        for line in f:
            ans1, ans2 = self.Forward.single_step(line), self.Backward.single_step(line)
            if ans1[:-1] != ans2:
                print(line)
                print(ans1[:-1])
                print(ans2)
                try:
                    ann = self.exe_diff(line, ans1[:-1], ans2)
                except:
                    ann = ans1[:-1]
                print(ann)
                ann.append(ans1[-1])
                ans.append(ann)
            else:
                ans.append(ans1)
        return ans

    def construct_tree(self):
        f = open(config.get("GlobalTrainingSet", "train_file"), encoding="utf8")
        cnt = 1
        for line in f:
            if line[0] == "“":
                line = line[1:]
            cnt += 1
            if cnt % 1000 == 0:
                print("%d/86924" % cnt)
            line = line.split()
            for it in line:
                if it not in self.dic:
                    self.dic[it] = 1
                else:
                    self.dic[it] += 1
                self.sum += 1
            for i in range(len(line)-1):
                key, follow = line[i], line[i+1]
                if key in self.stopwords or follow in self.stopwords:
                    continue
                else:
                    self.Forward.pattree_forward.insert_bigram(key, follow)

    def exe_diff(self, line, ans1, ans2):
        # fact: \sum ln p(w2|w1)
        set1 = {i for i in ans1}
        set = {i for i in ans2}.intersection(set1)
        crosspoi = sorted([i for i in set])
        chip, pos, hold, flag = [], 0, 0, True
        for it in crosspoi:
            while it != ans1[pos]:
                pos += 1
                flag = False
            if not flag:
                chip.append((hold, ans1[pos]))
            pos += 1
            flag = True
            hold = it
        if hold != ans1[-1]:
            chip.append((hold, len(line)))
        print(chip)
        for chipping in chip:
            beg, end = 0, 0
            for i in range(len(ans1)):
                if ans1[i] == chipping[0]:
                    beg = i
                if ans1[i] == chipping[1]:
                    end = i
            ch1 = ans1[beg:end+1]
            beg, end = 0, 0
            for i in range(len(ans2)):
                if ans2[i] == chipping[0]:
                    beg = i
                if ans2[i] == chipping[1]:
                    end = i
            ch2 = ans2[beg:end+1]
            print(ch1, ch2)
            lis1, lis2 = [], []
            if len(ch1) == 2:
                ch1 = [0] + ch1
            if len(ch2) == 2:
                ch2 = [0] + ch2
            if len(ch1) == 1 or len(ch2) == 1:
                continue
            for i in range(1, len(ch1)):
                lis1.append(line[i-1: i])
            for i in range(1, len(ch2)):
                lis2.append(line[i-1: i])
            # scoring
            score1, score2 = 0, 0
            if len(lis1) < 1 or len(lis2) < 1:
                continue
            if lis1[0] in self.dic:
                score1 = np.log(self.dic[lis1[0]]/self.sum)
            else:
                score1 = np.log(0.1/self.sum)
            if lis2[0] in self.dic:
                score2 = np.log(self.dic[lis2[0]]/self.sum)
            else:
                score2 = np.log(0.1/self.sum)
            for i in range(1, len(lis1)):
                score1 += np.log(self.Forward.pattree_forward.find_bigram(lis1[i-1], lis1[i])+0.01)
            for i in range(1, len(lis2)):
                score2 += np.log(self.Forward.pattree_forward.find_bigram(lis2[i-1], lis2[i])+0.01)
            if score1 < score2:
                ans1 = ans1[:beg] + ch2 + ans1[end+1:]
        return ans1


if __name__ == "__main__":
    bg = biGram()

    bg.find_diff()
