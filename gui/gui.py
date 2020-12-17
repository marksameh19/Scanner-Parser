# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scanner_test.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import re

def match_array(iterator,type):
    matches = []
    for x in iterator:
        matches.append([x,type])
    return matches

def sortFunc(x):
    return x[0].span()[0]+x[0].span()[1]*0.1

def format_tokens(tokens):
    final_tokens = []
    for token in tokens:
        if token[1]=='reserved word':
         final_tokens.append([token[0].group(2),token[1]])
        else:
         final_tokens.append([token[0].group(1),token[1]])
    return final_tokens

def scan_to_tokens(lines):
    comment = re.sub("[{][^{}]*[}]", " ", lines)
    lines = comment.split('\n')
    tokens = []
    for line in lines:
        reserved_words_iterator = re.finditer(r"(\W|^)(read|if|then|else|end|repeat|until|write)(\W|$)", line)
        list_of_reserved_words_matches = match_array(reserved_words_iterator, 'reserved word')

        identifiers_iterator = re.finditer(r"(\b(?!(?:read|if|then|else|end|repeat|until|write)\b)[a-zA-Z]+)", line)
        list_of_identifiers_matches = match_array(identifiers_iterator, 'identifier')

        numbers_iterator = re.finditer('([0-9]+)', line)
        list_of_numbers_matches = match_array(numbers_iterator, 'number')

        symbols_iterator = re.finditer('(:=|-|=|;|[+*/<>()])', line)
        list_of_symbols_matches = match_array(symbols_iterator, 'special symbol')

        list_of_reserved_words_matches.extend(list_of_identifiers_matches)
        list_of_reserved_words_matches.extend(list_of_numbers_matches)
        list_of_reserved_words_matches.extend(list_of_symbols_matches)
        list_of_reserved_words_matches.sort(key=sortFunc)
        tokens.extend(list_of_reserved_words_matches)

    final_tokens = format_tokens(tokens)
    return final_tokens

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(969, 760)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(600, 50, 300, 550))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(420, 570, 100, 30))
        self.pushButton.setObjectName("pushButton")
        self.pushButton2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton2.setGeometry(QtCore.QRect(420, 500, 100, 30))
        self.pushButton2.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(40, 50, 300, 550))
        self.textEdit.setObjectName("textEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 969, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        def output_tokens():
            lines = self.textEdit.toPlainText()
            text = scan_to_tokens(lines)
            for token in text:
                self.textBrowser_2.append(str(token))
            with open('outputFile.txt', 'w') as filehandle:
                for token in text:
                    filehandle.write('%s\n' % token)

        def clear():
            self.textBrowser_2.clear()

        self.pushButton.clicked.connect(output_tokens)
        self.pushButton2.clicked.connect(clear)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Start"))
        self.pushButton2.setText(_translate("MainWindow", "Clear"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
