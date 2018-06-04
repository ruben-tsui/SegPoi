# -*- coding: utf-8 -*-
"""
Last updated on Thu Apri 2400 09:21:05 2018
@author: RubenTsui@gmail.com
Purpose:
  Segment (tokenize) and/or POS-tag file in traditional or simplified Chinese, or in English, using
  the Stanford POS tagger via the Python wrapper available from:
  https://github.com/Lynten/stanford-corenlp
Installation: pip install stanfordcorenlp
"""

from stanfordcorenlp import StanfordCoreNLP

def lineCount(fn):
    count = 0
    with open(fn, "r", encoding="UTF-8") as f:
        for line in f:
            count += 1
    return count

class Zhs:
    """
    Use the Stanford CoreNLP to segment Chinese-simplified text
    """
    def __init__(self, fni, fno, pos, lib, window):
        self.fni = fni
        self.fi_linecount = lineCount(fni)
        self.fno = fno
        self.pos = pos
        self.lib = lib
        self.window = window
        self.numLineProcessed = 0

    def segment(self):
        """
        fni:  str;  input file name with path
        fno:  str;  output file name with path
        lang: str;  language code
        pos:  bool; POS tags included
        n:    int;  no. of lines processed
        """
        from PyQt5.QtWidgets import QApplication

        nlp = StanfordCoreNLP(self.lib, lang='zh')
        print("Finished initializing Stanford CoreNLP")
        
        fi  = open(self.fni, "r", encoding="UTF-8")
        fo  = open(self.fno, "w", encoding="UTF-8", newline="\n")

        n = 0
        for line in fi:
            n += 1
            if line.strip() == '':
                fo.write("\n")
                continue
            ## the next 2 lines are crucial
            line = line.replace("　", "")
            line = line.replace(" ", "")
            # write zht tokens with pos tags
            if self.pos:
                postags = nlp.pos_tag(line) # get pos tag for zhs string (line is in zhs)
                for (i, (w, pos)) in enumerate(postags):
                    fo.write(w + "_" + pos + " ")
            else:
                tokens = nlp.word_tokenize(line)
                for w in tokens:
                    fo.write(w + " ")
            fo.write("\n")
            if n % 10 == 0:
                self.window.ui.progressBar.setValue(round(100 * n / self.fi_linecount, 0))
                self.window.ui.progressBar.repaint()
                QApplication.processEvents()
        self.window.ui.progressBar.setValue(100)
        self.window.ui.progressBar.repaint()

        fi.close()
        fo.close()
        nlp.close()
        self.numLineProcessed = n
        return n


class Zht:
    """
    Use the Stanford CoreNLP to segment Chinese-simplified text
    """
    def __init__(self, fni, fno, pos, lib, window):
        self.fni = fni
        self.fi_linecount = lineCount(fni)
        self.fno = fno
        self.pos = pos
        self.lib = lib
        self.window = window
        self.numLineProcessed = 0

    def segment(self):
        """
        fni:  str;  input file name with path
        fno:  str;  output file name with path
        lang: str;  language code
        pos:  bool; POS tags included
        n:    int;  no. of lines processed
        """
        import copy
        from PyQt5.QtWidgets import QApplication
        from opencc import OpenCC

        openCC = OpenCC('t2s')  # convert from Traditional-to-Simplified
        nlp = StanfordCoreNLP(self.lib, lang='zh')
        print("Finished initializing Stanford CoreNLP")
        count = lineCount(self.fni)
        fi  = open(self.fni, "r", encoding="UTF-8")
        fo  = open(self.fno, "w", encoding="UTF-8", newline="\n")

        n = 0
        for line_zht in fi:
            n += 1
            if line_zht.strip() == '':
                fo.write("\n")
                continue
            ## the next 2 lines are crucial
            line_zht = line_zht.replace("　", "")
            line_zht = line_zht.replace(" ", "")
            line = openCC.convert(line_zht) # convert zht to zhs

            # 
            postags = nlp.pos_tag(line) # get pos tag for zhs string (line is in zhs)
            tokens = []
            for (i, (w, pos)) in enumerate(postags):
                tokens.append(w)
            tokens_zhs = copy.deepcopy(tokens)
            tokens_zht = []  # initialize list to hold segmented zht line
            # write zht tokens with pos tags
            while len(tokens_zhs) > 0:
                t = tokens_zhs.pop(0)  # remove leftmost zhs token and save to variable t
                m = len(t)  # no. of characters in token
                tokens_zht.append(line_zht[0:m])  # add corresponding zht token to tokens[]
                line_zht = line_zht[m:]  # delete token from zht line (from beginning of string)
                
            if self.pos:
                for (i, (w, pos)) in enumerate(postags):
                    fo.write(tokens_zht[i] + "_" + pos + " ")
            else:
                for (i, (w, pos)) in enumerate(postags):
                    fo.write(tokens_zht[i] + " ")
            fo.write("\n")
            if n % 50 == 0:
                self.window.ui.progressBar.setValue(round(100 * n / self.fi_linecount, 0))
                self.window.ui.progressBar.repaint()
                QApplication.processEvents()
        self.window.ui.progressBar.setValue(100)
        self.window.ui.progressBar.repaint()

        fi.close()
        fo.close()
        nlp.close()
        self.numLineProcessed = n
        return n

        
#class Zht_ICTCLAS(Zht):
    