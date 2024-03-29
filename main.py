from calendar import month
import sys
from unicodedata import name
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QPixmap
from mydb import *
from mainWindow import MainWindow

import datetime




       


class WindowForWork(QWidget):
    def __init__(self,uName):
        super().__init__()
        self.uName = uName
        self.setGeometry(100, 100, 950, 700)
        self.setWindowTitle("Project Management")
        self.ui()
        self.show()
        self.id_of_person = None
    def ui(self):
        self.mainDesign()
        self.layouts()
    def closeEvent(self, event):
        self.firstWindow = Window(self.uName)
    def mainDesign(self):
        self.setStyleSheet("background-color:rgb(18, 52, 121);color: white; font-family;font-size:12pt")
        self.tableWidget = QTableWidget(32,5)
        self.tableWidget.setStyleSheet("background-color:rgb(201, 198, 220);color: black")
        self.tableWidget.setHorizontalHeaderItem(0,QTableWidgetItem("Project name"))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("Start time"))
        self.tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem("End Time"))
        self.tableWidget.setHorizontalHeaderItem(3, QTableWidgetItem("Pause time"))
        self.tableWidget.setHorizontalHeaderItem(4, QTableWidgetItem("Total Time"))
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
        global mydb,mycursor
       
        query ="SELECT id FROM persons WHERE persons.name =%s"
        mycursor.execute(query,(self.uName,))
        id_list = mycursor.fetchone()
        self.id_of_person = id_list[0]
        myid = (self.id_of_person,)
        query = "SELECT projectName FROM projets WHERE personID = (%s) "
        mycursor.execute(query,myid)
        projet_list = mycursor.fetchall()   
        projet_list =[projet_list[i][0] for i in range (len (projet_list)) ]
        projet_list.insert(0,"Alle")
        projet_list=set(projet_list)
        self.projectComboBoxe.clear()
        for projet in projet_list:
            
            self.projectComboBoxe.addItem(projet)
            
    def addTracker(self):
        self.thirdWindow = AddWindow(self.uName)
    
    def update(self):
        self.projectListUpdate()
        # Noch nicht fertig 

    def projectOnChange(self,text):
        query ="SELECT id FROM persons WHERE persons.name =%s"
        mycursor.execute(query,(self.uName,))
        id_list = mycursor.fetchone()
        self.id_of_person = id_list[0]
        query=None
        if text == "Alle":
            query = "SELECT projectName,startTime,endTime,projets.dateTime,projets.month FROM projets WHERE personID =%s"
            mycursor.execute(query,(self.id_of_person,))
            print("my id {}".format(self.id_of_person))
        else:
            query = "SELECT projectName,startTime,endTime,projets.dateTime,projets.month FROM projets WHERE projectName =%s and personID =%s"
            mycursor.execute(query,(text,self.id_of_person))
        
        temp_data = mycursor.fetchall()
        projectNameData =[temp_data[i][0] for i in range (len (temp_data)) ]
        startTimeData =[temp_data[i][1] for i in range (len (temp_data)) ]
        endTimeData =[temp_data[i][2] for i in range (len (temp_data)) ]
        dateTimeData =[temp_data[i][3] for i in range (len (temp_data)) ]
        monthData =[temp_data[i][4] for i in range (len (temp_data)) ]
        print(projectNameData)
        print( monthData)
    def monthOnChange(self,text):
        query ="SELECT id FROM persons WHERE persons.name =%s"
        mycursor.execute(query,(self.uName,))
        id_list = mycursor.fetchone()
        self.id_of_person = id_list[0]
        query=None
        if text == "Alle":
            query = "SELECT projectName,startTime,endTime,projets.dateTime,projets.month FROM projets WHERE personID =%s"
            mycursor.execute(query,(self.id_of_person,))
        else:
            query = "SELECT projectName,startTime,endTime,projets.dateTime,projets.month FROM projets WHERE projets.month =%s and personID =%s"
            mycursor.execute(query,(text,self.id_of_person))
        
        temp_data = mycursor.fetchall()
        projectNameData =[temp_data[i][0] for i in range (len (temp_data)) ]
        startTimeData =[temp_data[i][1] for i in range (len (temp_data)) ]
        endTimeData =[temp_data[i][2] for i in range (len (temp_data)) ]
        dateTimeData =[temp_data[i][3] for i in range (len (temp_data)) ]
        monthData =[temp_data[i][4] for i in range (len (temp_data)) ]
        print(projectNameData)
        print(monthData)
        
        
class AddWindow(QWidget):
    def __init__(self,uName):
        super().__init__()
        self.id_of_person=None
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
        global mydb,mycursor
        query ="SELECT id FROM persons WHERE persons.name =%s"
        mycursor.execute(query,(self.uName,))
        id_list = mycursor.fetchone()
        project_Name, start_Time, end_Time, pause,month =self.getParam()
        query=("INSERT INTO projets" "(projectName,startTime,endTime,personiD,projets.month)"
        "VALUES (%s,%s,%s,%s,%s)")
        
        self.id_of_person = id_list[0]
        print(self.id_of_person)
        data_projet = (project_Name, start_Time, end_Time,self.id_of_person,month)
        mycursor.execute(query,data_projet)
        mydb.commit()
        self.close()

    def getParam(self):
        dt = datetime.datetime.today()
        current_month = dt.month
        months =['January', 'February', 'March', 'April', 'May', 'June', 'July','August', 'September', 'October', 'November', 'December']
        temp_month=None
        temp_month = self.monthLineE.text()
        if temp_month.capitalize() in months:
            temp_month=temp_month.capitalize()
        else:
            temp_month=months[dt.month-1]
        
       
            
        return self.projectNameLineE.text(), self.startTimeLineE.text(), self.endTImeLineE.text(), self.pauseLineE.text(),temp_month

def main():
    mydb,mycursor = connect_to_my_db()
    App = QApplication(sys.argv)
    window = MainWindow(mydb,mycursor)
    sys.exit(App.exec_())


if __name__ == "__main__":
    main()
