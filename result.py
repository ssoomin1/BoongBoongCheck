
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel

class resultWindow(QWidget):
    def __init__(self,parent):
        super().__init__()
        self.setupUI()
        self.setWindowTitle("인증결과")
        self.parent = parent

    def setupUI(self):
        self.setFixedSize(324,137)
        self.setFont(QtGui.QFont("나눔스퀘어",11))
        self.resultLabel = QLabel(self)
        self.resultLabel.setGeometry(20,40,300,20)
        self.resultLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.OkayBtn = QPushButton("확인",self)
        self.OkayBtn.setGeometry(120,95,91,31)
        self.OkayBtn.clicked.connect(self.close)



