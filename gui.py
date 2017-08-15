# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_wip.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

import urllib
import os
from PyQt5.QtWidgets import (QStackedWidget, QLineEdit, QListView, QPushButton, QProgressBar,
                             QListWidget, QSlider, QTextEdit, QMenuBar, QWidget, QLCDNumber,
                             QStatusBar, QLabel, QApplication, QMainWindow, QRadioButton, QFrame,
                             QVBoxLayout, QMenu, QHBoxLayout, QSizePolicy, QGridLayout, QLayout)
from PyQt5.QtCore import (Qt, QRect, QCoreApplication, QMetaObject, QSize, QPoint, QObject, QUrl)
from PyQt5.QtMultimedia import (QMediaPlayer, QMediaContent, QMediaPlaylist)
from PyQt5.QtGui import (QIcon, QPixmap, QFont, QMovie)
from functions import *
from youtube import *
from player import *

# create worker thread for login / prevent gui from freezing
class LoginWorker(QObject):
    done = pyqtSignal()

    def login(self):
        login()
        self.done.emit()

    #for identification in loggedIn function
    def text(self):
        return 'Login'

# grab youtube url and return it
class GetVideoDetails(QObject):
    result = pyqtSignal(str)

    def __init__(self, var):
        super(GetVideoDetails, self).__init__()
        self.name = var
        #print(self.name)

    # Grabbing audio details
    def getDetails(self):
        self.videoDetails = youtubeSearch(self.name)
        self.url = grabUrl(self.videoDetails)
        print(self.url)
        self.result.emit(self.url)

