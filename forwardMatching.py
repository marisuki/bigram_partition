import PatriciaTree_dict
import configparser


class forwardtree(object):
    def __init__(self):
        self.pattree_forward = PatriciaTree_dict.Patricia("forward")
        self.config = configparser.ConfigParser()
        self.config.read_file(open("config.ini"))
        self.test_path = self.config.get("GlobalTestingSet", "test_file")

    def run(self):
        f_test = open(self.test_path, encoding="utf8")
        search_len = int(self.config.get("PatriciaTree", "max_word_len"))
        ans = []
        for line in f_test:
            line = line.split()[0]
            tmp = []
            i = 0
            while i != len(line):
                if i+search_len < len(line):
                    j = self.pattree_forward.find(line[i: i+search_len])
                else:
                    j = self.pattree_forward.find(line[i:])
                tmp.append(i + j)
                i += j
            ans.append(tmp)
        return ans

    def single_step(self, line):
        search_len = int(self.config.get("PatriciaTree", "max_word_len"))
        line = line.split()[0]
        tmp = []
        i = 0
        while i != len(line):
            if i + search_len < len(line):
                j = self.pattree_forward.find(line[i: i + search_len])
            else:
                j = self.pattree_forward.find(line[i:])
            tmp.append(i + j)
            i += j
        return tmp
