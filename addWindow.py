
from calendar import month
from unicodedata import name
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
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
        self.dayLabel = QLabel("Day")
        self.dayLineE= QLineEdit()
        self.dayLineE.setPlaceholderText("to select the actual day, you do not need to specify otherwise e.g.")
        self.yearLabel = QLabel("Year")
        self.yearLineE= QLineEdit()
        self.yearLineE.setPlaceholderText("to select the actual year, you do not need to specify otherwise e.g.")
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
        self.meduimLayout.addRow(self.dayLabel,self.dayLineE)
        self.meduimLayout.addRow(self.yearLabel,self.yearLineE)
        ##
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.meduimLayout)
        self.mainLayout.addLayout(self.bottomLayout)
        self.setLayout(self.mainLayout)

    def confirm(self):
        project_Name, start_Time, end_Time, pause,month,day,year =self.getParam()
        query=("INSERT INTO projets" "(projectName,startTime,endTime,pauseTime,day,month,year,personID)"
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)")
        data_projet = (project_Name, start_Time, end_Time,pause,day,month,year,self.userId)
        self.mycursor.execute(query,data_projet)
        self.mydb.commit()
        self.close()
        print("confirm moth {}".format(month))

    def getParam(self):
        dt = datetime.datetime.today()
        
        months =['January', 'February', 'March', 'April', 'May', 'June', 'July','August', 'September', 'October', 'November', 'December']
        temp_month = self.monthLineE.text().capitalize() if self.monthLineE.text().capitalize() in months else  months[dt.month-1]
        temp_day = self.dayLineE.text() if self.dayLineE.text() else dt.day
        temp_year = self.yearLineE.text() if self.yearLineE.text() else dt.year
        print("temp month {}".format(temp_month))
      
            
        return self.projectNameLineE.text(), self.startTimeLineE.text(), self.endTImeLineE.text(), self.pauseLineE.text(),temp_month,temp_day,temp_year