# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_wip.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from functions import *
from youtube import *
from player import *
import urllib
import sys
import os
import threading
from PyQt5.QtWidgets import (QStackedWidget, QLineEdit, QListView, QPushButton, QProgressBar,
                             QListWidget, QScrollBar, QTextEdit, QMenuBar, QWidget, QLCDNumber,
                             QStatusBar, QLabel, QApplication, QMainWindow, QRadioButton, QFrame,
                             QVBoxLayout, QButtonGroup, QHBoxLayout, QSizePolicy, QGridLayout, QLayout)
from PyQt5.QtCore import (Qt, QRect, QCoreApplication, QMetaObject, QSize)
from PyQt5.QtMultimedia import (QMediaPlayer, QMediaContent)
from PyQt5.QtGui import (QIcon, QPixmap, QFont)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QRect(-1, 69, 971, 511))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.gridLayoutCenter = QGridLayout(self.horizontalLayoutWidget)
        self.gridLayoutCenter.setSizeConstraint(QLayout.SetMinimumSize)
        self.gridLayoutCenter.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutCenter.setObjectName("gridLayoutCenter")
        self.stackedWidget = QStackedWidget(self.horizontalLayoutWidget)
        self.stackedWidget.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setMinimumSize( QSize(600, 0))
        self.stackedWidget.setObjectName("stackedWidget")

        #audio player
        self.player = QMediaPlayer()

        #login page
        self.loginPage = QWidget()
        self.loginPage.setObjectName("loginPage")
        self.loginBtn = QPushButton(self.loginPage)
        self.loginBtn.setGeometry(QRect(140, 350, 121, 41))
        self.loginBtn.setObjectName("loginBtn")
        self.loginBtn.clicked.connect(self.loginFunc)

        #get previous users data

        self.continueBtn = QPushButton(self.loginPage)
        self.continueBtn.setGeometry(QRect(140, 400, 121, 41))
        self.continueBtn.setObjectName("continueBtn")
        self.continueBtn.clicked.connect(self.loginFunc)
        self.continueBtn.hide()

        if (os.path.isfile(os.path.join('data', "code.txt"))):
            self.imageurl = prevLogin()[1]
            self.data = urllib.request.urlopen(self.imageurl).read()
            self.lastUserPic = QLabel(self.loginPage)
            self.lastUserPic.resize(200,200)
            self.pixmap = QPixmap()
            self.pixmap.loadFromData(self.data, 'JPG')
            self.pixmap_resized = self.pixmap.scaled(140, 140)
            self.lastUserPic.setPixmap(self.pixmap_resized)
            self.lastUserPic.setGeometry(QRect(130, 170, 140, 140))
            self.name = QLabel("Last Login: {0}".format(prevLogin()[0]), self.loginPage)
            self.name.setMinimumSize(150, 15)
            self.name.move(130, 310)
            self.notYou = QLabel('(Not You?)', self.loginPage)
            self.notYou.move(130, 325)
            self.notYou.mousePressEvent = self.clearData
            self.continueBtn.show()

        #logo
        self.logo = QLabel(self.loginPage)
        self.logo.resize(300, 100)
        self.pixmapLogo = QPixmap()
        self.pixmapLogo.load(r'images\logo', 'PNG')
        self.pixmapLogo_resized = self.pixmapLogo.scaled(300, 200)
        self.logo.setPixmap(self.pixmapLogo_resized)
        self.logo.setGeometry(QRect(50, 0, 300, 200))


        self.stackedWidget.addWidget(self.loginPage)

        #main page
        self.mainPage = QWidget()
        self.mainPage.setObjectName("mainPage")
        self.stackedWidget.addWidget(self.mainPage)

        #result page
        self.resultPage = QWidget()
        self.resultPage.setObjectName("resultPage")
        self.labelSearch = QLabel(self.resultPage)
        self.labelSearch.setGeometry(QRect(350, 10, 241, 41))
        font = QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.labelSearch.setFont(font)
        self.labelSearch.setAlignment(Qt.AlignCenter)
        self.labelSearch.setObjectName("labelSearch")

        self.resultList = QListWidget(self.resultPage)
        self.resultList.setGeometry(QRect(80, 70, 391, 401))
        self.resultList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.resultList.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.resultList.setObjectName("resultList")
        self.resultList.itemClicked.connect(self.resultClick)
        self.resultList.itemDoubleClicked.connect(self.resultDoubleClick)

        self.songArtwork = QLabel(self.resultPage)
        self.songArtwork.setObjectName("songArtwork")
        self.artistLabel = QLabel(self.resultPage)
        self.artistLabel.setGeometry(QRect(580, 400, 221, 31))
        self.artistLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.artistLabel.setObjectName("artistLabel")
        self.songTitleLabel = QLabel(self.resultPage)
        self.songTitleLabel.setGeometry(QRect(580, 415, 221, 31))
        self.songTitleLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.songTitleLabel.setObjectName("songTitleLabel")
        self.popLabel = QLabel(self.resultPage)
        self.popLabel.setGeometry(QRect(580, 430, 80, 31))
        self.popLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.popLabel.setObjectName("popLabel")
        self.stackedWidget.addWidget(self.resultPage)

        #artist page
        self.artistPage = QWidget()
        self.artistPage.setObjectName("artistPage")
        self.stackedWidget.addWidget(self.artistPage)

        #album page
        self.albumPage = QWidget()
        self.albumPage.setObjectName("albumPage")
        self.stackedWidget.addWidget(self.albumPage)

        #playlist page
        self.playlistPage = QWidget()
        self.playlistPage.setObjectName("playlistPage")
        self.stackedWidget.addWidget(self.playlistPage)

        #settings page
        self.settingsPage = QWidget()
        self.settingsPage.setObjectName("settingsPage")
        self.stackedWidget.addWidget(self.settingsPage)
        self.gridLayoutCenter.addWidget(self.stackedWidget, 0, 0, 1, 1)

        #music player
        self.frameAlbumArt = QFrame(self.centralwidget)
        self.frameAlbumArt.setGeometry(QRect(40, 590, 100, 70))
        self.frameAlbumArt.setFrameShape(QFrame.StyledPanel)
        self.frameAlbumArt.setFrameShadow(QFrame.Raised)
        self.frameAlbumArt.setObjectName("frameAlbumArt")
        self.frameControls = QFrame(self.centralwidget)
        self.frameControls.setGeometry(QRect(400, 590, 381, 41))
        self.frameControls.setFrameShape(QFrame.StyledPanel)
        self.frameControls.setFrameShadow(QFrame.Raised)
        self.frameControls.setObjectName("frameControls")
        self.labelSongTitle_2 = QLabel(self.centralwidget)
        self.labelSongTitle_2.setGeometry(QRect(150, 610, 81, 21))
        self.labelSongTitle_2.setObjectName("labelSongTitle_2")
        self.labelSongTitle = QLabel(self.centralwidget)
        self.labelSongTitle.setGeometry(QRect(150, 630, 81, 21))
        self.labelSongTitle.setObjectName("labelSongTitle")
        self.labelNowPlaying = QLabel(self.centralwidget)
        self.labelNowPlaying.setGeometry(QRect(150, 590, 121, 21))
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelNowPlaying.setFont(font)
        self.labelNowPlaying.setObjectName("labelNowPlaying")
        self.lcdNumber = QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QRect(750, 640, 31, 16))
        self.lcdNumber.setProperty("value", 2.0)
        self.lcdNumber.setObjectName("lcdNumber")
        self.progressMusic = QProgressBar(self.centralwidget)
        self.progressMusic.setGeometry(QRect(400, 640, 341, 16))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressMusic.sizePolicy().hasHeightForWidth())
        self.progressMusic.setSizePolicy(sizePolicy)
        self.progressMusic.setProperty("value", 24)
        self.progressMusic.setTextVisible(False)
        self.progressMusic.setObjectName("progressMusic")

        #search
        self.searchBox = QLineEdit(self.centralwidget)
        self.searchBox.setGeometry(QRect(44, 31, 501, 20))
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchBox.sizePolicy().hasHeightForWidth())
        self.searchBox.setSizePolicy(sizePolicy)
        self.searchBox.setMinimumSize(QSize(400, 10))
        self.searchBox.setMaximumSize(QSize(1000, 16777215))
        self.searchBox.setLayoutDirection(Qt.LeftToRight)
        self.searchBox.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.searchBox.setObjectName("searchBox")
        self.searchBox.returnPressed.connect(self.getSearchParms)

        self.searchBtn = QPushButton(self.centralwidget)
        self.searchBtn.setGeometry(QRect(550, 30, 75, 23))
        self.searchBtn.setObjectName("searchBtn")
        self.searchBtn.clicked.connect(self.getSearchParms)

        #user info
        self.userPicSmall = QLabel(self.centralwidget)
        self.userPicSmall.resize(300, 100)
        self.userPicSmall.setGeometry(QRect(1110, 10, 71, 51))
        self.userPicSmall.setObjectName("userPicSmall")
        self.labelUserName = QLabel(self.centralwidget)
        self.labelUserName.setGeometry(QRect(1000, 10, 141, 20))
        self.labelUserName.setObjectName("labelUserName")
        self.labelSubType = QLabel(self.centralwidget)
        self.labelSubType.setGeometry(QRect(1000, 30, 141, 20))
        self.labelSubType.setObjectName("labelSubType")

        #search options
        self.searchOp1 = QRadioButton(self.centralwidget)
        self.searchOp1.setGeometry( QRect(660, 30, 70, 17))
        self.searchOp1.setChecked(True)
        self.searchOp1.setObjectName("radioButton")
        self.searchOp2 = QRadioButton(self.centralwidget)
        self.searchOp2.setGeometry( QRect(720, 30, 70, 17))
        self.searchOp2.setObjectName("radioButton_2")
        self.searchOp3 = QRadioButton(self.centralwidget)
        self.searchOp3.setGeometry( QRect(780, 30, 70, 17))
        self.searchOp3.setObjectName("radioButton_3")
        self.searchOp4 = QRadioButton(self.centralwidget)
        self.searchOp4.setGeometry( QRect(840, 30, 70, 17))
        self.searchOp4.setObjectName("radioButton_4")
        self.searchOps = [self.searchOp1, self.searchOp2, self.searchOp3, self.searchOp4]

        #playlists
        self.label =QLabel(self.centralwidget)
        self.label.setGeometry( QRect(990, 70, 191, 21))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setLayoutDirection( Qt.LeftToRight)
        self.label.setTextFormat( Qt.AutoText)
        self.label.setAlignment( Qt.AlignCenter)
        self.label.setIndent(0)
        self.label.setObjectName("label")
        self.listViewPlaylists =QListView(self.centralwidget)
        self.listViewPlaylists.setGeometry( QRect(980, 100, 211, 481))
        sizePolicy =QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listViewPlaylists.sizePolicy().hasHeightForWidth())
        self.listViewPlaylists.setSizePolicy(sizePolicy)
        self.listViewPlaylists.setAcceptDrops(False)
        self.listViewPlaylists.setAutoFillBackground(False)
        self.listViewPlaylists.setVerticalScrollBarPolicy( Qt.ScrollBarAlwaysOff)
        self.listViewPlaylists.setHorizontalScrollBarPolicy( Qt.ScrollBarAsNeeded)
        self.listViewPlaylists.setAlternatingRowColors(True)
        self.listViewPlaylists.setObjectName("listViewPlaylists")
        self.horizontalLayoutWidget.raise_()
        self.frameAlbumArt.raise_()
        self.frameControls.raise_()
        self.labelSongTitle_2.raise_()
        self.labelSongTitle.raise_()
        self.labelNowPlaying.raise_()
        self.lcdNumber.raise_()
        self.progressMusic.raise_()
        self.searchBox.raise_()
        self.searchBtn.raise_()
        self.userPicSmall.raise_()
        self.labelUserName.raise_()
        self.labelSubType.raise_()
        self.searchOp1.raise_()
        self.searchOp2.raise_()
        self.searchOp3.raise_()
        self.searchOp4.raise_()
        self.label.raise_()
        self.listViewPlaylists.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry( QRect(0, 0, 1264, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(MainWindow)

        #hiding stuff if on login page
        if self.stackedWidget.currentIndex() == 0:

            MainWindow.setFixedSize(400, 600)
            MainWindow.setWindowTitle("Youtifpy - Login")

            self.searchBox.hide()
            self.searchBtn.hide()
            self.searchOp1.hide()
            self.searchOp2.hide()
            self.searchOp3.hide()
            self.searchOp4.hide()
            self.frameAlbumArt.hide()
            self.frameControls.hide()
            self.labelSongTitle_2.hide()
            self.labelSongTitle.hide()
            self.labelNowPlaying.hide()
            self.lcdNumber.hide()
            self.progressMusic.hide()
            self.label.hide()
            self.listViewPlaylists.hide()
            self.labelUserName.hide()
            self.labelSubType.hide()
            self.frameAlbumArt.hide()
            self.frameControls.hide()
            self.songArtwork.hide()
            self.artistLabel.hide()
            self.songTitleLabel.hide()
            self.popLabel.hide()

    def loginFunc(self):
        sender = self.MainWindow.sender()
        if(sender.text() == 'Login'):
            login()

        #go to main page
        self.stackedWidget.setCurrentIndex(1)
        MainWindow.setFixedSize(1200, 700)
        MainWindow.setWindowTitle("Youtifpy - Home")

        #show all hidden elements
        self.searchBox.show()
        self.searchBtn.show()
        self.searchOp1.show()
        self.searchOp2.show()
        self.searchOp3.show()
        self.searchOp4.show()
        self.frameAlbumArt.show()
        self.frameControls.show()
        self.labelSongTitle_2.show()
        self.labelSongTitle.show()
        self.labelNowPlaying.show()
        self.lcdNumber.show()
        self.progressMusic.show()
        self.label.show()
        self.listViewPlaylists.show()
        self.labelUserName.show()
        self.labelUserName.setText('Name: {0}'.format(prevLogin()[0]))
        self.labelSubType.show()
        self.labelSubType.setText('Subscription: {0}'.format(prevLogin()[2]))

        #get user picture
        self.imageurl = prevLogin()[1]
        self.data = urllib.request.urlopen(self.imageurl).read()
        self.userPicSmall.resize(50, 50)
        self.pixmap = QPixmap()
        self.pixmap.loadFromData(self.data, 'JPG')
        self.pixmap_resized = self.pixmap.scaled(50, 50)
        self.userPicSmall.setPixmap(self.pixmap_resized)
        self.userPicSmall.setGeometry(QRect(1120, 10, 50, 50))

        self.frameAlbumArt.show()
        self.frameControls.show()

    def clearData(self, event):
        deleteData()
        self.lastUserPic.hide()
        self.name.hide()
        self.notYou.hide()
        self.continueBtn.hide()


    def getSearchParms(self):
        self.searchText = self.searchBox.text()

        if self.searchText == '':
            return

        if self.resultList.count() > 0:
            self.resultList.clear()

        for self.searchOp in self.searchOps:
            if self.searchOp.isChecked():
                option = self.searchOp.text()
                break
        try:
            self.results = search(str(option), self.searchText, 30)

            for self.result in self.results[0]:

                self.item = self.result
                self.resultList.addItem(self.item)
                self.stackedWidget.setCurrentIndex(2)
                MainWindow.setWindowTitle("Youtifpy - Search Results")


        except requests.exceptions.ConnectionError:

            self.item = 'No Internet Connection'
            self.resultList.addItem(self.item)

    #display song info
    def resultClick(self):

        for self.searchOp in self.searchOps:
            if self.searchOp.isChecked():
                option = self.searchOp.text()
                break

        name = self.resultList.currentItem().text()

        if name == 'No Internet Connection':
            return

        id = self.resultList.currentRow()

        if option == 'artist':
           getArtist(self.results[1][id])

        elif option == 'track':
            trackInfo = getTrack(self.results[1][id])

            self.imageurl = trackInfo[2]
            self.data = urllib.request.urlopen(self.imageurl).read()
            self.songArtwork.resize(300, 300)
            self.pixmap = QPixmap()
            self.pixmap.loadFromData(self.data, 'JPG')
            self.pixmap_resized = self.pixmap.scaled(300, 300)
            self.songArtwork.setPixmap(self.pixmap_resized)
            self.songArtwork.setGeometry(QRect(580, 100, 300, 300))

            self.artistLabel.setText("Artist: {0}".format(trackInfo[1]))
            self.songTitleLabel.setText("Song: {0}".format(trackInfo[0]))
            self.popLabel.setText("Popularity: {0}".format(trackInfo[3]))

            self.songArtwork.show()
            self.artistLabel.show()
            self.songTitleLabel.show()
            self.popLabel.show()

        elif option == 'album':
            getAlbum(self.results[1][id])

        else:
            getPlaylist(id)

    #play song
    def resultDoubleClick(self):
        name = self.resultList.currentItem().text()
        if name == 'No Internet Connection':
            return

        videoId = youtubeSearch(name)
        url = grabUrl(videoId)

        self.addMedia = playAudio(self.player, 'audio', True)
        self.addMedia.play()


    def retranslateUi(self, MainWindow):
        _translate =  QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.loginBtn.setText(_translate("MainWindow", "Login"))
        self.continueBtn.setText(_translate("MainWindow", "Continue as user"))
        self.labelSearch.setText(_translate("MainWindow", "Search Results"))
        self.artistLabel.setText(_translate("MainWindow", "Artist"))
        self.songTitleLabel.setText(_translate("MainWindow", "Song Title"))
        self.popLabel.setText(_translate("MainWindow", "Popularity:"))
        self.labelSongTitle_2.setText(_translate("MainWindow", "Artist"))
        self.labelSongTitle.setText(_translate("MainWindow", "Song Title"))
        self.labelNowPlaying.setText(_translate("MainWindow", "Now Playing:"))
        self.searchBox.setPlaceholderText(_translate("MainWindow", "Search..."))
        self.searchBtn.setText(_translate("MainWindow", "Search"))
        self.labelUserName.setText(_translate("MainWindow", "UserName"))
        self.labelSubType.setText(_translate("MainWindow", "SubType"))
        self.searchOp1.setText(_translate("MainWindow", "track"))
        self.searchOp2.setText(_translate("MainWindow", "artist"))
        self.searchOp3.setText(_translate("MainWindow", "album"))
        self.searchOp4.setText(_translate("MainWindow", "playlist"))
        self.label.setText(_translate("MainWindow", "Playlists"))

if __name__ == "__main__":
    import sys
    app =QApplication(sys.argv)
    MainWindow =QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

