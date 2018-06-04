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
from opencc import OpenCC


def lineCount(fn):
    count = 0
    with open(fn, "r", encoding="UTF-8") as f:
        for line in f:
            count += 1
    return count


class ZhtZhsConvert:

    def __init__(self, fni, fno, direction, window):
        self.fni = fni
        self.fno = fno
        self.direction = direction
        self.numLineProcessed = 0
        self.window = window

    def convert(self):

        from PyQt5.QtWidgets import QApplication
        count = lineCount(self.fni)
        
        openCC = OpenCC(self.direction)  # direction of conversion
        fi  = open(self.fni, "r", encoding="UTF-8")
        fo  = open(self.fno, "w", encoding="UTF-8", newline="\n")

        n = 0
        for line in fi:
            n += 1
            txt = openCC.convert(line)
            fo.write(txt)  # wirte converted text to output
            #completed = 100 * n / count
            if n % 100 == 0:
                self.window.ui.progressBar.setValue(round(100 * n / count, 0))
                self.window.ui.progressBar.repaint()
                QApplication.processEvents()
            #self.window.update()
        fi.close()
        fo.close()
        self.window.ui.progressBar.setValue(100)
        self.window.ui.progressBar.repaint()
        self.numLineProcessed = n
        return self.numLineProcessed


#import time
#start_time = time.time()
#print(lineCount("C:/NLP/collo/chinatimes2014.txt"))
#elapsed_time = round(time.time() - start_time, 2)
#print("Elapsed time: {sec} sec".format(sec=elapsed_time))
