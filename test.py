import sys
import os
import time
import urllib
from functions import *
from PyQt5.QtWidgets import (QLineEdit, QSlider, QPushButton, QListWidget, QGridLayout, QVBoxLayout, QApplication, QWidget, QMainWindow, QLabel)
from PyQt5.QtCore import (Qt, QRect)
from PyQt5.QtGui import (QIcon, QPixmap)

class loginWindow(QWidget):

    def __init__(self):
        super(loginWindow, self).__init__()
        self.setWindowTitle('Spotify - Login')
        self.setFixedSize(300, 300)
        self.init_ui()

    def init_ui(self):

        if (os.path.isfile(os.path.join('data', "code.txt"))):
            self.imageurl = prevLogin()[1]

            self.data = urllib.request.urlopen(self.imageurl).read()
            self.label = QLabel(self)
            self.label.resize(200,200)
            self.pixmap = QPixmap()
            self.pixmap.loadFromData(self.data, 'JPG')
            self.pixmap_resized = self.pixmap.scaled(140, 140)
            self.label.setPixmap(self.pixmap_resized)
            self.label.move(80, 20)


            self.name = QLabel("Last Login: {0}".format(prevLogin()[0]), self)
            self.name.setMinimumSize(150, 15)
            self.name.move(15, 10)
            self.notYou = QLabel('(Not You?)', self)
            self.notYou.move(15, 25)

            self.notYou.mousePressEvent = self.clearData
        
        self.btnLogin = QPushButton('Login', self)
        self.btnLogin.resize(100, 30)
        self.btnLogin.move(100, 210)
        self.btnLogin.clicked.connect(self.click_btn)

        
        self.btnLoginG = QPushButton('Guest', self)
        self.btnLoginG.resize(100, 30)
        self.btnLoginG.move(100, 250)
        self.btnLoginG.clicked.connect(self.checkPrevLogin)

        box = QVBoxLayout()
        self.setLayout(box)
        
        self.show()
        
    def click_btn(self):
        sender = self.sender()
        if(sender.text() == 'Login'):
            login()
            self.hide()
            homeWin.show()

    def checkPrevLogin(self):
        userName = prevLogin()[0]
        userPic = prevLogin()[1]
        print(userName)

    def clearData(self, event):
        deleteData()

class homeWindow(QMainWindow):

    def __init__(self):
        super(homeWindow, self).__init__()

        self.init_ui()

    def init_ui(self):
        self.centralwidget = QWidget()
        self.centralwidget.setObjectName("centralwidget")

        self.setWindowTitle('Spotify - Home')
        self.setFixedSize(800,400)

        self.search = QLineEdit('Search...', self)
        self.search.move(50, 200)
        self.search.returnPressed.connect(self.getSearchParms)

        self.searchBtn = QPushButton('', self)
        self.searchBtn.move(50, 250)
        self.searchBtn.clicked.connect(self.getSearchParms)

        self.resultList = QListWidget(self)
        self.resultList.resize(400, 250)
        self.resultList.move(300, 100)

    def getSearchParms(self):
        self.searchText = self.search.text()

        results = search('track', self.searchText)

        for result in results:
            self.item = result
            self.resultList.addItem(self.item)

def run():
    app = QApplication(sys.argv)

    #set Main window to global variable, otherwise won't stay alive
    global homeWin
    homeWin = homeWindow()
    
    loginWin = loginWindow()
    loginWin.show  
    sys.exit(app.exec_())

run()
