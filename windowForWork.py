from calendar import month
import sys
from unicodedata import name
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QPixmap
from mydb import *

from addWindow import AddWindow
import datetime


class WindowForWork(QWidget):
    def __init__(self,uName,mydb,mycursor,userId):
        super().__init__()
        self.uName = uName
        self.mydb = mydb
        self.mycursor = mycursor
        self.userId = userId
        self.SelectedProject="Alle"
        self.SelectedMonth="Alle"
        self.setGeometry(100, 100, 1200, 700)
        self.setWindowTitle("Project Management")
        self.ui()
        self.show()
        
    def ui(self):
        self.mainDesign()
        self.layouts()
    def closeEvent(self, event):
        #self.firstWindow = MainWindow(mydb,mycursor)
        print("first")
    def mainDesign(self):
        self.setStyleSheet("background-color:rgb(18, 52, 121);color: white; font-family;font-size:12pt")
        self.tableWidget = QTableWidget(32,7)
        self.tableWidget.setStyleSheet("background-color:rgb(201, 198, 220);color: black")
        self.tableWidget.setHorizontalHeaderLabels(["Project name", "Start time", "End Time", "Pause Time", "Day", "Month","Year"])
     
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.btnNew = QPushButton("New")
        self.btnUpdate = QPushButton("Update")
        self.btnDelete = QPushButton("Delete")
        self.clockimage = QLabel()
        self.clockimage.setPixmap(QPixmap("images/clocki.png"))
        self.welcomeLabel = QLabel("Welcome")
        self.welcomeNameLabel = QLabel("")
        self.projectNameLabel = QLabel("Project")
        self.monthNameLabel = QLabel("Month")
        self.projectComboBoxe= QComboBox()
        self.monthComboBoxe = QComboBox()
        self.months_list()
        self.projectListUpdate()
        self.getDataFilter()
        self.welcomeNameLabel.setText(self.uName)
        self.btnNew.clicked.connect(self.addTracker)
        self.btnUpdate.clicked.connect(self.update)
        self.projectComboBoxe.activated[str].connect(self.projectOnChange)
        self.monthComboBoxe.activated[str].connect(self.monthOnChange)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.leftayout = QFormLayout()
        self.rightMainLayout = QVBoxLayout()
        self.rightTopLayout = QHBoxLayout()
        self.rightBottomLayout = QHBoxLayout()
        ###
        self.rightMainLayout.addLayout(self.rightTopLayout)
        self.rightMainLayout.addLayout(self.rightBottomLayout)
        self.mainLayout.addLayout(self.leftayout,40)
        self.mainLayout.addLayout(self.rightMainLayout,60)
        ###
        self.rightTopLayout.addWidget(self.tableWidget)
        self.rightBottomLayout.addWidget(self.btnNew)
        self.rightBottomLayout.addWidget(self.btnUpdate)
        self.rightBottomLayout.addWidget(self.btnDelete)
        ###
        self.leftayout.addRow(" ",self.clockimage)
        self.leftayout.addRow(self.welcomeLabel,self.welcomeNameLabel)
        self.leftayout.addRow(self.projectNameLabel,self.projectComboBoxe)
        self.leftayout.addRow(self.monthNameLabel,self.monthComboBoxe)
        self.setLayout(self.mainLayout)

    def months_list(self):
        months =['Alle','January', 'February', 'March', 'April', 'May', 'June', 'July','August', 'September', 'October', 'November', 'December']
        for month in months:
            self.monthComboBoxe.addItem(month)
    def projectListUpdate(self):    
        userId = (self.userId,)
        query = "SELECT projectName FROM projets WHERE personID = (%s) "
        self.mycursor.execute(query,userId)
        projet_list = self.mycursor.fetchall()   
        projet_list =[projet_list[i][0] for i in range (len (projet_list)) ]
        projet_list.insert(0,"Alle")
        projet_list=set(projet_list)
        self.projectComboBoxe.clear()
        for projet in projet_list:
            
            self.projectComboBoxe.addItem(projet)
            
    def addTracker(self):
        self.thirdWindow = AddWindow(self.uName,self.mydb,self.mycursor,self.userId)
    
    def update(self):
        self.projectListUpdate()
        # Noch nicht fertig 

    def projectOnChange(self,text):
        self.SelectedProject = text
        self.getDataFilter()
    def monthOnChange(self,text):
        self.SelectedMonth = text
        self.getDataFilter()
    
    def getDataFilter(self):
        query=None
        myparam = None
        if self.SelectedProject == "Alle" and self.SelectedMonth =="Alle":
            query = "SELECT projectName,startTime,endTime,pauseTime,projets.day,projets.month,projets.year FROM projets WHERE personID =%s"
            myparam=(self.userId,)
        elif  self.SelectedProject == "Alle" and self.SelectedMonth !="Alle": 
            query = "SELECT  projectName,startTime,endTime,pauseTime,projets.day,projets.month,projets.year FROM projets WHERE projets.month =%s and personID =%s"
            myparam=(self.SelectedMonth,self.userId)
        elif  self.SelectedProject != "Alle" and self.SelectedMonth =="Alle":     
            query = "SELECT  projectName,startTime,endTime,pauseTime,projets.day,projets.month,projets.year FROM projets WHERE  projectName =%s and personID =%s"
            myparam=(self.SelectedProject,self.userId)
        else:
            query = "SELECT projectName,startTime,endTime,pauseTime,projets.day,projets.month,projets.year FROM projets WHERE projectName =%s and projets.month =%s and personID =%s"
            myparam=(self.SelectedProject,self.SelectedMonth,self.userId)
        self.mycursor.execute(query,myparam)
        temp_data = self.mycursor.fetchall()
        projectNameData =[temp_data[i][0] for i in range (len (temp_data)) ]
        startTimeData =[temp_data[i][1] for i in range (len (temp_data)) ]
        endTimeData =[temp_data[i][2] for i in range (len (temp_data)) ]
        pauseTimeData =[temp_data[i][3] for i in range (len (temp_data)) ]
        dayData =[temp_data[i][4] for i in range (len (temp_data)) ]
        monthData =[temp_data[i][5] for i in range (len (temp_data)) ]
        yearData =[temp_data[i][6] for i in range (len (temp_data)) ]
        
        table_data =[projectNameData,startTimeData,endTimeData,pauseTimeData,dayData,monthData,yearData]
        self.tableWidget.clear()
        self.tableWidget.setHorizontalHeaderLabels(["Project name", "Start time", "End Time", "Pause Time", "Day", "Month","Year"])
        for i in range (len(projectNameData)):
            for j in range(7):
                self.tableWidget.setItem(i,j,QTableWidgetItem(str(table_data[j][i])))
        
     
    
        