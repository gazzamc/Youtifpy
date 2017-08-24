# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_wip.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

import urllib
import os
import logging
import images_qr
from PyQt5.QtWidgets import (QStackedWidget, QLineEdit, QListView, QPushButton, QProgressBar,
                             QListWidget, QSlider, QTextEdit, QMenuBar, QWidget, QListWidgetItem,
                             QStatusBar, QLabel, QApplication, QMainWindow, QRadioButton, QFrame,
                             QVBoxLayout, QMenu, QHBoxLayout, QSizePolicy, QGridLayout, QLayout, QGraphicsOpacityEffect)
from PyQt5.QtCore import (Qt, QRect, QCoreApplication, QMetaObject, QSize, QPoint, QObject, QUrl, pyqtSignal, QThread)
from PyQt5.QtMultimedia import (QMediaPlayer, QMediaContent, QMediaPlaylist)
from PyQt5.QtGui import (QIcon, QPixmap, QFont, QMovie)
from functions import *
from youtube import *

# setup logger

if not (os.path.isfile(os.path.join('logs', "errorLog.log"))):

    if not os.path.isdir("logs"):
        os.makedirs("logs")

# create folder for tokens
if not os.path.isdir("data"):
    os.makedirs("data")


logging.basicConfig(filename=os.path.join('logs', "errorLog.log"), level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

# create worker thread for login / prevent gui from freezing
class LoginWorker(QObject):
    done = pyqtSignal()

    def login(self):
        login()
        self.done.emit()

    # for identification in loggedIn function
    def text(self):
        return 'Login'

class GetResultDetails(QObject):
    result = pyqtSignal(str, str, str, str, int)
    error = pyqtSignal(str, str, str, str, int)

    def __init__(self, id, option):
        super(GetResultDetails, self).__init__()
        self.option = option
        self.id = id

    def trackDetails(self):

        try:
            self.trackInfo = getData(self.id, self.option)
            self.image = self.trackInfo[2]
            self.title = self.trackInfo[0]
            self.artist = self.trackInfo[1]
            self.pop = self.trackInfo[3]

            self.result.emit(self.option, self.image, self.artist, self.title, self.pop)

        except Exception as err:

            self.error.emit("Not Found", "Not Found", "Not Found", "Not Found", 0)
            logger.error(err)

    def artistDetails(self):

        try:
            self.trackInfo = getData(self.id, self.option)
            self.name = self.trackInfo[0]
            self.image = self.trackInfo[1]
            self.pop = self.trackInfo[2]
            self.followers = self.trackInfo[3]

            self.result.emit(self.option, self.name, self.image, str(self.pop), self.followers)

        except Exception as err:

            self.error.emit(self.option, "Not Found", "Not Found", "0", 0)
            logger.error(err)

# grab youtube url and return it
class GetVideoDetails(QObject):
    result = pyqtSignal(str, str, str, str)
    error = pyqtSignal(str)

    def __init__(self, vidName, vidID, playWhen):
        super(GetVideoDetails, self).__init__()
        self.name = vidName
        self.trackDetails = getData(vidID, "track")
        self.playWhen = playWhen

    # Grabbing audio details
    def getDetails(self):

        try:
            self.videoDetails = youtubeSearch(self.name, self.trackDetails[1])
            self.url = grabUrl(self.videoDetails)
            self.result.emit(self.url, self.name, self.trackDetails[1], self.playWhen)

        except Exception as err:
            self.error.emit("{} not found".format(self.name))
            logger.error(err)

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
        self.loadingLogo.setFileName(":images\loading.gif")
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

        # set app icon
        app_icon = QIcon()
        app_icon.addFile(':images/ico_16.png', QSize(16, 16))
        app_icon.addFile(':images/ico_24.png', QSize(24, 24))
        app_icon.addFile(':images/ico_32.png', QSize(32, 32))
        app_icon.addFile(':images/ico_48.png', QSize(48, 48))
        app_icon.addFile(':images/ico_256.png', QSize(256, 256))
        MainWindow.setWindowIcon(app_icon)

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

        # list for threads
        self.threads = []

        # audio player
        self.player = QMediaPlayer(flags=QMediaPlayer.StreamPlayback)
        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)
        self.playlist.setPlaybackMode(2)

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
        self.continueBtn.clicked.connect(self.loginFunc)
        self.continueBtn.hide()

        if (os.path.isfile(os.path.join('data', "code.txt")) and
            os.path.isfile(os.path.join('data', "reftoken.txt"))):

            try:
                self.lastUserPic = QLabel(self.loginPage)
                self.lastUserPic.resize(200, 200)

                try:
                    self.imageurl = prevLogin()[1]
                    self.data = urllib.request.urlopen(self.imageurl).read()
                    self.pixmap = QPixmap()
                    self.pixmap.loadFromData(self.data, 'JPG')
                    self.pixmap_resized = self.pixmap.scaled(140, 140, Qt.KeepAspectRatio)
                    self.lastUserPic.setPixmap(self.pixmap_resized)
                    self.lastUserPic.setGeometry(QRect(130, 170, 140, 140))

                except urllib.error.URLError:
                    logger.error("No user picture available")
                    self.lastUserPic.setText("No User Image Available")
                    self.lastUserPic.setGeometry(QRect(130, 170, 140, 140))

                self.name = QLabel("Last Login: {0}".format(prevLogin()[0]), self.loginPage)

                # set username as id if none present
                if self.name.text() == "Last Login: None":
                    self.name.setText('Last Login: {0}'.format(prevLogin()[3]))

                self.name.setMinimumSize(150, 15)
                self.name.move(130, 310)
                self.notYou = QLabel('(Not You?)', self.loginPage)
                self.notYou.move(130, 325)
                self.notYou.mousePressEvent = self.clearData
                self.continueBtn.show()

            except requests.exceptions.ConnectionError as err:
                logger.error(err)

        # logo
        self.logo = QLabel(self.loginPage)
        self.logo.resize(300, 100)

        self.pixmapLogo = QPixmap()
        self.pixmapLogo.load(r':images\logo', 'PNG')
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
        #self.resultList.itemDoubleClicked.connect(lambda: self.mediaState.setText("Media Loading..."))
        self.resultList.itemDoubleClicked.connect(lambda: self.resultDoubleClick("Play Now"))
        self.resultList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.resultList.customContextMenuRequested.connect(self.listItemRightClicked)


        self.artwork = QLabel(self.resultPage)
        self.artwork.setObjectName("artwork")
        self.resultLabel1 = QLabel(self.resultPage)
        self.resultLabel1.setGeometry(QRect(580, 400, 221, 31))
        self.resultLabel1.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.resultLabel1.setObjectName("resultLabel1")
        self.resultLabel2 = QLabel(self.resultPage)
        self.resultLabel2.setGeometry(QRect(580, 415, 221, 31))
        self.resultLabel2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.resultLabel2.setObjectName("resultLabel2")
        self.resultLabel3 = QLabel(self.resultPage)
        self.resultLabel3.setGeometry(QRect(580, 430, 80, 31))
        self.resultLabel3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.resultLabel3.setObjectName("resultLabel3")
        self.stackedWidget.addWidget(self.resultPage)

        # artist page
        self.artistPage = QWidget()
        self.artistPage.setObjectName("artistPage")
        self.artistTitle = QLabel(self.artistPage)
        self.artistTitle.setText("Artist")
        self.artistTitle.setGeometry(QRect(580, 415, 221, 31))
        self.artistTitle.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.artistTitle.setObjectName("artistTitleLabel")
        self.bgImage = QLabel(self.artistPage)
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
        self.iconPlay.addFile(':images\play.png')
        self.controlPlay.setFlat(True)
        self.controlPlay.setGeometry(QRect(254, 590, 50, 50))
        self.controlPlay.setObjectName("controlPlay")
        self.controlPlay.setIcon(self.iconPlay)
        self.controlPlay.setIconSize(QSize(50, 50))
        self.controlPlay.clicked.connect(lambda: self.controlPressed("Play"))

        self.controlStop = QPushButton(self.centralwidget)
        self.iconStop = QIcon()
        self.iconStop.addFile(r':images\stop.png')
        self.controlStop.setFlat(True)
        self.controlStop.setGeometry(QRect(190, 587, 50, 50))
        self.controlStop.setObjectName("controlStop")
        self.controlStop.setIcon(self.iconStop)
        self.controlStop.setIconSize(QSize(45, 45))
        self.controlStop.clicked.connect(lambda: self.controlPressed("Stop"))

        self.controlForw = QPushButton(self.centralwidget)
        self.iconForw = QIcon()
        self.iconForw.addFile(r':images\forward.png')
        self.controlForw.setFlat(True)
        self.controlForw.setGeometry(QRect(320, 588, 50, 50))
        self.controlForw.setObjectName("controlForw")
        self.controlForw.setIcon(self.iconForw)
        self.controlForw.setIconSize(QSize(45, 45))
        self.controlForw.clicked.connect(lambda: self.controlPressed("Forward"))

        self.controlBack = QPushButton(self.centralwidget)
        self.iconBack = QIcon()
        self.iconBack.addFile(r':images\back.png')
        self.controlBack.setFlat(True)
        self.controlBack.setGeometry(QRect(120, 586, 50, 50))
        self.controlBack.setObjectName("controlBack")
        self.controlBack.setIcon(self.iconBack)
        self.controlBack.setIconSize(QSize(45, 45))
        self.controlBack.clicked.connect(lambda: self.controlPressed("Back"))

        self.controlPause = QPushButton(self.centralwidget)
        self.iconPause = QIcon()
        self.iconPause.addFile(r':images\pause.png')
        self.controlPause.setFlat(True)
        self.controlPause.setGeometry(QRect(254, 588, 50, 50))
        self.controlPause.setObjectName("controlPause")
        self.controlPause.setIcon(self.iconPause)
        self.controlPause.setIconSize(QSize(45, 45))
        self.controlPause.clicked.connect(lambda: self.controlPressed("Pause"))
        self.controlPause.hide()

        self.mediaState = QLabel(self.centralwidget)
        self.mediaState.setText("No Media Loaded")
        self.mediaState.setAlignment(Qt.AlignHCenter| Qt.AlignVCenter)
        self.mediaState.setGeometry(QRect(445, 668, 300, 16))
        self.mediaState.setAlignment(Qt.AlignHCenter)
        self.mediaState.setObjectName("mediaState")

        self.labelSongArtist = QLabel(self.centralwidget)
        self.labelSongArtist.setGeometry(QRect(980, 610, 81, 21))
        self.labelSongArtist.setObjectName("labelSongArtist")
        self.labelSongTitle = QLabel(self.centralwidget)
        self.labelSongTitle.setGeometry(QRect(980, 630, 81, 21))
        self.labelSongTitle.setObjectName("labelSongTitle")
        self.labelNowPlaying = QLabel(self.centralwidget)
        self.labelNowPlaying.setGeometry(QRect(980, 590, 121, 21))
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelNowPlaying.setFont(font)
        self.labelNowPlaying.setObjectName("labelNowPlaying")

        self.currSongPos = QLabel(self.centralwidget)
        self.currSongPos.setGeometry(QRect(437, 635, 300, 16))
        self.currSongPos.setText("-.-")

        self.currSongDur = QLabel(self.centralwidget)
        self.currSongDur.setGeometry(QRect(785, 635, 61, 16))
        self.currSongDur.setText("-.-")

        self.progressMusic = QProgressBar(self.centralwidget)
        self.progressMusic.setGeometry(QRect(470, 640, 300, 5))
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
        self.volumeControl.setGeometry(QRect(170, 650, 150, 16))
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
        self.playListsLabel = QLabel(self.centralwidget)
        self.playListsLabel.setGeometry( QRect(990, 100, 191, 21))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.playListsLabel.setFont(font)
        self.playListsLabel.setLayoutDirection( Qt.LeftToRight)
        self.playListsLabel.setTextFormat(Qt.AutoText)
        self.playListsLabel.setAlignment(Qt.AlignCenter)
        self.playListsLabel.setIndent(0)
        self.playListsLabel.setObjectName("playListslabel")
        self.listViewPlaylists =QListWidget(self.centralwidget)
        self.listViewPlaylists.setGeometry( QRect(980, 140, 211, 200))
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
        self.listViewPlaylists.setObjectName("listPlaylists")

        # Current playlists
        self.currPlaylist = QLabel(self.centralwidget)
        self.currPlaylist.setGeometry( QRect(990, 370, 191, 21))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.currPlaylist.setFont(font)
        self.currPlaylist.setLayoutDirection( Qt.LeftToRight)
        self.currPlaylist.setTextFormat(Qt.AutoText)
        self.currPlaylist.setAlignment(Qt.AlignCenter)
        self.currPlaylist.setIndent(0)
        self.currPlaylist.setObjectName("CurrentPlaylist")

        self.currPlaylistWid = QListWidget(self.centralwidget)
        self.currPlaylistWid.setGeometry( QRect(980, 400, 211, 140))
        sizePolicy =QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.currPlaylistWid.sizePolicy().hasHeightForWidth())
        self.currPlaylistWid.setSizePolicy(sizePolicy)
        self.currPlaylistWid.setAcceptDrops(False)
        self.currPlaylistWid.setAutoFillBackground(False)
        self.currPlaylistWid.setVerticalScrollBarPolicy( Qt.ScrollBarAlwaysOff)
        self.currPlaylistWid.setHorizontalScrollBarPolicy( Qt.ScrollBarAsNeeded)
        self.currPlaylistWid.setAlternatingRowColors(True)
        self.currPlaylistWid.setObjectName("listPlaylists")
        self.currPlaylistWid.clicked.connect(self.playFromCurrPlaylist)


        self.horizontalLayoutWidget.raise_()
        self.frameAlbumArt.raise_()
        #self.controlPlay.raise_()
        self.labelSongArtist.raise_()
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
        self.playListsLabel.raise_()
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
            self.labelSongArtist.hide()
            self.labelSongTitle.hide()
            self.labelNowPlaying.hide()
            self.progressMusic.hide()
            self.playListsLabel.hide()
            self.listViewPlaylists.hide()
            self.labelUserName.hide()
            self.labelSubType.hide()
            self.frameAlbumArt.hide()
            self.artwork.hide()
            self.resultLabel1.hide()
            self.resultLabel2.hide()
            self.resultLabel3.hide()
            self.mediaState.hide()

    def playFromCurrPlaylist(self):
        # get song index in list
        self.itemInd = self.currPlaylistWid.currentRow()
        self.playlist.setCurrentIndex(self.itemInd)

        if not self.player.state == 1:
            self.player.play()

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
        self.resultClick()

    def itemClicked(self, name):

        if name == "Play Now":
            self.resultDoubleClick(name)

        elif name == "Play Next":
            self.resultDoubleClick(name)

        elif name == "Artist Page":
            self.bgImageResiz = self.pixmap.scaled(self.stackedWidget.size(), Qt.KeepAspectRatioByExpanding)
            self.bgImage.setPixmap(self.bgImageResiz)
            self.bgImage.setMargin(15)
            effect = QGraphicsOpacityEffect(self.bgImage)
            effect.setOpacity(0.4)
            self.bgImage.setGraphicsEffect(effect)
            self.bgImage.show()
            self.stackedWidget.setCurrentIndex(3)

        elif name == "Album Page":
            self.stackedWidget.setCurrentIndex(4)

        elif name == "Playlist Page":
            self.stackedWidget.setCurrentIndex(5)

        else:
            # check if playlist is empty
            self.playlist.isEmpty()

    def controlPressed(self, ctrlName="", state=0):

        if ctrlName == "Play":

            self.controlPlay.hide()
            self.controlPause.show()
            self.player.play()

        elif ctrlName == "Pause":

            self.controlPause.hide()
            self.controlPlay.show()
            self.player.pause()

        elif ctrlName == "Stop":
            self.player.stop()

        elif ctrlName == "Forward":
            if not self.playlist.mediaCount() == self.playlist.currentIndex() + 1:
                self.playlist.setCurrentIndex(self.playlist.currentIndex() + 1)

        else:
            if self.playlist.currentIndex() > 0:
                self.playlist.setCurrentIndex(self.playlist.currentIndex() - 1)

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
        self.labelSongArtist.show()
        self.labelSongTitle.show()
        self.labelNowPlaying.show()
        self.progressMusic.show()
        self.mediaState.show()
        self.playListsLabel.show()
        self.listViewPlaylists.show()
        self.labelUserName.show()
        self.labelUserName.setText('Name: {0}'.format(prevLogin()[0]))

        # set username as id if none present
        if self.labelUserName.text() == "Name: None":
            self.labelUserName.setText('Name: {0}'.format(prevLogin()[3]))

        self.labelSubType.show()
        self.labelSubType.setText('Subscription: {0}'.format(prevLogin()[2]))

        # get user picture
        try:
            self.imageurl = prevLogin()[1]
            self.data = urllib.request.urlopen(self.imageurl).read()
            self.userPicSmall.resize(50, 50)
            self.pixmap = QPixmap()
            self.pixmap.loadFromData(self.data, 'JPG')
            self.pixmap_resized = self.pixmap.scaled(50, 50)
            self.userPicSmall.setPixmap(self.pixmap_resized)
            self.userPicSmall.setGeometry(QRect(1120, 10, 45, 45))

        except Exception:
            pass

        # show mainWindow
        MainWindow.show()

    def loginFunc(self):
        MainWindow.hide()

        sender = self.MainWindow.sender()
        if(sender.text() == 'Login'):

            # create seperate thread for login function
            self.thread = QThread()

            self.threads.append(self.thread)
            self.threadsAlive = len(self.threads)

            self.worker = LoginWorker()
            self.worker.moveToThread(self.thread)

            self.threads[self.threadsAlive - 1].started.connect(self.worker.login)
            self.threads[self.threadsAlive - 1].finished.connect(self.threads[self.threadsAlive - 1].deleteLater)
            self.worker.done.connect(self.loggedIn)

            self.loading = LoadingWindow()
            self.loading.show()

            # start work
            self.threads[self.threadsAlive - 1].start()

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

                self.item = self.result[:45] ## Truncate string if too long
                self.resultList.addItem(self.item)
                self.stackedWidget.setCurrentIndex(2)
                MainWindow.setWindowTitle("Youtifpy - Search Results")

        except requests.exceptions.ConnectionError as err:
            logger.error(err)

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

        # initiate thread
        self.thread = QThread()

        # get size of threads list/ add thread
        self.threads.append(self.thread)
        self.threadsAlive = len(self.threads)


        # determine which data to grab
        if self.option == 'artist':

            self.worker = GetResultDetails(self.results[1][self.id], self.option)
            self.threads[self.threadsAlive - 1].started.connect(self.worker.artistDetails)

        elif self.option == 'track':
            self.worker = GetResultDetails(self.results[1][self.id], self.option)
            self.threads[self.threadsAlive - 1].started.connect(self.worker.trackDetails)

        elif self.option == 'album':
            self.albumInfo = getData(self.results[1][self.id], self.option)

        else:
            self.playlistInfo = getData(self.results[1][self.id], self.option, self.results[3][self.id])

        self.worker.moveToThread(self.threads[self.threadsAlive - 1])
        self.worker.result.connect(self.showResultDetails)
        self.worker.error.connect(self.showResultDetails)
        self.threads[self.threadsAlive - 1].finished.connect(self.threads[self.threadsAlive - 1].deleteLater)
        self.threads[self.threadsAlive - 1].start()

    def showResultDetails(self, option, str2, str3, str4, int):

        if option == "track":

            imageUrl = str2
            artist = str3
            song = str4
            pop = int

            self.data = urllib.request.urlopen(imageUrl).read()
            self.pixmap = QPixmap()
            self.pixmap.loadFromData(self.data, 'JPG')
            self.pixmap_resized = self.pixmap.scaled(300, 300, Qt.KeepAspectRatio)
            self.artwork.setPixmap(self.pixmap_resized)
            self.artwork.setGeometry(QRect(580, 100, 300, 300))

            self.resultLabel1.setText("Artist: {0}".format(artist))
            self.resultLabel2.setText("Song: {0}".format(song))
            self.resultLabel3.setText("Popularity: {0}".format(pop))

            self.artwork.show()
            self.resultLabel1.show()
            self.resultLabel2.show()
            self.resultLabel3.show()

        elif option == "artist":

            artist = str2
            imageUrl = str3
            pop = str4
            followers = int

            self.data = urllib.request.urlopen(imageUrl).read()
            self.artwork.resize(300, 300)
            self.pixmap = QPixmap()
            self.pixmap.loadFromData(self.data, 'JPG')
            self.pixmap_resized = self.pixmap.scaled(300, 300)
            self.artwork.setPixmap(self.pixmap_resized)
            self.artwork.setGeometry(QRect(580, 100, 300, 300))

            self.resultLabel1.setText("Artist: {0}".format(artist))
            self.resultLabel2.setText("Followers: {0}".format(followers))
            self.resultLabel3.setText("Popularity: {0}".format(pop))
            self.artwork.show()
            self.resultLabel1.show()
            self.resultLabel2.show()
            self.resultLabel3.show()

    # play song
    def resultDoubleClick(self, playWhen):

        self.name = self.resultList.currentItem().text()

        self.id = self.resultList.currentRow()
        self.songId = self.results[1][self.id]

        if self.name == 'No Internet Connection':
            return

        # create thread/worker to get details
        self.thread = QThread()

        # get size of threads list/ add thread
        self.threads.append(self.thread)
        self.threadsAlive = len(self.threads)

        self.worker = GetVideoDetails(self.name, self.songId, playWhen)
        self.worker.moveToThread(self.threads[self.threadsAlive - 1])

        self.threads[self.threadsAlive - 1].started.connect(self.worker.getDetails)
        self.worker.result.connect(self.playSong)
        self.worker.error.connect(self.errorSong)
        self.threads[self.threadsAlive - 1].finished.connect(self.threads[self.threadsAlive - 1].deleteLater)
        self.threads[self.threadsAlive - 1].start()

    def errorSong(self, errorMsg):
        self.mediaState.setText(errorMsg)

    def playSong(self, url, currSongName, songArtist, playWhen):

        self.url = url

        # setup item for insertion to current playlist
        self.mediaItem = QListWidgetItem("{0} - {1}".format(currSongName[:20], songArtist[:12]))
        self.audioFile = QUrl(self.url)
        self.media = QMediaContent(self.audioFile)

        if playWhen == "Play Now":
            self.mediaState.setText("Loading Media")
            print(self.playlist.currentIndex())

            # insert into current row
            if self.playlist.currentIndex() >= 0:
                self.currPlaylistWid.insertItem(self.playlist.currentIndex(), self.mediaItem)
                self.currPlaylistWid.setCurrentItem(self.mediaItem)
                self.playlist.insertMedia(self.playlist.currentIndex(), self.media)
                self.playlist.setCurrentIndex(self.currPlaylistWid.currentRow())

            else:
                self.currPlaylistWid.insertItem(0, self.mediaItem)
                self.currPlaylistWid.setCurrentItem(self.mediaItem)
                self.playlist.insertMedia(0, self.media)
                self.playlist.setCurrentIndex(self.currPlaylistWid.currentRow())

            self.player.setVolume(self.volumeControl.value())

            # set playing now details
            self.labelSongArtist.setText(songArtist)
            self.labelSongTitle.setText(currSongName)

            # change button
            if self.controlPlay.isVisible():
                self.controlPause.show()
                self.controlPlay.hide()

            # play song
            self.player.play()
            self.mediaState.setText("Loaded Media")

        else:
            self.mediaState.setText("Adding Media to playlist")

            # check if playlist is empty/ if so add as play now
            if self.currPlaylistWid.count() == 0:
                self.currPlaylistWid.insertItem(0, self.mediaItem)
                self.currPlaylistWid.setCurrentItem(self.mediaItem)
                self.playlist.insertMedia(0, self.media)
                self.playlist.setCurrentIndex(self.currPlaylistWid.currentRow())

                # set playing now details
                self.labelSongArtist.setText(songArtist)
                self.labelSongTitle.setText(currSongName)

                # change button
                if self.controlPlay.isVisible():
                    self.controlPause.show()
                    self.controlPlay.hide()

                # play song
                self.player.play()
                self.mediaState.setText("Loaded Media")

            else:
                # insert into playlist
                self.currPlaylistWid.insertItem(self.playlist.currentIndex() + 1, self.mediaItem)
                self.playlist.insertMedia(self.playlist.currentIndex() + 1, self.media)
                self.mediaState.setText("Added to playlist")

        self.playlist.currentIndexChanged.connect(self.playerStateChange)
        self.player.durationChanged.connect(self.setDuration)
        self.player.positionChanged.connect(self.posChanged)
        self.player.mediaChanged.connect(self.updateCurrPlaylist)
        self.player.stateChanged.connect(self.stateChanged)

    def stateChanged(self, val):
        # change buttons depending on state (play/pause)
        if val == 0 or val == 2:
            self.controlPause.hide()
            self.controlPlay.show()

        else:
            self.controlPause.show()
            self.controlPlay.hide()

    def playerStateChange(self):

        if self.playlist.mediaCount() > 1 and self.playlist.currentIndex() > -1:
            self.song = self.currPlaylistWid.item(self.playlist.currentIndex()).text()
            self.songArt = self.song.split(' - ')
            self.labelSongTitle.setText(self.songArt[0])
            self.labelSongArtist.setText(self.songArt[1])

    def updateCurrPlaylist(self):
        self.currPlaylistWid.setCurrentIndex(self.playlist.currentIndex())

    # set max duration for progress bar
    def setDuration(self, val):
        self.progressMusic.setMaximum(val)
        self.progressMusic.setTextVisible(False)

        if round(((float(val % 60000))) / 1000) < 10:
            self.currSongDur.setText("{0}:0{1}".format(int(val/60000), round(((float(val % 60000))) / 1000)))

        else:
            self.currSongDur.setText("{0}:{1}".format(int(val / 60000), round(((float(val % 60000))) / 1000)))

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
        self.resultLabel1.setText(_translate("MainWindow", "Artist"))
        self.resultLabel2.setText(_translate("MainWindow", "Song Title"))
        self.resultLabel3.setText(_translate("MainWindow", "Popularity:"))
        self.labelSongArtist.setText(_translate("MainWindow", "Artist"))
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
        self.playListsLabel.setText(_translate("MainWindow", "Playlists"))
        self.currPlaylist.setText(_translate("MainWindow", "Current Playlist"))

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

