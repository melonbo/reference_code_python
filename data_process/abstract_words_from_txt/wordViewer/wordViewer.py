import sys
import re
import sqlite3
import string
from PyQt5.QtWidgets import (QMainWindow, QAction, qApp, QApplication, QFileDialog,
                             QWidget, QTableWidgetItem, QAbstractItemView, QDialog,
                             QPushButton, QHBoxLayout, QVBoxLayout, QTableWidget, QTextEdit)
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QEvent, pyqtSignal

"""
database:
level   0:simple word     1:normal word       2:important word
"""

class myQTableWidget(QTableWidget):
    updateSignal = pyqtSignal(QtGui.QKeyEvent)

    def __ini__(self):
        super().__ini__()

    def keyPressEvent(self, event) -> None:
        self.updateSignal.emit(event)


class inputDialog(QDialog):
    _signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("输入文本")
        self.button_OK = QPushButton("OK")
        self.text_edit = QTextEdit()
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.button_OK)
        vbox.addWidget(self.text_edit)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.button_OK.clicked.connect(self.slot_button_ok_clicked)

    def slot_button_ok_clicked(self):
        data_str = self.text_edit.toPlainText()
        self.text_edit.clear()
        self._signal.emit(data_str)
        self.accept()

# noinspection PyAttributeOutsideInit
class mainGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.my_dict_db = sqlite3.connect("mydict.db")
        self.db_cursor = self.my_dict_db.cursor()
        self.words = []
        self.desktop_width = QApplication.desktop().screen(0).width()
        self.desktop_height = QApplication.desktop().screen(0).height()
        self.input_dialog = inputDialog()
        self.input_dialog._signal.connect(self.get_data_from_input_dialog)
        self.initUI()

    def initUI(self):
        menubar = self.menuBar()

        openFileAction = QAction(QIcon('file_open.png'), '&打开文件', self)
        openFileAction.setShortcut('Ctrl+O')
        openFileAction.triggered.connect(self.selectFile)

        openDialogAction = QAction(QIcon('file_open.png'), '&打开输入框', self)
        openDialogAction.setShortcut('Ctrl+P')
        openDialogAction.triggered.connect(self.open_input_dialog)

        loadSimpleWordsAction = QAction('&加载简单词', self)
        loadSimpleWordsAction.triggered.connect(self.load_simple_words)

        loadImportantWordsAction = QAction(QIcon(''), '&加载重要词', self)
        loadImportantWordsAction.triggered.connect(self.load_important_words)

        menu_open_file = menubar.addMenu('&File')
        menu_open_file.addAction(openFileAction)
        menu_open_file.addAction(openDialogAction)
        menu_open_file.addAction(loadSimpleWordsAction)
        menu_open_file.addAction(loadImportantWordsAction)

        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        menu_exit = menubar.addMenu('&Exit')
        menu_exit.addAction(exitAction)

        self.button_filter_simple_words = QPushButton('过滤简单词')
        self.button_set_simple_word = QPushButton('设为简单词')
        self.button_set_normal_word = QPushButton('设为普通词')
        self.button_set_important_word = QPushButton('设为重要词')
        self.button_filter_simple_words.clicked.connect(self.filter_simple_words)
        self.button_set_simple_word.clicked.connect(self.set_word_simple)
        self.button_set_normal_word.clicked.connect(self.set_word_nomal)
        self.button_set_important_word.clicked.connect(self.set_word_important)

        vbox = QVBoxLayout()
        vbox.addWidget(self.button_filter_simple_words)
        vbox.addWidget(self.button_set_simple_word)
        vbox.addWidget(self.button_set_normal_word)
        vbox.addWidget(self.button_set_important_word)

        self.table_words = myQTableWidget()
        self.table_words.setColumnCount(2)
        self.table_words.setRowCount(20)
        self.table_words.setHorizontalHeaderLabels(['english', 'chinese'])
        self.table_words.horizontalHeader().setStretchLastSection(True)
        self.table_words.horizontalHeader().setStyleSheet('QHeaderView::section{background:skyblue}')
        # self.table_words.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_words.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_words.installEventFilter(self)
        self.table_words.updateSignal.connect(self.receive_table_widget_event)

        hbox = QHBoxLayout()
        hbox.addWidget(self.table_words)
        hbox.addLayout(vbox)

        main_frame = QWidget()
        self.setCentralWidget(main_frame)
        main_frame.setLayout(hbox)

        self.setGeometry(self.desktop_width/5, self.desktop_height/5, self.desktop_width/2, self.desktop_height/2)
        self.setWindowTitle("wordViewer")
        self.statusBar().hide()

        self.show()

    def selectFile(self):
        file = QFileDialog.getOpenFileName(self, 'open file', './')

        if file[0]:
            print(file[0])
            self.display_words(self.extract_word_from_article(file[0]))

    def open_input_dialog(self):
        main_window_x = self.geometry().x()
        main_window_y = self.geometry().y()
        main_window_w = self.geometry().width()
        main_window_h = self.geometry().height()
        self.input_dialog.resize(main_window_w*0.8, main_window_h*0.8)
        self.input_dialog.move(main_window_x*1.1, main_window_y*1.1)
        result = self.input_dialog.exec()


    def get_data_from_input_dialog(self, data):
        line = data
        line = line.replace('-', ' ')
        line = line.replace("/", " ")
        line = line.replace("\\", " ")
        line = line.replace("'", " ")
        line = line.replace("[", " ")
        line = line.replace("]", " ")
        line = line.replace("%", " ")
        line = line.replace("&", " ")
        line = line.replace("_", " ")
        line = line.replace("(", " ")
        line = line.replace(")", " ")
        line = line.replace(".", " ")
        line = line.replace("\"", " ")
        line = line.replace(":", " ")
        for word in line.split():
            word = word.strip(string.punctuation + string.whitespace)
            word = word.lower()
            if word not in self.words:
                self.words.append(word)
        self.display_words(self.words)

    def load_simple_words(self):
        self.load_words_by_level(0)

    def load_important_words(self):
        self.load_words_by_level(2)

    def load_words_by_level(self, level):
        while self.table_words.rowCount():
            self.table_words.removeRow(self.table_words.rowCount() - 1)

        sql = "select english, chinese from DICT WHERE level = \"{0}\"".format(level)
        cursor = self.db_cursor.execute(sql)
        content = self.db_cursor.fetchall()

        for line in content:
            self.insert_item_into_table(line[0], line[1])

        self.table_words.resizeRowsToContents()
        self.table_words.selectRow(0)

    def insert_item_into_table(self, colum_01, colum_02):
        item_english = QTableWidgetItem(colum_01)
        item_chinese = QTableWidgetItem(colum_02)
        item_english.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item_chinese.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item_english.setFlags(item_english.flags() & (~Qt.ItemIsEditable))
        item_chinese.setFlags(item_chinese.flags() & (~Qt.ItemIsEditable))
        row = self.table_words.rowCount()
        self.table_words.insertRow(row)
        self.table_words.setItem(row, 0, item_english)
        self.table_words.setItem(row, 1, item_chinese)


    def filter_simple_words(self):
        current_row = self.table_words.currentRow()
        row_count = self.table_words.rowCount()
        while row_count > 0:
            if self.table_words.item(row_count-1, 0) == None:
                row_count -= 1
                continue

            word = self.table_words.item(row_count-1, 0).text()
            sql = "select level from DICT WHERE english = \"{0}\"".format(word)
            cursor = self.db_cursor.execute(sql)
            content = self.db_cursor.fetchone()
            if content[0]==0:
                self.table_words.removeRow(row_count-1)

            row_count-=1
        row_count = self.table_words.rowCount()
        if current_row < row_count:
            self.table_words.selectRow(current_row)
        else:
            self.table_words.selectRow(0)


    def extract_word_from_article(self, filename):
        fin = open(filename)

        for line in fin:
            line = line.replace('-', ' ')
            line = line.replace("/", " ")
            line = line.replace("\\", " ")
            line = line.replace("'", " ")
            line = line.replace("[", " ")
            line = line.replace("]", " ")
            line = line.replace("%", " ")
            line = line.replace("&"," ")
            line = line.replace("_", " ")
            line = line.replace("(", " ")
            line = line.replace(")", " ")
            line = line.replace(".", " ")
            line = line.replace("\"", " ")
            line = line.replace(":", " ")
            for word in line.split():
                word = word.strip(string.punctuation + string.whitespace)
                word = word.lower()
                if word not in self.words:
                    self.words.append(word)

        print("english word number: ", len(self.words))
        return self.words

    def set_word_simple(self):
        self.set_current_item_level(0)

    def set_word_nomal(self):
        self.set_current_item_level(1)

    def set_word_important(self):
        self.set_current_item_level(2)

    def display_words(self, words):
        while self.table_words.rowCount():
            self.table_words.removeRow(self.table_words.rowCount() - 1)
        print(words)

        for word in words:
            sql = "select chinese from DICT WHERE english = \"{0}\"".format(word)
            cursor = self.db_cursor.execute(sql)
            trans = self.db_cursor.fetchone()
            if trans:
                self.insert_item_into_table(word, trans[0])

        self.table_words.resizeRowsToContents()
        self.table_words.selectRow(0)

    def receive_table_widget_event(self, event):
        if (event.key() == Qt.Key_D):
            self.set_current_item_level(0)
        if (event.key() == Qt.Key_S):
            self.set_current_item_level(2)
        if (event.key() == Qt.Key_N):
            self.set_current_item_level(1)
        if (event.key() == Qt.Key_U):
            print('测试：U')


    def set_current_item_level(self, level):
        current_row = self.table_words.currentIndex().row()
        if self.table_words.item(current_row, 0) == None:
            return;

        current_english_word = self.table_words.item(current_row, 0).text()
        if current_english_word:
            sql = "update DICT SET level = {0} WHERE english = \"{1}\"".format(level, current_english_word)
            print(sql)
        self.db_cursor.execute(sql)
        self.my_dict_db.commit()

        if level == 0:
            self.table_words.removeRow(current_row)
            if current_row == self.table_words.rowCount()-1:
                self.table_words.selectRow(current_row-1)
            else:
                self.table_words.selectRow(current_row)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = mainGUI()
    gui.show()
    sys.exit(app.exec_())