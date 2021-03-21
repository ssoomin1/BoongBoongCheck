import datetime
import sys
import pymysql
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QComboBox, QDialog, QMainWindow
from result import resultWindow

#아이디 중복확인 다이얼로그
class checkId_D(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setFont(QtGui.QFont("나눔스퀘어",9))
        self.setFixedSize(236,88)
        self.setWindowTitle("확인")
        self.resultL = QLabel(self)
        self.resultL.setAlignment(QtCore.Qt.AlignCenter)
        self.resultL.setFont(QtGui.QFont("나눔스퀘어",10))
        self.resultL.setGeometry(10, 10, 221, 41)
        
        self.okay = QPushButton("확인", self)
        self.okay.setGeometry(78, 50, 93, 28)
        self.okay.clicked.connect(self.close)


# 운전면허번호 확인 다이얼로그
class check_driveNum(QDialog):

    def __init__(self, name, birth, driveNum):
        super().__init__()
        self.name = name  # 이름
        self.birth = birth  # 생일
        self.dNum = driveNum  # 입력한 면허번호

        self.my_db = pymysql.connect(user="bb", passwd="1201", host="127.0.0.1", db="boongboong")
        self.cursor = self.my_db.cursor()

        self.setFont(QtGui.QFont("나눔스퀘어",11))
        self.setFixedSize(290,190)
        self.setWindowTitle("입력창")

        self.inputNumL = QLabel("식별번호를 입력하세요", self)
        self.inputNumL.setFont(QtGui.QFont("나눔스퀘어", 12))
        self.inputNumL.setAlignment(QtCore.Qt.AlignCenter)
        self.inputNumL.setGeometry(50, 20, 190, 41)

        self.inputPW = QLineEdit(self)
        self.inputPW.setGeometry(50, 80, 204, 41)
        self.inputPW.setPlaceholderText("P70D34")

        self.okayBtn = QPushButton("확인", self)
        self.okayBtn.setGeometry(100, 140,90,35)
        self.okayBtn.clicked.connect(self.confirm)

    # 입력한 면허번호의 유효기간이 지났는지 확인
    def is_valid(self):
        now = datetime.date.today()
        print("면허: ", self.dNum)
        sql = "select validity from drive where drivenum=%s;"
        self.cursor.execute(sql, self.dNum)
        result = self.cursor.fetchall()
        re = result[0][0]
        if now > re:
            # print("유효기간 만료")
            return False
        else:
            # print("유효기간 아직 살아있음")
            return True

    # 내가 입력한 면허번호에서 등록된 식별번호와 내가 입력한 식별번호가 같은지
    def is_same(self):
        sql = "select drivepw from drive where drivenum=%s;"
        self.cursor.execute(sql, self.dNum)
        result = self.cursor.fetchall()
        re = result[0][0]
        if re == self.inputPW.text().strip():
            # print("같습니다")
            return True
        else:
            # print("다릅니다")
            return False

    # 나의 이름, 생일 ,운전면허가 drive(면허관리디비)에 존재하는지
    def is_exist(self):
        birth_year = self.birth[0:4]
        birth_month = self.birth[4:6]
        birth_date = self.birth[6:]
        self.final_birth = birth_year + "-" + birth_month + "-" + birth_date
        sql = "select * from drive where drivenum=%s"
        self.cursor.execute(sql, self.dNum)
        result = self.cursor.fetchall()
        for re in result:
            print(re[1], re[2], re[3])

        self.userName = re[1]
        self.userBirth = re[2]
        self.userDNum = re[3]

        if self.userName == self.name and self.final_birth == str(self.userBirth) and self.userDNum == self.dNum:
            # print("확인 완료")
            return True
        else:
            # print("확인 불가")
            return False

    def confirm(self):
        # 입력한 drivenum과 식별번호가 같은가?
        self.same_answer = self.is_same()

        # 유효기간이 지났나?
        self.valid_answer = self.is_valid()

        # drivenum이 같은 사람이 존재하는가?
        self.exist_answer = self.is_exist()

        #식별번호를 입력하지 않았을 경우
        if self.inputPW.text() == "":
            self.rw=resultWindow(self)
            self.rw.resultLabel.setText("식별번호를 입력해주세요")
            self.rw.show()
        else:
            # 셋 다 true여야만 인증 가능
            if self.same_answer == True and self.valid_answer == True and self.exist_answer == True:
                print("인증 성공")
                self.rw = resultWindow(self)
                self.rw.resultLabel.setText("인증에 성공하였습니다!")
                self.rw.show()
                self.close()

            elif self.same_answer == False:
                self.rw = resultWindow(self)
                self.rw.resultLabel.setText("식별번호가 다릅니다.")
                self.rw.show()

            elif self.valid_answer == False:
                self.rw = resultWindow(self)
                self.rw.resultLabel.setText("유효기간이 지났습니다.")
                self.rw.show()

            elif self.exist_answer == False:
                print("인증 불가")
                self.rw = resultWindow(self)
                self.rw.resultLabel.setText("정보가 존재하지 않습니다.")
                self.rw.show()

