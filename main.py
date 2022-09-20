from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import os
import sys
import random

def get_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    else:
        return filename

def answer():
    n = random.randint(1, 51)
    if n>0 and n<=10:
        res = "언젠가는"
    elif n>10 and n<=20:
        res = "가만히 있어"
    elif n>20 and n<=30:
        res = "그것도 안 돼"
    elif n>30 and n<=40:
        res = "다시 한 번 물어봐"
    elif n>40 and n<=50:
        res = "안 돼"
    else:
        res = "그럼"
    return res

class CustomBar(QWidget):

    def __init__(self, parent):
        super(CustomBar, self).__init__()
        self.parent = parent
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.title = QLabel("마법의 소라고동")

        self.title.setFixedHeight(35)
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)

        self.title.setStyleSheet("""
            background-color: black;
            color: white;
        """)
        self.setLayout(self.layout)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.right_menu)

    def right_menu(self, pos):
        menu = QMenu()
        exit_option = menu.addAction('종료')
        exit_option.triggered.connect(lambda: sys.exit())
        menu.exec_(self.mapToGlobal(pos))

class MDWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.initUI()

    def initUI(self):

        self.question_box = QPlainTextEdit()
        self.question_box.LineWrapMode()
        self.answer_btn = QPushButton("질문하기")
        self.answer_lbl = QLabel("대답 : ")

        self.answer_btn.clicked.connect(self.click_btn)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.question_box)
        self.main_layout.addWidget(self.answer_btn)
        self.main_layout.addWidget(self.answer_lbl)

        self.setLayout(self.main_layout)

    def click_btn(self):
        self.question_box.clear()
        self.answer_lbl.setText(f"대답 : {answer()}")

class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.initUI()
        self.modal = MDWindow()

    def initUI(self):
        self.setStyleSheet("background-color: black;")

        self.p_label = QLabel()
        self.p_label.setPixmap(QPixmap(get_path('image1.png')))

        main_layout = QVBoxLayout()
        main_layout.addWidget(CustomBar(self))
        main_layout.addWidget(self.p_label)

        main_layout.setContentsMargins(0,0,0,0)
        main_layout.addStretch(-1)
        
        self.setLayout(main_layout)

        self.customContextMenuRequested.connect(self.right_menu)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

    def open_quest(self):
        self.modal.move(self.pos().x()+255, self.pos().y())
        self.modal.resize(200, self.frameGeometry().height())
        if(self.modal.isVisible()):
            self.modal.hide()
        else:
            self.modal.show()

    def right_menu(self, pos):
        menu = QMenu()
        exit_option = menu.addAction('소라고동님!')
        exit_option.triggered.connect(self.open_quest)
        menu.exec_(self.mapToGlobal(pos))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.moveFlag = True
            self.movePosition = event.globalPos() - self.pos()
            self.setCursor(QCursor(Qt.OpenHandCursor))
            event.accept()

    def mouseMoveEvent(self, event):
        try:
            if Qt.LeftButton or self.moveFlag:
                c_pos = event.globalPos() - self.movePosition
                self.move(c_pos)
                self.modal.move(c_pos.x()+255, c_pos.y())
                event.accept()
        except:
            pass
    def mouseReleaseEvent(self, QMouseEvent):
        self.moveFlag = False
        self.setCursor(Qt.CrossCursor)


class Main(QObject):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.gui = Window()          
        self.gui.show()

if __name__ == "__main__":
    # print(get_path('image1.png'))
    app = QApplication(sys.argv)
    main = Main(app)
    sys.exit(app.exec_())