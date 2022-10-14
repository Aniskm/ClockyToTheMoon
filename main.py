import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QPixmap
import mysql.connector



mydb = mysql.connector.connect(
host="localhost",
user="root",
password="",
database="anis")
mycursor = mydb.cursor()
    


class Window(QWidget):
    def __init__(self):
        super().__init__()
        
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
        self.getUsers()
        self.windowForWork()

    def windowForWork(self):
        self.secondWindow = WindowForWork(self.uName)
        self.close()


    def getUsers(self):
        global mycursor,mydb
        query = "SELECT name FROM persons"
        mycursor.execute(query)
        users_list = mycursor.fetchall()

       
      
        users_list =[users_list[i][0] for i in range (len (users_list)-1) ]
        if self.uName in users_list:
            print("Willkommen {} ".format(self.uName))
        else:
            print("call add user")
            self.addUsers()

    def addUsers(self):
        global mycursor,mydb
        
        myname = (self.uName,)
        
        query = ("INSERT INTO persons (persons.name) VALUES (%s)")
        mycursor.execute(query,myname)
            
        mydb.commit()
       


class WindowForWork(QWidget):
    def __init__(self,uName):
        super().__init__()
        self.uName = uName
        self.setGeometry(100, 100, 950, 700)
        self.setWindowTitle("Project Management")
        self.ui()
        self.show()

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
        self.nameLabel = QLabel()
        self.projectNameLabel = QLabel("Project")
        self.monthNameLabel = QLabel("Month")
        self.projectComboBoxe= QComboBox()
        self.monthComboBoxe = QComboBox()
        self.months_list()
        self.projectListUpdate()
        self.btnNew.clicked.connect(self.addTracker)
        self.btnUpdate.clicked.connect(self.update)

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
        self.leftayout.addRow("",self.nameLabel)
        self.leftayout.addRow(self.projectNameLabel,self.projectComboBoxe)
        self.leftayout.addRow(self.monthNameLabel,self.monthComboBoxe)
        self.setLayout(self.mainLayout)

    def months_list(self):
        months =['Alle','January', 'February', 'March', 'April', 'May', 'June', 'July','August', 'September', 'October', 'November', 'December']
        for month in months:
            self.monthComboBoxe.addItem(month)
    def projectListUpdate(self):
        global mydb,mycursor
        query = "SELECT projectName FROM projets"
        mycursor.execute(query)
        projet_list = mycursor.fetchall()   
        projet_list =[projet_list[i][0] for i in range (len (projet_list)-1) ]
        projet_list=set(projet_list)
        self.projectComboBoxe.clear()
        for projet in projet_list:
            
            self.projectComboBoxe.addItem(projet)
            
    def addTracker(self):
        self.thirdWindow = AddWindow(self.uName)
    
    def update(self):
        self.projectListUpdate()
        # Noch nicht fertig 


class AddWindow(QWidget):
    def __init__(self,uName):
        super().__init__()
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
        project_Name, start_Time, end_Time, pause =self.getParam()
        query=("INSERT INTO projets" "(projectName,startTime,endTime,personiD)"
        "VALUES (%s,%s,%s,%s)")
        
        id_of_person = id_list[0]
        print(id_of_person)
        data_projet = (project_Name, start_Time, end_Time,id_of_person)
        mycursor.execute(query,data_projet)
        mydb.commit()
        self.close()

    def getParam(self):

        print(self.projectNameLineE.text())
        return self.projectNameLineE.text(), self.startTimeLineE.text(), self.endTImeLineE.text(), self.pauseLineE.text()

def main():
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())


if __name__ == "__main__":
    main()
