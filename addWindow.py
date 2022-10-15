
from calendar import month
import sys
from unicodedata import name
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QPixmap
from mydb import *
import datetime


class AddWindow(QWidget):
    def __init__(self,uName,mydb,mycursor,userId):
        super().__init__()
        self.mydb = mydb
        self.mycursor = mycursor
        self.userId = userId
        self.uName=uName
        self.setGeometry(450, 150, 400, 600)
        self.setFixedSize(400,600)
        self.setWindowTitle("Add Tracker")
        self.ui()
        self.show()
    def ui(self):
        self.mainDesign()
        self.ui()

    def mainDesign(self):
        self.setStyleSheet("background-color:rgb(18, 52, 121);color: white; font-family;font-size:12pt")
        self.titelLabel = QLabel("Add Tracker")
        self.projectNameLabel = QLabel("Project Name")
        self.titelLabel.setStyleSheet("font-size:15pt")
        self.titelLabel.setContentsMargins(135, 1, 100, 10)
        self.projectNameLineE = QLineEdit()
        self.startTimeLabel = QLabel("Start Time")
        self.startTimeLineE = QLineEdit()
        self.startTimeLineE.setPlaceholderText("eg: 08:00")
        self.endTImeLabel = QLabel("End Time")
        self.endTImeLineE = QLineEdit()
        self.endTImeLineE.setPlaceholderText("eg: 16:30")
        self.pauseLabel = QLabel("Pause Time")
        self.pauseLineE = QLineEdit()
        self.pauseLineE.setPlaceholderText("eg: 30")
        self.monthLabel = QLabel("Month")
        self.monthLineE = QLineEdit()
        self.monthLineE.setPlaceholderText("to select the actual month, you do not need to specify otherwise e.g. January, February ")
        self.btnConfirm = QPushButton("Confirm")
        self.btnConfirm.clicked.connect(self.confirm)



    def ui(self):
        self.mainDesign()
        self.layouts()

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.meduimLayout = QFormLayout()
        self.bottomLayout = QHBoxLayout()
        ###
        self.topLayout.addWidget(self.titelLabel)
        self.bottomLayout.addWidget(self.btnConfirm)
        self.meduimLayout.addRow(self.projectNameLabel,self.projectNameLineE)
        self.meduimLayout.addRow(self.startTimeLabel, self.startTimeLineE)
        self.meduimLayout.addRow(self.endTImeLabel, self.endTImeLineE)
        self.meduimLayout.addRow(self.pauseLabel, self.pauseLineE)
        self.meduimLayout.addRow(self.monthLabel,self.monthLineE)

        ##
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.meduimLayout)
        self.mainLayout.addLayout(self.bottomLayout)
        self.setLayout(self.mainLayout)

    def confirm(self):
        project_Name, start_Time, end_Time, pause,month =self.getParam()
        query=("INSERT INTO projets" "(projectName,startTime,endTime,personiD,projets.month)"
        "VALUES (%s,%s,%s,%s,%s)")
        data_projet = (project_Name, start_Time, end_Time,self.userId,month)
        self.mycursor.execute(query,data_projet)
        self.mydb.commit()
        self.close()

    def getParam(self):
        dt = datetime.datetime.today()
        
        months =['January', 'February', 'March', 'April', 'May', 'June', 'July','August', 'September', 'October', 'November', 'December']
        temp_month=None
        temp_month = self.monthLineE.text()
        if temp_month.capitalize() in months:
            temp_month=temp_month.capitalize()
        else:
            temp_month=months[dt.month-1]
        
       
            
        return self.projectNameLineE.text(), self.startTimeLineE.text(), self.endTImeLineE.text(), self.pauseLineE.text(),temp_month