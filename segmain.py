# -*- coding: utf-8 -*-

import time, datetime, os
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

from PyQt5 import QtCore, QtGui, QtWidgets
from cat_ui import Ui_SegPoi

CWD = os.getcwd()
print("Current working directory is {}".format(CWD))
LANG = 'zht'

def openfile_dialog(dir):
    fname = QtWidgets.QFileDialog.getOpenFileName(None, "請選擇輸入檔 Select input file", dir, filter="All files (*)")
    return fname

def getTokenizationLibrary(window):
    tokLib = ['StanfordCoreNLP', 'NLPIR', 'Jieba', 'spaCy']
    tl = tokLib[0] # default
    if window.ui.radioButton_tokLib_ICTCLAS.isChecked():
        tl = tokLib[1]
    elif window.ui.radioButton_tokLib_Jieba.isChecked():
        tl = tokLib[2]
    elif window.ui.radioButton_tokLib_spaCy.isChecked():
        tl = tokLib[3]
    return tl

def getPosStatus(window):
    return window.ui.checkBox_POS.isChecked()
    
def processSegment(fni, fno, lang, pos, lib, window):
    start_time = time.time()
    # Update message pane
    window.ui.textBrowser.append('Processing file {}'.format(fni))
    window.ui.textBrowser.repaint()
    # Determine the tokenization library selected
    tokLib = getTokenizationLibrary(window)
    
    if lang == 'zht':
        if tokLib == 'StanfordCoreNLP':
            from SegPos import Zht
            doc = Zht(fni, fno, pos, lib, window)
        elif tokLib == 'NLPIR':
            if getPosStatus(window):
                from SegPos1 import Zht_pos
                doc = Zht_pos(fni, fno, pos, lib, window)
            else:
                from SegPos1 import Zht
                doc = Zht(fni, fno, pos, lib, window)
    elif lang == 'zhs':
        if tokLib == 'StanfordCoreNLP':
            from SegPos import Zhs
            doc = Zhs(fni, fno, pos, lib, window)
        elif tokLib == 'NLPIR':
            if getPosStatus(window):
                from SegPos1 import Zhs_pos
                doc = Zhs_pos(fni, fno, pos, lib, window)
            else:
                from SegPos1 import Zhs
                doc = Zhs(fni, fno, pos, lib, window)
    n = doc.segment()
    elapsed_time = round(time.time() - start_time, 2)
    window.ui.textBrowser.append('File written to {}'.format(fno))
    window.ui.textBrowser.repaint()
    window.ui.textBrowser.append('Processed a total of {n} lines in {t} seconds'.format(n=n, t=elapsed_time))
    window.ui.textBrowser.append("=========================================\n")
    window.ui.textBrowser.repaint()
    return None

def initialize(window):
    window.ui.myTextInput.clear()
    window.ui.myTextInput_2.clear()
    window.ui.myTextInput_Convert_fileIn.clear()
    window.ui.myTextInput_Convert_fileOut.clear()
    window.ui.TextInput_lib.setText("./")