class LoadingWindow(QWidget):
    def __init__(self):
        super(LoadingWindow, self).__init__()
        self.setWindowTitle("Youtifpy - Logging In!")
        self.setFixedSize(400, 600)
        self.init_ui()

    def init_ui(self):
        # logo gif
        self.logogif = QLabel(self)
        self.logogif.resize(300, 200)
        self.loadingLogo = QMovie()
        self.loadingLogo.setFileName("images\loading.gif")
        self.logogif.setMovie(self.loadingLogo)
        self.loadingLogo.start()
        self.logogif.setGeometry(QRect(50, 180, 300, 200))
        #self.show()

        if (self.loadingLogo.isValid() == False):
            self.logogif.setText('No image found!')

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

        # audio player
        self.player = QMediaPlayer(flags=QMediaPlayer.StreamPlayback)
        self.playlist = QMediaPlaylist()
        self.playlist.setPlaybackMode(0)

        # login page
        self.loginPage = QWidget()
        self.loginPage.setObjectName("loginPage")
        self.loginBtn = QPushButton(self.loginPage)
        self.loginBtn.setGeometry(QRect(140, 350, 121, 41))
        self.loginBtn.setObjectName("loginBtn")
        self.loginBtn.clicked.connect(self.loginFunc)

        # get previous users data
        self.continueBtn = QPushButton(self.loginPage)
        self.continueBtn.setGeometry(QRect(140, 400, 121, 41))
        self.continueBtn.setObjectName("continueBtn")
        self.continueBtn.clicked.connect(self.loggedIn)
        self.continueBtn.hide()

        if (os.path.isfile(os.path.join('data', "code.txt")) and
            os.path.isfile(os.path.join('data', "reftoken.txt"))):

            try:
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

            except requests.exceptions.ConnectionError:
                pass

        # logo
        self.logo = QLabel(self.loginPage)
        self.logo.resize(300, 100)

        self.pixmapLogo = QPixmap()
        self.pixmapLogo.load(r'images\logo', 'PNG')
        self.pixmapLogo_resized = self.pixmapLogo.scaled(300, 200)
        self.logo.setPixmap(self.pixmapLogo_resized)
        self.logo.setGeometry(QRect(50, 0, 300, 200))


        self.stackedWidget.addWidget(self.loginPage)

        # main page
        self.mainPage = QWidget()
        self.mainPage.setObjectName("mainPage")
        self.stackedWidget.addWidget(self.mainPage)

        # result page
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
        self.resultList.itemDoubleClicked.connect(lambda: self.mediaState.setText("Media Loading..."))
        self.resultList.itemDoubleClicked.connect(self.resultDoubleClick)
        self.resultList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.resultList.customContextMenuRequested.connect(self.listItemRightClicked)


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

        # artist page
        self.artistPage = QWidget()
        self.artistPage.setObjectName("artistPage")
        self.artistTitle = QLabel(self.artistPage)
        self.artistTitle.setText("Artist")
        self.artistTitle.setGeometry(QRect(580, 415, 221, 31))
        self.artistTitle.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.artistTitle.setObjectName("artistTitleLabel")
        self.stackedWidget.addWidget(self.artistPage)

        # album page
        self.albumPage = QWidget()
        self.albumPage.setObjectName("albumPage")
        self.albumTitle = QLabel(self.albumPage)
        self.albumTitle.setText("Album")
        self.albumTitle.setGeometry(QRect(580, 415, 221, 31))
        self.albumTitle.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.albumTitle.setObjectName("albumTitleLabel")
        self.stackedWidget.addWidget(self.albumPage)

        # playlist page
        self.playlistPage = QWidget()
        self.playlistPage.setObjectName("playlistPage")
        self.playlistTitle = QLabel(self.playlistPage)
        self.playlistTitle.setText("Playlist")
        self.playlistTitle.setGeometry(QRect(580, 415, 221, 31))
        self.playlistTitle.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.playlistTitle.setObjectName("playlistTitleLabel")
        self.stackedWidget.addWidget(self.playlistPage)

        # settings page
        self.settingsPage = QWidget()
        self.settingsPage.setObjectName("settingsPage")
        self.stackedWidget.addWidget(self.settingsPage)
        self.gridLayoutCenter.addWidget(self.stackedWidget, 0, 0, 1, 1)

        # music player
        self.frameAlbumArt = QFrame(self.centralwidget)
        self.frameAlbumArt.setGeometry(QRect(40, 590, 100, 70))
        #self.frameAlbumArt.setFrameShape(QFrame.StyledPanel)
        #self.frameAlbumArt.setFrameShadow(QFrame.Raised)
        self.frameAlbumArt.setObjectName("frameAlbumArt")

        # player controls
        self.controlPlay = QPushButton(self.centralwidget)
        self.iconPlay = QIcon()
        self.iconPlay.addFile('images\play.png')
        self.controlPlay.setFlat(True)
        self.controlPlay.setGeometry(QRect(604, 587, 50, 50))
        self.controlPlay.setObjectName("controlPlay")
        self.controlPlay.setIcon(self.iconPlay)
        self.controlPlay.setIconSize(QSize(50, 50))
        self.controlPlay.clicked.connect(lambda: self.controlPressed("Play"))

        self.controlStop = QPushButton(self.centralwidget)
        self.iconStop = QIcon()
        self.iconStop.addFile(r'images\stop.png')
        self.controlStop.setFlat(True)
        self.controlStop.setGeometry(QRect(540, 585, 50, 50))
        self.controlStop.setObjectName("controlStop")
        self.controlStop.setIcon(self.iconStop)
        self.controlStop.setIconSize(QSize(45, 45))

        self.controlForw = QPushButton(self.centralwidget)
        self.iconForw = QIcon()
        self.iconForw.addFile(r'images\forward.png')
        self.controlForw.setFlat(True)
        self.controlForw.setGeometry(QRect(670, 587, 50, 50))
        self.controlForw.setObjectName("controlForw")
        self.controlForw.setIcon(self.iconForw)
        self.controlForw.setIconSize(QSize(45, 45))

        self.controlBack = QPushButton(self.centralwidget)
        self.iconBack = QIcon()
        self.iconBack.addFile(r'images\back.png')
        self.controlBack.setFlat(True)
        self.controlBack.setGeometry(QRect(470, 586, 50, 50))
        self.controlBack.setObjectName("controlBack")
        self.controlBack.setIcon(self.iconBack)
        self.controlBack.setIconSize(QSize(45, 45))

        self.controlPause = QPushButton(self.centralwidget)
        self.iconPause = QIcon()
        self.iconPause.addFile(r'images\pause.png')
        self.controlPause.setFlat(True)
        self.controlPause.setGeometry(QRect(604, 585, 50, 50))
        self.controlPause.setObjectName("controlPause")
        self.controlPause.setIcon(self.iconPause)
        self.controlPause.setIconSize(QSize(45, 45))
        self.controlPause.clicked.connect(lambda: self.controlPressed("Pause"))
        self.controlPause.hide()

        self.mediaState = QLabel(self.centralwidget)
        self.mediaState.setText("No Media Loaded")
        self.mediaState.setAlignment(Qt.AlignHCenter| Qt.AlignVCenter)
        self.mediaState.setGeometry(QRect(543, 660, 100, 16))
        self.mediaState.setObjectName("mediaState")

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

        self.currSongPos = QLabel(self.centralwidget)
        self.currSongPos.setGeometry(QRect(750, 635, 61, 16))
        self.currSongPos.setText("-.-")

        self.currSongDur = QLabel(self.centralwidget)
        self.currSongDur.setGeometry(QRect(775, 635, 61, 16))
        self.currSongDur.setText("/ -.-")

        self.progressMusic = QProgressBar(self.centralwidget)
        self.progressMusic.setGeometry(QRect(445, 640, 300, 5))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressMusic.sizePolicy().hasHeightForWidth())
        self.progressMusic.setSizePolicy(sizePolicy)
        self.progressMusic.setProperty("value", 0)
        self.progressMusic.setTextVisible(False)
        self.progressMusic.setObjectName("progressMusic")

        # volume slider
        self.volumeControl = QSlider(self.centralwidget)
        self.volumeControl.setGeometry(QRect(445, 650, 200, 10))
        self.volumeControl.setObjectName("volumeControl")
        self.volumeControl.setOrientation(Qt.Horizontal)
        self.volumeControl.setMaximum(100)
        self.volumeControl.setValue(30)
        self.volumeControl.valueChanged.connect(self.changeVolumeVal)

        # search
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

        # user info
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

        # search options
        self.searchOp1 = QRadioButton(self.centralwidget)
        self.searchOp1.setGeometry( QRect(660, 30, 70, 17))
        self.searchOp1.setChecked(True)
        self.searchOp1.setObjectName("radioButton")
        self.searchOp1.toggled.connect(self.getSearchParms)  # On toggle change re-search with new params/toggle

        self.searchOp2 = QRadioButton(self.centralwidget)
        self.searchOp2.setGeometry( QRect(720, 30, 70, 17))
        self.searchOp2.setObjectName("radioButton_2")
        self.searchOp2.toggled.connect(self.getSearchParms)

        self.searchOp3 = QRadioButton(self.centralwidget)
        self.searchOp3.setGeometry( QRect(780, 30, 70, 17))
        self.searchOp3.setObjectName("radioButton_3")
        self.searchOp3.toggled.connect(self.getSearchParms)

        self.searchOp4 = QRadioButton(self.centralwidget)
        self.searchOp4.setGeometry( QRect(840, 30, 70, 17))
        self.searchOp4.setObjectName("radioButton_4")
        self.searchOp4.toggled.connect(self.getSearchParms)

        self.searchOps = [self.searchOp1, self.searchOp2, self.searchOp3, self.searchOp4]

        # playlists
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
        #self.controlPlay.raise_()
        self.labelSongTitle_2.raise_()
        self.labelSongTitle.raise_()
        self.labelNowPlaying.raise_()
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

        # hiding stuff if on login page
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
            self.controlPlay.hide()
            self.labelSongTitle_2.hide()
            self.labelSongTitle.hide()
            self.labelNowPlaying.hide()
            self.progressMusic.hide()
            self.label.hide()
            self.listViewPlaylists.hide()
            self.labelUserName.hide()
            self.labelSubType.hide()
            self.frameAlbumArt.hide()
            self.songArtwork.hide()
            self.artistLabel.hide()
            self.songTitleLabel.hide()
            self.popLabel.hide()
            self.mediaState.hide()

    def changeVolumeVal(self, val):
        self.player.setVolume(val)

    def songPosChanged(self):

        self.curPos = self.player.position()

        self.progressMusic.setProperty("value", (self.curPos / 1000))

    def listItemRightClicked(self, QPos):

        self.listMenu = QMenu()
        self.menuItems = []

        for self.searchOp in self.searchOps:
            if self.searchOp.isChecked():
                self.option = self.searchOp.text()
                break

        if self.option == "track":
            self.menuOps = ["Play Now", "Play Next"]

        elif self.option == "artist":
            self.menuOps = ["Artist Page"]

        elif self.option == "playlist":
            self.menuOps = ["View Playlist"]

        else:
            self.menuOps = ["View Album", "View Artist"]

        for i in range(0, len(self.menuOps)):
            self.menuItems.append(self.listMenu.addAction(self.menuOps[i]))

        if self.option == "track":
            self.menuItems[0].triggered.connect(lambda: self.itemClicked(self.menuItems[0].text()))
            self.menuItems[1].triggered.connect(lambda: self.itemClicked(self.menuItems[1].text()))

        elif self.option == "artist":
            self.menuItems[0].triggered.connect(lambda: self.itemClicked(self.menuItems[0].text()))

        elif self.option == "playlist":
            self.menuItems[0].triggered.connect(lambda: self.itemClicked(self.menuItems[0].text()))

        else:
            self.menuItems[0].triggered.connect(lambda: self.itemClicked(self.menuItems[0].text()))
            self.menuItems[1].triggered.connect(lambda: self.itemClicked(self.menuItems[1].text()))

        self.parentPosition = self.resultList.mapToGlobal(QPoint(0, 0))
        self.listMenu.move(self.parentPosition + QPos)
        self.listMenu.show()

    def itemClicked(self, name):

        if name == "Play Now":
            self.resultDoubleClick()

        elif name == "Artist Page":
            self.stackedWidget.setCurrentIndex(3)

        elif name == "Album Page":
            self.stackedWidget.setCurrentIndex(4)

        elif name == "Playlist Page":
            self.stackedWidget.setCurrentIndex(5)

        else:
            # check if playlist is empty
            self.playlist.isEmpty()

    def controlPressed(self, ctrlName="", state=0):

        if ctrlName == "Play" or state == 1:

            self.controlPlay.hide()
            self.controlPause.show()
            self.player.play()

        elif ctrlName == "Pause" or state == 0 \
                                 or state == 2:

            self.controlPause.hide()
            self.controlPlay.show()
            self.player.pause()

        elif ctrlName == "Stop":
            self.player.stop()

    def loggedIn(self):

        sender = self.MainWindow.sender()

        if sender.text() == "Login":
            self.loading.hide()

        # go to main page
        self.stackedWidget.setCurrentIndex(1)
        MainWindow.setFixedSize(1200, 700)
        MainWindow.setWindowTitle("Youtifpy - Home")

        # show all hidden elements
        self.searchBox.show()
        self.searchBtn.show()
        self.searchOp1.show()
        self.searchOp2.show()
        self.searchOp3.show()
        self.searchOp4.show()
        self.frameAlbumArt.show()
        self.controlPlay.show()
        self.labelSongTitle_2.show()
        self.labelSongTitle.show()
        self.labelNowPlaying.show()
        self.progressMusic.show()
        self.mediaState.show()
        self.label.show()
        self.listViewPlaylists.show()
        self.labelUserName.show()
        self.labelUserName.setText('Name: {0}'.format(prevLogin()[0]))
        self.labelSubType.show()
        self.labelSubType.setText('Subscription: {0}'.format(prevLogin()[2]))

        # get user picture
        self.imageurl = prevLogin()[1]
        self.data = urllib.request.urlopen(self.imageurl).read()
        self.userPicSmall.resize(50, 50)
        self.pixmap = QPixmap()
        self.pixmap.loadFromData(self.data, 'JPG')
        self.pixmap_resized = self.pixmap.scaled(50, 50)
        self.userPicSmall.setPixmap(self.pixmap_resized)
        self.userPicSmall.setGeometry(QRect(1120, 10, 45, 45))

        # show mainWindow
        MainWindow.show()

    def loginFunc(self):
        MainWindow.hide()

        sender = self.MainWindow.sender()
        if(sender.text() == 'Login'):

            #create seperate thread for login function
            self.thread = QThread()
            self.worker = LoginWorker()
            self.worker.moveToThread(self.thread)

            self.thread.started.connect(self.worker.login)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.done.connect(lambda: self.loggedIn())

            self.loading = LoadingWindow()
            self.loading.show()

            #start work
            self.thread.start()

        else:
            self.loggedIn()

    def clearData(self, event):
        deleteData()
        self.lastUserPic.hide()
        self.name.hide()
        self.notYou.hide()
        self.continueBtn.hide()

    def getSearchParms(self):

        # Prevents function being called twice by
        # toggle. Probably unnecessary but i like
        # the feature

        self.getSender = self.MainWindow.sender()

        for self.searchOp in self.searchOps:
            if self.searchOp.isChecked():
                self.toggled = self.searchOp
                break

        if self.getSender == self.toggled:
            return

        #######################################

        self.searchText = self.searchBox.text()

        if self.searchText == '':
            return

        if self.resultList.count() > 0:
            self.resultList.clear()

        for self.searchOp in self.searchOps:
            if self.searchOp.isChecked():
                self.option = self.searchOp.text()
                break
        try:
            self.results = search(str(self.option), self.searchText, 30)

            for self.result in self.results[0]:

                self.item = self.result
                self.resultList.addItem(self.item)
                self.stackedWidget.setCurrentIndex(2)
                MainWindow.setWindowTitle("Youtifpy - Search Results")

        except requests.exceptions.ConnectionError:

            self.item = 'No Internet Connection'
            self.resultList.addItem(self.item)

    # display song info
    def resultClick(self):

        for self.searchOp in self.searchOps:
            if self.searchOp.isChecked():
                self.option = self.searchOp.text()
                break

        self.name = self.resultList.currentItem().text()

        if self.name == 'No Internet Connection':
            return

        self.id = self.resultList.currentRow()

        if self.option == 'artist':
            self.artistInfo = getData(self.results[1][self.id], self.option)

        elif self.option == 'track':
            self.trackInfo = getData(self.results[1][self.id], self.option)

            self.imageurl = self.trackInfo[2]
            self.data = urllib.request.urlopen(self.imageurl).read()
            self.songArtwork.resize(300, 300)
            self.pixmap = QPixmap()
            self.pixmap.loadFromData(self.data, 'JPG')
            self.pixmap_resized = self.pixmap.scaled(300, 300)
            self.songArtwork.setPixmap(self.pixmap_resized)
            self.songArtwork.setGeometry(QRect(580, 100, 300, 300))

            self.artistLabel.setText("Artist: {0}".format(self.trackInfo[1]))
            self.songTitleLabel.setText("Song: {0}".format(self.trackInfo[0]))
            self.popLabel.setText("Popularity: {0}".format(self.trackInfo[3]))

            self.songArtwork.show()
            self.artistLabel.show()
            self.songTitleLabel.show()
            self.popLabel.show()

        elif self.option == 'album':
            self.albumInfo = getData(self.results[1][self.id], self.option)

        else:
            self.playlistInfo = getData(self.results[1][self.id], self.option, self.results[3][self.id])

    # play song
    def resultDoubleClick(self, string=""):

        self.mediaState.setText("Media Loaded")
        self.name = self.resultList.currentItem().text()
        if self.name == 'No Internet Connection':
            return

        self.controlPlay.hide()
        self.controlPause.show()

        # create thread/worker to get details
        self.thread = QThread()
        self.worker = GetVideoDetails(self.name)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.getDetails)
        self.worker.result.connect(self.playSong)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()



    def playSong(self, url):

        self.url = url

        download = False

        self.audioFile = QUrl()

        if not download:

            self.audioFile = QUrl(self.url)
            self.media = QMediaContent(self.audioFile)
            self.playlist.clear()
            self.playlist.addMedia(self.media)
            self.player.setMedia(self.media)

        else:

            self.audioFile = self.audioFile.fromLocalFile(os.path.join('music', "audio.mp3"))
            self.media = QMediaContent(self.audioFile)
            self.playlist.clear()
            self.playlist.addMedia(self.media)

        #self.playlist.setCurrentIndex(0)
        self.player.setPlaylist(self.playlist)
        self.player.setVolume(self.volumeControl.value())
        self.player.stateChanged.connect(lambda: self.controlPressed("", self.player.state()))
        self.player.positionChanged.connect(lambda: self.songPosChanged())

        self.player.durationChanged.connect(self.setDuration)
        self.player.positionChanged.connect(self.posChanged)
        self.player.play()

    # set max duration for progress bar
    def setDuration(self, val):
        self.progressMusic.setMaximum(val)
        self.progressMusic.setTextVisible(False)

        self.currSongDur.setText("/ {0}:{1}".format(int(val/60000), round(((float(val % 60000)))/1000)))

    # update progress bar with current position
    def posChanged(self, val):
        self.progressMusic.setProperty('value', val)

        if round(((float(val % 60000))) / 1000) < 10:
            self.currSongPos.setText("{0}:0{1}".format(int(val / 60000), round(((float(val % 60000))) / 1000)))
        else:
            self.currSongPos.setText("{0}:{1}".format(int(val / 60000), round(((float(val % 60000))) / 1000)))

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
        app = QApplication(sys.argv)
        MainWindow = QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        loadWindow = LoadingWindow()
        loadWindow.hide()
        sys.exit(app.exec_())

