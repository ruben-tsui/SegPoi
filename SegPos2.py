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

import pynlpir

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
        self.pos = window.ui.checkBox_POS.isChecked()
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


class Zht_pos:
    """
    Use the Stanford CoreNLP to segment Chinese-simplified text
    """
    def __init__(self, fni, fno, pos, lib, window):
        self.fni = fni
        self.fi_linecount = lineCount(fni)
        self.fno = fno
        self.pos = window.ui.checkBox_POS.isChecked()
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
        pynlpir.open(encoding="utf-8")
        print("Finished initializing ITCLAS/NLPIR")
        count = lineCount(self.fni)
        fit  = open(self.fni, "r", encoding="UTF-8")
        fot  = open(self.fno, "w", encoding="UTF-8", newline="\n")

        sep = " " # separator of Chinese tokens (space by default)
        n = 0
        for linet in fit:

            n += 1
            if (linet.strip() == ''): # empty string
                fot.write("\n")
                continue
            lines = openCC.convert(linet.strip())
            lines_seg = pynlpir.segment(lines, pos_tagging=True, pos_names=None) 
            # segment with optional POS-tagging

            # The following segments the zht text according to the
            # segmentation patterns obtained from NLPIR above
            tokens   = []  # initialize list to hold 'words' of segmented zht line
            pos_tags = []  # initialize list to hold pos tags of segmented words
            while len(lines_seg) > 0:  # loop until nothing is left in lines_seg
                t, p = lines_seg.pop(0)  # remove leftmost zhs token and save to variable t0
                m = len(t)  # no. of characters in token
                tokens.append(linet[0:m])  # add corresponding zht token to tokens[]
                pos_tags.append(p)
                linet = linet[m:]  # delete token from zht line (from beginning of string)

            #fot.write(sep.join(tokens)+"\n")  # wirte zht-seg output
            tok_pos = ["{}_{}".format(x, y) for x,y in zip(tokens, pos_tags)]  # list of tok_pos pairs
            fot.write(sep.join(tok_pos)+"\n")
            #if (n == 1): break
            if n % 50 == 0:
                self.window.ui.progressBar.setValue(round(100 * n / self.fi_linecount, 0))
                self.window.ui.progressBar.repaint()
                QApplication.processEvents()
        self.window.ui.progressBar.setValue(100)
        self.window.ui.progressBar.repaint()

        fit.close()
        fot.close()
        pynlpir.close()
        self.numLineProcessed = n
        return n

    