class Window(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        # object created in GuiLinkExample.py:
        self.ui = Ui_SegPoi()
        self.ui.setupUi(self)
        # connect to actions in GUI
        ### SEGPOS
        # Open input file button
        self.ui.toolButton.clicked.connect(self.on_click)
		# "Segment" button
        self.ui.pushButton_Segment.clicked.connect(self.on_click_SegPos_OpenFile)
		# Debug Check button
        self.ui.pushButton_Check.clicked.connect(self.on_click3)
		# "POS Checkbox" button
        self.ui.checkBox_POS.clicked.connect(self.on_click4)
        ### CONVERT
        # Open input file button
        self.ui.toolButton_Convert.clicked.connect(self.on_click_Convert)
        #
        self.ui.pushButton_Convert.clicked.connect(self.on_click_Convert_OpenFile)
        #
        initialize(self)

    def on_click(self):
        global CWD
        fn = openfile_dialog(CWD)
        fullpathfilename = fn[0]
        secext = 'seg' # file secondary extension
        if self.ui.checkBox_POS.isChecked():
            secext = 'pos'
        if fullpathfilename != '':
            (fn, ext) = os.path.splitext(fullpathfilename)
            self.ui.myTextInput.setText(fullpathfilename)
            self.ui.myTextInput_2.setText(fn + '.' + secext + ext)
            CWD = os.path.dirname(fullpathfilename)
            print("Current working directory is {}".format(CWD))
			
    def on_click_SegPos_OpenFile(self):
        global LANG
        fni = self.ui.myTextInput.text()
        fno = self.ui.myTextInput_2.text()
        pos = self.ui.checkBox_POS.isChecked()
        lib = self.ui.TextInput_lib.text()
        print("Input file to be processed: {}".format(fni))
        print("Output file: {}".format(fno))
        print("POS = {}".format(pos))
        print("Stanford CoreNLP lib: {}".format(lib))
        self.ui.textBrowser.append("Begin word segmentation/POS tagging on " +
            f"{datetime.datetime.now():%Y-%m-%d at %H:%M:%S}")
        self.ui.textBrowser.repaint()
        n = 0
        if self.ui.radioButton_en.isChecked():
            LANG = 'en'
        elif self.ui.radioButton_zht.isChecked():
            LANG = 'zht'
        elif self.ui.radioButton_zhs.isChecked():
            LANG = 'zhs'
        if os.path.exists(fni) and fno != '':
            self.ui.progressBar.textVisible = True
            ret = processSegment(fni, fno, LANG, pos, lib, self)
            #if ret != None:
            #    #self.ui.listWidget.addItems(ret)
            #    self.ui.textBrowser.setPlainText("\n".join(ret))
        else:
            self.ui.textBrowser.append("Input or output file is empty. Nothing to do!")
            self.ui.textBrowser.repaint()
            
 
    # Debug Check button
    def on_click3(self):
        print("CWD = {}".format(CWD))
        print("LANG = {}".format(LANG))
        # check if POS is checked
        if self.ui.checkBox_POS.isChecked():
            print("POS is checked!")
        else:
            print("POS excluded")
        # check which language button is checked
        if self.ui.radioButton_en.isChecked():
            print("Lang: en checked")
        elif self.ui.radioButton_zht.isChecked():
            print("Lang: zht checked")
        if self.ui.radioButton_zhs.isChecked():
            print("Lang: zhs checked")

    def on_click4(self):
        print("checkBox_POS clicked")
        fno = self.ui.myTextInput_2.text()
        if self.ui.checkBox_POS.isChecked():
            fno = fno.replace(".seg.", ".pos.")
        else:
            fno = fno.replace(".pos.", ".seg.")
        self.ui.myTextInput_2.setText(fno)
        
    def on_click_Convert(self):
        global CWD
        fn = openfile_dialog(CWD)
        fullpathfilename = fn[0]
        secext = 'con' # file secondary extension
        if fullpathfilename != '':
            (fn, ext) = os.path.splitext(fullpathfilename)
            self.ui.myTextInput_Convert_fileIn.setText(fullpathfilename)
            self.ui.myTextInput_Convert_fileOut.setText(fn + '.' + secext + ext)
            CWD = os.path.dirname(fullpathfilename)
            print("Current working directory is {}".format(CWD))
			

    def on_click_Convert_OpenFile(self):
        fni = self.ui.myTextInput_Convert_fileIn.text()
        fno = self.ui.myTextInput_Convert_fileOut.text()
        #pos = self.ui.checkBox_POS.isChecked()
        print("Input file to be processed: {}".format(fni))
        print("Output file: {}".format(fno))
        #print("Conversion direction = {}".format(pos))
        self.ui.textBrowser.append("Begin conversion (using OpenCC) on " +
            f"{datetime.datetime.now():%Y-%m-%d at %H:%M:%S}")
        self.ui.textBrowser.repaint()
        # determine conversion direction from UI
        conversion_direction = 's2tw' # default (see OpenCC docs)
        if self.ui.radioButton_zht2zhs.isChecked():
            conversion_direction = 't2s'
        elif self.ui.radioButton_zhs2zht.isChecked():
            conversion_direction = 's2tw'
        elif self.ui.radioButton_enLowercse.isChecked():
            conversion_direction = 'enlc'
        if os.path.exists(fni) and fno != '':
            #ret = processSegment(fni, fno, LANG, pos, lib, self)
            if conversion_direction in ['s2tw', 't2s']:
                start_time = time.time()
                import Convert
                doc = Convert.ZhtZhsConvert(fni, fno, conversion_direction, self)
                #line_count = Convert.lineCount(fni)
                ret = doc.convert()
                elapsed_time = round(time.time() - start_time, 2)
                self.ui.textBrowser.append("Conversion complete in {} seconds".format(elapsed_time))
                self.ui.textBrowser.repaint()
            elif conversion_direction in ['enlc']:
                pass
        else:
            self.ui.textBrowser.append("Input or output file is empty. Nothing to do!")
            self.ui.textBrowser.repaint()
  

# This creates the GUI window:
if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    #window.initialize()
    sys.exit(app.exec_())
#=========================================================
