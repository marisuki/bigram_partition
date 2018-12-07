import PatriciaTree_dict
import configparser


class backwardtree(object):
    def __init__(self):
        self.pattree_backward = PatriciaTree_dict.Patricia("backward")
        self.config = configparser.ConfigParser()
        self.config.read_file(open("config.ini"))
        self.test_path = self.config.get("GlobalTestingSet", "test_file")

    def run(self):
        f_test = open(self.test_path, encoding="utf8")
        search_len = int(self.config.get("PatriciaTree", "max_word_len"))
        ans = []
        for line in f_test:
            tmp = []
            i = len(line) - 1
            while i != 0:
                if i - search_len >= 0:
                    j = self.pattree_backward.find(line[i-search_len: i])
                else:
                    j = self.pattree_backward.find(line[:i])
                tmp.append(j)
                i -= j
            tmpp, flag = [tmp[-1]], 0
            if len(tmp) > 2:
                for i in range(len(tmp)-2, 0, -1):
                    tmpp.append(tmpp[flag]+tmp[i])
                    flag += 1
            ans.append(tmpp)
        return ans

    def single_step(self, line):
        search_len = int(self.config.get("PatriciaTree", "max_word_len"))
        tmp = []
        i = len(line) - 1
        while i != 0:
            if i - search_len >= 0:
                j = self.pattree_backward.find(line[i - search_len: i])
            else:
                j = self.pattree_backward.find(line[:i])
            tmp.append(j)
            i -= j
        tmpp, flag = [tmp[-1]], 0
        if len(tmp) > 2:
            for i in range(len(tmp) - 2, 0, -1):
                tmpp.append(tmpp[flag] + tmp[i])
                flag += 1
        return tmpp
