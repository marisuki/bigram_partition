import configparser


class Patricia(object):
    def __init__(self, mode="forward"):
        self.config = configparser.ConfigParser()
        self.config.read_file(open("config.ini"))
        self.train_file = self.config.get("GlobalTrainingSet", "Patricia_train_word")
        self.tree_dict = {}
        self.mode = (mode == "forward")
        self.make_tree()
        # print(self.tree_dict)

    def make_tree(self):
        f_in = open(self.train_file, encoding="utf8")
        for word in f_in:
            word = word.split()[0]
            dicc = self.tree_dict
            if self.mode:
                pos = 0
                while pos != len(word):
                    if word[pos] in dicc:
                        dicc = dicc[word[pos]]
                    else:
                        dicc[word[pos]] = {}
                        dicc = dicc[word[pos]]
                    pos += 1
                    if pos == len(word):
                        dicc["$"] = -1
            else:
                pos = len(word)-1
                while pos != -1:
                    if word[pos] in dicc:
                        dicc = dicc[word[pos]]
                    else:
                        dicc[word[pos]] = {}
                        dicc = dicc[word[pos]]
                    pos -= 1
                    if pos == -1:
                        dicc["$"] = -1

    def find(self, seq):
        find_dic = self.tree_dict
        if self.mode:
            pos = -1
            for i in range(0, len(seq), 1):
                if seq[i] in find_dic:
                    find_dic = find_dic[seq[i]]
                else:
                    break
                if "$" in find_dic:
                    pos = i + 1
        else:
            pos = -1
            for i in range(len(seq)-1, -1, -1):
                if seq[i] in find_dic:
                    find_dic = find_dic[seq[i]]
                else:
                    break
                if "$" in find_dic:
                    pos = len(seq) - i
        if pos == -1:
            pos = 1
        return pos

    def insert_bigram(self, word1, word2):
        if not self.mode:
            print("[Warning] rejected.")
            return self.tree_dict
        dicc = self.tree_dict
        pos = 0
        while pos != len(word1):
            if word1[pos] in dicc:
                dicc = dicc[word1[pos]]
            else:
                dicc[word1[pos]] = {}
                dicc = dicc[word1[pos]]
            pos += 1
            if pos == len(word1):
                if ("$" not in dicc) or (dicc["$"] == -1):
                    dicc["$"] = {word2: 1, "$$": 1}
                else:
                    if word2 in dicc["$"]:
                        dicc["$"][word2] += 1
                        dicc["$"]["$$"] += 1
                    else:
                        dicc["$"][word2] = 1
                        dicc["$"]["$$"] += 1
        return self.tree_dict

    def find_bigram(self, keyword, testword):
        print(keyword)
        if not self.mode:
            print("[Warning] Rejected.")
            return 0
        dicc = self.tree_dict
        pos = 0
        while pos != len(keyword):
            if keyword[pos] in dicc:
                dicc = dicc[keyword[pos]]
            else:
                break
            pos += 1
            if pos == len(keyword):
                try:
                    if "$" in dicc and testword in dicc["$"]:
                        return float(dicc["$"][testword])/float(len(dicc))
                    else:
                        return 0.0
                except:
                    pass
        return 0.0
