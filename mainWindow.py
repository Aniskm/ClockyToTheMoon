from calendar import month
import sys
from unicodedata import name
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QPixmap
from mydb import *
from windowForWork import WindowForWork
import datetime


class MainWindow(QWidget):
    def __init__(self,mydb,mycursor):
        super().__init__()
        self.mydb = mydb
        self.mycursor = mycursor
        self.UserId = None
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Timer To The Moon")
        self.UI()
        self.show()

    
         
    def UI(self):
        self.mainDesign()
        self.layouts()

    def mainDesign(self):
        self.setStyleSheet("background-color:rgb(18, 52, 121);color: white; font-family;font-size:12pt")
        self.title_for_main = QLabel("Clocky To The Moon")
        self.title_for_main.setStyleSheet("font-size:30pt")
        self.lineEdit_for_name = QLineEdit()
        self.lineEdit_for_name.setPlaceholderText(" Please Enter your Name")
        self.lineEdit_for_name.setStyleSheet("font-size:20pt")
        self.clockLabel = QLabel()
        self.clockLabel.setStyleSheet("font-size:30pt")
        self.logoLabel = QLabel()
        self.logoLabel.setPixmap(QPixmap("images/roc_klein.gif"))
        #
        self.title_for_main.setAlignment(Qt.AlignCenter)

        self.logoLabel.setAlignment(Qt.AlignBottom)
        self.clockLabel.setAlignment(Qt.AlignCenter)

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == 16777220 and self.lineEdit_for_name.text():
            self.accountCheck()

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.centerLayout = QHBoxLayout()
        self.buttomLayout = QHBoxLayout()
        self.logoLayout = QHBoxLayout()

        ##

        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.centerLayout)
        self.mainLayout.addLayout(self.buttomLayout)
        self.mainLayout.addLayout(self.logoLayout)

        self.setLayout(self.mainLayout)
        #######
        self.topLayout.addWidget((self.title_for_main))
        self.centerLayout.addWidget((self.lineEdit_for_name))
        self.buttomLayout.addWidget(self.clockLabel)
        self.logoLayout.addWidget(self.logoLabel)
        self.centerLayout.setContentsMargins(200, 20, 200, 30)
        timer = QTimer(self)
        timer.timeout.connect(self.myClock)
        timer.start(1000)

    def myClock(self):
        current_time = QTime.currentTime()

        label_time = current_time.toString('hh:mm:ss')

        self.clockLabel.setText(label_time)

    def accountCheck(self):
        ## check not finisched
        self.uName = self.lineEdit_for_name.text()
        self.UserId = self.getUsersId()
        if self.UserId==None:
            self.addUsers
        self.windowForWork()

    def windowForWork(self):
        self.secondWindow = WindowForWork(self.uName,self.mydb,self.mycursor,self.UserId)
        self.close()


    def getUsersId(self):
        
        query = "SELECT COUNT(*),id FROM persons WHERE name in (%s)"
        self.mycursor.execute(query,(self.uName,))
       
        data_list = self.mycursor.fetchall()
 
        if data_list[0][0]>0:
            return data_list[0][1]
        else:
            return None
       
      
        

    def addUsers(self):
        print("ADD USER")
        myname = (self.uName,)
        
        query = ("INSERT INTO persons (persons.name) VALUES (%s)")  
        self.mycursor.execute(query,myname)
            
        self.mydb.commit()