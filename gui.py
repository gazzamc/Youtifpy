# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_wip.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

import requests
import urllib
import os
import logging
import images_qr
from PyQt5.QtWidgets import (QStackedWidget, QLineEdit, QListView, QPushButton, QProgressBar,
                             QListWidget, QSlider, QTextEdit, QMenuBar, QWidget, QListWidgetItem,
                             QStatusBar, QLabel, QApplication, QMainWindow, QRadioButton, QScrollArea,
                             QVBoxLayout, QMenu, QHBoxLayout, QSizePolicy, QGridLayout, QLayout, QGraphicsOpacityEffect)
from PyQt5.QtCore import (Qt, QRect, QCoreApplication, QMetaObject, QSize, QPoint, QObject, QUrl, pyqtSignal, QThread, QPointF)
from PyQt5.QtMultimedia import (QMediaPlayer, QMediaContent, QMediaPlaylist)
from PyQt5.QtGui import (QIcon, QPixmap, QFont, QMovie, QPalette,  QLinearGradient, QColor, QBrush, QPainter, QPen)
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
    result = pyqtSignal(str, str, str, str, str, int)
    error = pyqtSignal(str, str, str, str, str, int)
    playlistRetrieved = pyqtSignal()

    def __init__(self, id, option, userId=""):
        super(GetResultDetails, self).__init__()
        self.option = option
        self.id = id
        self.userId = userId

    def trackDetails(self):

        try:
            self.trackInfo = getData(self.id, self.option)
            self.image = self.trackInfo[2]
            self.title = self.trackInfo[0]
            self.artist = self.trackInfo[1]
            self.artistID = self.trackInfo[3]
            self.pop = self.trackInfo[4]

            self.result.emit(self.option, self.image, self.artist, self.title, self.artistID, self.pop)

        except Exception as err:

            self.error.emit("Not Found", "Not Found", "Not Found", "Not Found", "Not Found", 0)
            logger.error(err)

    def artistDetails(self):

        try:
            self.trackInfo = getData(self.id, self.option)
            self.name = self.trackInfo[0]
            self.image = self.trackInfo[1]
            self.pop = self.trackInfo[2]
            self.followers = self.trackInfo[4]
            self.artistID = self.trackInfo[3]

            self.result.emit(self.option, self.name, self.image, str(self.pop), self.artistID, self.followers)

        except Exception as err:

            self.error.emit(self.option, "Not Found", "Not Found", "Not Found", "0", 0)
            logger.error(err)

    def albumDetails(self):

        try:
            self.albumInfo = getData(self.id, self.option)
            self.name = self.albumInfo[0]
            self.image = self.albumInfo[3]
            self.artist = self.albumInfo[1]
            self.artistId = self.albumInfo[2]
            self.tracks = self.albumInfo[4]

            self.result.emit(self.option, self.name, self.image, self.artist, self.artistId,  self.tracks)

        except Exception as err:

            self.error.emit(self.option, "Not Found", "Not Found", "Not Found", "0", 0)
            logger.error(err)

    def playlistDetails(self):

        try:
            self.albumInfo = getData(self.id, self.option, self.userId)
            self.name = self.albumInfo[0]
            self.image = self.albumInfo[2]
            self.user = self.albumInfo[1]
            self.tracks = self.albumInfo[3]

            self.result.emit(self.option, self.name, self.image, self.user, "", self.tracks)

        except Exception as err:

            self.error.emit(self.option, "Not Found", "Not Found", "Not Found", "0", 0)
            logger.error(err)


class PopulateWindow(QObject):
    result = pyqtSignal(list, list, list, list, list, list, int)
    result2 = pyqtSignal(list, list, list, list, list, list, int)
    result3 = pyqtSignal(list, list, list, list, str, list, int)
    artistAlbumResults = pyqtSignal(str, str, list, list, list)
    artistSongResults = pyqtSignal(str, str, list, list, list)
    artistRelResults = pyqtSignal(str, str, list, list, list)
    playlistRetrieved = pyqtSignal()
    done = pyqtSignal()
    done2 = pyqtSignal()

    def __init__(self, id=""):
        super(PopulateWindow, self).__init__()
        self.id = id

    def getFeaturedPlaylist(self):

        try:
            self.playlistData = getData("", "featPlaylists")
            self.playlistNames = self.playlistData[0]
            self.images = self.playlistData[1]
            self.ids = self.playlistData[2]
            self.loadedImages = []

            # adding loop for image grabbing to avoid freezing to main thread
            for i in range(len(self.images)):
                self.data = requests.get(self.images[i]).content  # This is a bit of a bottle-neck
                self.pixmap = QPixmap()
                self.pixmap.loadFromData(self.data, 'JPG')
                self.pixmap_resized = self.pixmap.scaled(140, 140, Qt.KeepAspectRatio)

                self.loadedImages.append(self.pixmap_resized)

            self.result.emit(self.playlistNames, self.loadedImages, self.ids, [], [], [], 0)
            self.playlistRetrieved.emit()
        except Exception as err:
            logger.error(err)

    def getnewReleases(self):

        try:
            self.newReleasesData = getData("", "newReleases")
            self.names = self.newReleasesData[0]
            self.artistNames = self.newReleasesData[1]
            self.artistIds = self.newReleasesData[5]
            self.images = self.newReleasesData[2]
            self.ids = self.newReleasesData[3]
            self.type = self.newReleasesData[4]
            self.loadedImages = []

            # adding loop for image grabbing to avoid freezing to main thread
            for i in range(len(self.images)):
                self.data = requests.get(self.images[i]).content  # This is a bit of a bottle-neck
                self.pixmap = QPixmap()
                self.pixmap.loadFromData(self.data, 'JPG')
                self.pixmap_resized = self.pixmap.scaled(140, 140, Qt.KeepAspectRatio)

                self.loadedImages.append(self.pixmap_resized)

            self.result2.emit(self.names, self.artistNames, self.loadedImages, self.ids, self.type, self.artistIds, 1)
            self.done.emit()

        except Exception as err:
            logger.error(err)

    def getRecomTracks(self):

        try:
            prevTrackFile = open(os.path.join('data', "prevTrack.txt"))
            self.trackDetails = prevTrackFile.read().split(',')
            self.trackId = self.trackDetails[0]
            self.trackName = self.trackDetails[1]

            self.recomTracksData = getData(self.trackId, "recomByTrack")

            self.names = self.recomTracksData[0]
            self.artists = self.recomTracksData[2]
            self.artistIds = self.recomTracksData[4]
            self.images = self.recomTracksData[1]
            self.ids = self.recomTracksData[3]
            self.loadedImages = []

            # adding loop for image grabbing to avoid freezing to main thread

            for i in range(len(self.images)):
                self.data = requests.get(self.images[i]).content  # This is a bit of a bottle-neck
                self.pixmap = QPixmap()
                self.pixmap.loadFromData(self.data, 'JPG')
                self.pixmap_resized = self.pixmap.scaled(140, 140, Qt.KeepAspectRatio)

                self.loadedImages.append(self.pixmap_resized)

            self.result3.emit(self.artists, self.names, self.loadedImages, self.ids, self.trackName, self.artistIds, 2)

        except Exception as err:
            logger.error(err)

    def getArtistAlbums(self):

        try:
            self.artistAlbumsData = getData(self.id, "artistAlbums")

            self.names = self.artistAlbumsData[1]
            self.images = self.artistAlbumsData[0]
            self.ids = self.artistAlbumsData[2]
            self.loadedImages = []

            # adding loop for image grabbing to avoid freezing to main thread
            for i in range(len(self.images)):
                self.data = requests.get(self.images[i]).content  # This is a bit of a bottle-neck
                self.pixmap = QPixmap()
                self.pixmap.loadFromData(self.data, 'JPG')
                self.pixmap_resized = self.pixmap.scaled(140, 140, Qt.KeepAspectRatio)

                self.loadedImages.append(self.pixmap_resized)

            self.artistAlbumResults.emit("artist", "albums", self.loadedImages, self.names, self.ids)
            self.done.emit()

        except Exception as err:
            logger.error(err)

    def getArtistSongs(self):

        try:
            self.artistTrackData = getData(self.id, "artistTopTracks")

            self.names = self.artistTrackData[0]
            self.images = self.artistTrackData[1]
            self.ids = self.artistTrackData[2]
            self.loadedImages = []

            # adding loop for image grabbing to avoid freezing to main thread
            for i in range(len(self.images)):
                self.data = requests.get(self.images[i]).content  # This is a bit of a bottle-neck
                self.pixmap = QPixmap()
                self.pixmap.loadFromData(self.data, 'JPG')
                self.pixmap_resized = self.pixmap.scaled(140, 140, Qt.KeepAspectRatio)

                self.loadedImages.append(self.pixmap_resized)

            self.artistSongResults.emit("artist", "songs", self.loadedImages, self.names, self.ids)
            self.done2.emit()

        except Exception as err:
            logger.error(err)

    def getArtistRel(self):

        try:
            self.artistAlbumsData = getData(self.id, "artistRelated")

            self.names = self.artistAlbumsData[0]
            self.images = self.artistAlbumsData[1]
            self.ids = self.artistAlbumsData[2]
            self.loadedImages = []

            # adding loop for image grabbing to avoid freezing to main thread
            for i in range(len(self.images)):
                self.data = requests.get(self.images[i]).content  # This is a bit of a bottle-neck
                self.pixmap = QPixmap()
                self.pixmap.loadFromData(self.data, 'JPG')
                self.pixmap_resized = self.pixmap.scaled(140, 140, Qt.KeepAspectRatio)

                self.loadedImages.append(self.pixmap_resized)

            self.artistRelResults.emit("artist", "related artists", self.loadedImages, self.names, self.ids)

        except Exception as err:
            logger.error(err)


# grab youtube url and return it
class GetVideoDetails(QObject):
    result = pyqtSignal(str, str, str, str, str, str)
    error = pyqtSignal(str)

    def __init__(self, songName, songID, playWhen, artistId):
        super(GetVideoDetails, self).__init__()
        self.name = songName
        self.songID = songID
        self.trackDetails = getData(songID, "track")
        self.playWhen = playWhen
        self.artistId = artistId

    # Grabbing audio details
    def getDetails(self):

        try:
            self.videoDetails = youtubeSearch(self.name, self.trackDetails[1])
            self.url = grabUrl(self.videoDetails)
            self.result.emit(self.url, self.name, self.trackDetails[1], self.songID, self.playWhen, self.artistId)

        except Exception as err:
            self.error.emit("Something went wrong with {}, Try again.".format(self.name))
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

        # home button
        self.returnHome = QPushButton(self.centralwidget)
        self.iconHome = QIcon()
        self.iconHome.addFile(":images/home.png")
        self.returnHome.setFlat(False)
        self.returnHome.setGeometry(QRect(590, 30, 40, 23))
        self.returnHome.setIcon(self.iconHome)
        self.returnHome.setIconSize(QSize(20, 20))
        self.returnHome.clicked.connect(self.updateHomeWindow)

        # list for threads
        self.threads = []

        # audio player
        self.player = QMediaPlayer(flags=QMediaPlayer.StreamPlayback)
        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)
        self.playlist.setPlaybackMode(2)
        self.grabbingMedia = False

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
                    self.missingPic = QPixmap(':images/ico_256.png')
                    self.missingPic_resized = self.missingPic.scaled(140, 140, Qt.KeepAspectRatio)
                    self.lastUserPic.setPixmap(self.missingPic_resized)
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
        self.bgImageMain = QLabel(self.mainPage)
        self.bgImageMain.move(200, 20)

        # set background image
        self.pixmap = QPixmap()
        self.pixmap.load(':images\ico_256', 'PNG')
        self.bgImageMainResiz = self.pixmap.scaled(self.stackedWidget.size(), Qt.KeepAspectRatioByExpanding)
        self.bgImageMain.setPixmap(self.bgImageMainResiz)
        self.bgImageMain.setMargin(0)
        effect = QGraphicsOpacityEffect(self.bgImageMain)
        effect.setOpacity(0.1)
        self.bgImageMain.setGraphicsEffect(effect)

        # set background color
        p = QPalette()
        gradient = QLinearGradient(0, 0, -50, 600)
        gradient.setColorAt(0.0, QColor(0, 0, 0))
        gradient.setColorAt(1.0, Qt.transparent)
        p.setBrush(QPalette.Window, QBrush(gradient))
        self.mainPage.setPalette(p)
        self.mainPage.setAutoFillBackground(True)
        self.mainPage.setStyleSheet("color: white")

        # Temp item for QListWidgets while loading data
        self.loadingItem = QListWidgetItem("Loading Data..")

        #  Featured Playlists
        self.featPlaylists = QLabel(self.mainPage)
        self.featPlaylists.setText("Featured Playlist's:")
        self.featPlaylists.setGeometry(QRect(50, 10, 241, 41))
        font = QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.featPlaylists.setFont(font)

        self.featPlaylistsWid = QListWidget(self.mainPage)
        self.featPlaylistsWid.addItem(self.loadingItem)
        self.featPlaylistsWid.setGeometry(QRect(50, 60, 900, 100))
        self.featPlaylistsWid.setFlow(QListWidget.LeftToRight)
        self.featPlaylistsWid.setIconSize(QSize(140, 140))
        self.featPlaylistsWid.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.featPlaylistsWid.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.featPlaylistsWid.setAutoFillBackground(False)
        self.featPlaylistsWid.setStyleSheet("background-color: transparent; border: none; color: white;")
        self.featPlaylistsWid.clicked.connect(lambda: self.populatePage("playlist", "", "", "", ""))

        #  Newly released songs
        self.newReleases = QLabel(self.mainPage)
        self.newReleases.setText("New Releases:")
        self.newReleases.setGeometry(QRect(50, 180, 241, 41))
        font = QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.newReleases.setFont(font)

        self.newReleasesWid = QListWidget(self.mainPage)
        self.newReleasesWid.addItem(self.loadingItem)
        self.newReleasesWid.setGeometry(QRect(50, 230, 900, 100))
        self.newReleasesWid.setFlow(QListWidget.LeftToRight)
        self.newReleasesWid.setIconSize(QSize(140, 140))
        self.newReleasesWid.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.newReleasesWid.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.newReleasesWid.setAutoFillBackground(False)
        self.newReleasesWid.setStyleSheet("background-color: transparent; border: none; color: white;")
        self.newReleasesWid.clicked.connect(lambda: self.resultDoubleClick("Play Now", sender="newReleases"))

        # list for later use / holds ids for retrieving data
        self.newReleasesList = []
        self.relatedTrackList = []
        self.artistAlbumsList = []
        self.artistSongsList = []
        self.artistRelatedList = []

        #  Related music (previously played)
        self.relatedMusic = QLabel(self.mainPage)
        self.relatedMusic.setText("When you listen to music this will be updated")
        self.relatedMusic.setGeometry(QRect(50, 350, 300, 70))

        self.relatedMusicWid = QListWidget(self.mainPage)
        self.relatedMusicWid.addItem(self.loadingItem)
        self.relatedMusicWid.setGeometry(QRect(50, 400, 900, 100))
        self.relatedMusicWid.setFlow(QListWidget.LeftToRight)
        self.relatedMusicWid.setIconSize(QSize(70, 70))
        self.relatedMusicWid.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.relatedMusicWid.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.relatedMusicWid.setAutoFillBackground(False)
        self.relatedMusicWid.setStyleSheet("background-color: transparent; border: none; color: white;")
        self.relatedMusicWid.clicked.connect(lambda: self.resultDoubleClick("Play Now", "relMusic"))

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
        self.resultList.itemDoubleClicked.connect(lambda: self.resultDoubleClick("Play Now"))
        self.resultList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.resultList.customContextMenuRequested.connect(self.listItemRightClicked)

        self.trackArt = ""

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

        # bg image
        self.bgImage = QLabel(self.artistPage)

        self.artistBioText = QLabel(self.artistPage)
        self.artistBioText.setWordWrap(True)
        self.artistBioText.setMargin(5)
        self.artistBioText.setGeometry(400, 130, 400, 200)

        self.artistPopSongs = QPushButton(self.artistPage)
        self.artistPopSongs.setGeometry(195, 330, 90, 30)
        self.artistPopSongs.setFlat(True)
        self.artistPopSongs.setText("Popular Songs")
        self.artistPopSongs.clicked.connect(self.changeArtistPage)


        self.artistAlbums = QPushButton(self.artistPage)
        self.artistAlbums.setGeometry(140, 330, 55, 30)
        self.artistAlbums.setFlat(True)
        self.artistAlbums.setText("Albums")
        self.artistAlbums.clicked.connect(self.changeArtistPage)

        self.artistRelated = QPushButton(self.artistPage)
        self.artistRelated.setGeometry(280, 330, 100, 30)
        self.artistRelated.setFlat(True)
        self.artistRelated.setText("Related Artists")
        self.artistRelated.clicked.connect(self.changeArtistPage)

        # list widgets for albums, pop songs and related artists
        self.albumList = QListWidget(self.artistPage)
        self.albumList.setGeometry(QRect(140, 360, 700, 150))
        self.albumList.setFlow(QListWidget.LeftToRight)
        self.albumList.setIconSize(QSize(140, 140))
        self.albumList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.albumList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.albumList.setStyleSheet("color: black")
        self.albumList.setAutoFillBackground(False)
        self.albumList.setStyleSheet("background-color: transparent; border: none;")
        self.albumList.addItem(self.loadingItem)

        self.songList = QListWidget(self.artistPage)
        self.songList.setGeometry(QRect(140, 360, 700, 150))
        self.songList.setFlow(QListWidget.LeftToRight)
        self.songList.setIconSize(QSize(140, 140))
        self.songList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.songList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.songList.setStyleSheet("color: black")
        self.songList.setAutoFillBackground(False)
        self.songList.setStyleSheet("background-color: transparent; border: none;")
        self.songList.addItem(self.loadingItem)
        self.songList.clicked.connect(lambda: self.resultDoubleClick("Play Now", "songList"))
        self.songList.hide()

        self.relArtistList = QListWidget(self.artistPage)
        self.relArtistList.setGeometry(QRect(140, 360, 700, 150))
        self.relArtistList.setFlow(QListWidget.LeftToRight)
        self.relArtistList.setIconSize(QSize(140, 140))
        self.relArtistList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.relArtistList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.relArtistList.setStyleSheet("color: black")
        self.relArtistList.setAutoFillBackground(False)
        self.relArtistList.setStyleSheet("background-color: transparent; border: none;")
        self.relArtistList.addItem(self.loadingItem)
        self.relArtistList.clicked.connect(lambda: self.setArtistPageLink(sender="relatedArtist"))
        self.relArtistList.hide()

        self.artistTitle = QLabel(self.artistPage)
        self.artistTitle.setGeometry(140, 60, 500, 50)
        self.artistTitle.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        font = QFont()
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.artistTitle.setFont(font)
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
        self.mediaState.setGeometry(QRect(445, 660, 300, 16))
        self.mediaState.setAlignment(Qt.AlignHCenter)
        self.mediaState.setObjectName("mediaState")

        # play mode buttons
        self.noRepeat = QPushButton(self.centralwidget)
        self.noRepeat.setGeometry(QRect(320, 640, 30, 30))
        self.noRepeat.setFlat(True)
        self.noRepeatIcon = QIcon()
        self.noRepeatIcon.addFile(":images/norepeat.png")
        self.noRepeat.setIcon(self.noRepeatIcon)
        self.noRepeat.setIconSize(QSize(25, 25))
        self.noRepeat.clicked.connect(self.changeMode)

        self.repeatOne = QPushButton(self.centralwidget)
        self.repeatOne.setGeometry(QRect(320, 640, 30, 30))
        self.repeatOne.setFlat(True)
        self.repeatOneIcon = QIcon()
        self.repeatOneIcon.addFile(":images/repeatone.png")
        self.repeatOne.setIcon(self.repeatOneIcon)
        self.repeatOne.setIconSize(QSize(25, 25))
        self.repeatOne.clicked.connect(self.changeMode)
        self.repeatOne.hide()

        self.repeatAll = QPushButton(self.centralwidget)
        self.repeatAll.setGeometry(QRect(320, 640, 30, 30))
        self.repeatAll.setFlat(True)
        self.repeatAllIcon = QIcon()
        self.repeatAllIcon.addFile(":images/repeatall.png")
        self.repeatAll.setIcon(self.repeatAllIcon)
        self.repeatAll.setIconSize(QSize(25, 25))
        self.repeatAll.clicked.connect(self.changeMode)
        self.repeatAll.hide()

        self.shuffle = QPushButton(self.centralwidget)
        self.shuffle.setGeometry(QRect(320, 640, 30, 30))
        self.shuffle.setFlat(True)
        self.shuffleIcon = QIcon()
        self.shuffleIcon.addFile(":images/shuffle.png")
        self.shuffle.setIcon(self.shuffleIcon)
        self.shuffle.setIconSize(QSize(25, 25))
        self.shuffle.clicked.connect(self.changeMode)
        self.shuffle.hide()

        # Current song playing info
        self.currSongArt = QLabel(self.centralwidget)
        self.currSongArt.setGeometry(QRect(860, 600, 80, 80))
        self.currSongArt.setObjectName("currSongArt")

        self.labelSongArtist = QLabel(self.centralwidget)
        self.labelSongArtist.setGeometry(QRect(980, 630, 160, 21))
        self.labelSongArtist.setObjectName("labelSongArtist")
        self.labelSongArtist.setToolTip("Click to view artist")
        self.labelSongArtist.mousePressEvent = self.setArtistPageLink

        self.labelSongTitle = QLabel(self.centralwidget)
        self.labelSongTitle.setGeometry(QRect(980, 650, 160, 21))
        self.labelSongTitle.setObjectName("labelSongTitle")

        self.labelNowPlaying = QLabel(self.centralwidget)
        self.labelNowPlaying.setGeometry(QRect(980, 610, 121, 21))
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
        self.progressMusic.mousePressEvent = self.scrubPos

        # volume slider
        self.volumeControl = QSlider(self.centralwidget)
        self.volumeControl.setGeometry(QRect(140, 650, 150, 16))
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
        self.searchBtn.setGeometry(QRect(550, 30, 40, 23))
        self.searchBtn.setFlat(False)
        self.searchIcon = QIcon()
        self.searchIcon.addFile(':images\search.png')
        self.searchBtn.setObjectName("searchBtn")
        self.searchBtn.setIcon(self.searchIcon)
        self.searchBtn.setIconSize(QSize(25, 25))
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
        self.currPlaylist.setGeometry(QRect(990, 370, 191, 21))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.currPlaylist.setFont(font)
        self.currPlaylist.setLayoutDirection(Qt.LeftToRight)
        self.currPlaylist.setTextFormat(Qt.AutoText)
        self.currPlaylist.setAlignment(Qt.AlignCenter)
        self.currPlaylist.setIndent(0)
        self.currPlaylist.setObjectName("CurrentPlaylist")

        self.currPlaylistWid = QListWidget(self.centralwidget)
        self.currPlaylistWid.setGeometry(QRect(980, 400, 211, 140))
        sizePolicy =QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.currPlaylistWid.sizePolicy().hasHeightForWidth())
        self.currPlaylistWid.setSizePolicy(sizePolicy)
        self.currPlaylistWid.setAcceptDrops(False)
        self.currPlaylistWid.setAutoFillBackground(False)
        self.currPlaylistWid.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.currPlaylistWid.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.currPlaylistWid.setAlternatingRowColors(True)
        self.currPlaylistWid.setObjectName("listPlaylists")
        self.currPlaylistWid.clicked.connect(self.playFromCurrPlaylist)

        # using this list to store song images for later use
        self.currPlaylistImages = []


        self.horizontalLayoutWidget.raise_()
        self.currSongArt.raise_()
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
            self.currSongArt.hide()
            self.controlPlay.hide()
            self.labelSongArtist.hide()
            self.labelSongTitle.hide()
            self.labelNowPlaying.hide()
            self.progressMusic.hide()
            self.playListsLabel.hide()
            self.listViewPlaylists.hide()
            self.labelUserName.hide()
            self.labelSubType.hide()
            self.currSongArt.hide()
            self.artwork.hide()
            self.resultLabel1.hide()
            self.resultLabel2.hide()
            self.resultLabel3.hide()
            self.mediaState.hide()

    def updateHomeWindow(self, prevTrack):

        # check if the home button was clicked
        self.sender = MainWindow.sender()

        # allow auto updating from another function
        try:
            if self.sender.text() == "":

                try:
                    # check to see if previous song has changed
                    prevTrackFile = open(os.path.join('data', "prevTrack.txt"))
                    self.trackDetails = prevTrackFile.read().split(',')
                    self.prevTrackName = self.trackDetails[1]

                except FileNotFoundError:
                    self.prevTrackName = "none"

            self.stackedWidget.setCurrentIndex(1)

        except AttributeError:
            self.prevTrackName = prevTrack

        self.getCurrentName = self.relatedMusic.text().split("\"")

        try:
            self.currentName = self.getCurrentName[1][1:-1]  # remove spaces

        except IndexError:
            self.currentName = "none"

        if not self.prevTrackName == self.currentName:
            # set update status and clear list
            self.relatedMusicWid.clear()
            self.relatedMusic.setText("Updating list with new music, one moment!")

            # grab new data
            self.thread = QThread()

            self.threads.append(self.thread)
            self.threadsAlive = len(self.threads)

            self.worker = PopulateWindow()
            self.worker.moveToThread(self.thread)

            self.threads[self.threadsAlive - 1].started.connect(self.worker.getRecomTracks)
            self.worker.result3.connect(self.populateHomeWindow)
            self.threads[self.threadsAlive - 1].finished.connect(self.threads[self.threadsAlive - 1].deleteLater)
            self.threads[self.threadsAlive - 1].start()

    def changeArtistPage(self):
        self.sender = MainWindow.sender()

        if self.sender.text() == "Albums":
            self.relArtistList.hide()
            self.songList.hide()
            self.albumList.show()

        elif self.sender.text() == "Popular Songs":
            self.relArtistList.hide()
            self.albumList.hide()
            self.songList.show()

        else:
            self.songList.hide()
            self.albumList.hide()
            self.relArtistList.show()

    def changeMode(self):
        if self.noRepeat.isVisible():
            self.noRepeat.hide()
            self.repeatOne.show()
            self.playlist.setPlaybackMode(1)

        elif self.repeatOne.isVisible():
            self.repeatOne.hide()
            self.repeatAll.show()
            self.playlist.setPlaybackMode(3)

        elif self.repeatAll.isVisible():
            self.repeatAll.hide()
            self.shuffle.show()
            self.playlist.setPlaybackMode(4)

        else:
            self.shuffle.hide()
            self.noRepeat.show()
            self.playlist.setPlaybackMode(2)

    def scrubPos(self, event):

        # get mouse press relative to the progressbar
        press = event.x()

        # get size of progress bar
        progBarSize = self.progressMusic.width()

        # get the value of the progress bar relative to the song duration
        maxValue = self.progressMusic.maximum()

        # check if song finished/not loaded
        if not maxValue == 0:
            # get step value
            stepValue = progBarSize / maxValue

            # get value of press
            value = press / stepValue

            # set player to position
            self.player.setPosition(value)

    def playFromCurrPlaylist(self):
        # get song index in list
        self.itemId = self.currPlaylistWid.currentRow()
        self.playlist.setCurrentIndex(self.itemId)

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
            self.menuOps = ["Play Now", "Play Next", "Artist Page"]

        elif self.option == "artist":
            self.menuOps = ["Artist Page"]

        elif self.option == "playlist":
            self.menuOps = ["View Playlist"]

        else:
            self.menuOps = ["View Album", "Artist Page"]

        for i in range(0, len(self.menuOps)):
            self.menuItems.append(self.listMenu.addAction(self.menuOps[i]))

        if self.option == "track":
            self.menuItems[0].triggered.connect(lambda: self.itemClicked(self.menuItems[0].text()))
            self.menuItems[1].triggered.connect(lambda: self.itemClicked(self.menuItems[1].text()))
            self.menuItems[2].triggered.connect(lambda: self.itemClicked(self.menuItems[2].text()))

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
            # save image for insertion into list
            self.trackArtPlay = self.trackArt
            self.resultDoubleClick(name)

        elif name == "Play Next":
            self.trackArtPlay = self.trackArt
            self.resultDoubleClick(name)

        elif name == "Artist Page":

            if not self.resultLabel1.text() == "Artist: Not Found":
                # get artist info
                self.artistInfo = getData(self.artistId, "artist")

                self.artistName = self.artistInfo[0]
                self.artistImage = self.artistInfo[1]

                # set background image
                self.data = urllib.request.urlopen(self.artistImage).read()
                self.pixmap = QPixmap()
                self.pixmap.loadFromData(self.data, 'JPG')
                self.bgImageResiz = self.pixmap.scaled(self.stackedWidget.size(), Qt.KeepAspectRatioByExpanding)
                self.bgImage.setPixmap(self.bgImageResiz)
                self.bgImage.setMargin(0)
                effect = QGraphicsOpacityEffect(self.bgImage)
                effect.setOpacity(0.1)
                self.bgImage.setGraphicsEffect(effect)

                # set background color
                p = QPalette()
                gradient = QLinearGradient(0, 0, 0, self.stackedWidget.height())
                gradient.setColorAt(0.0, QColor(0, 0, 0))
                gradient.setColorAt(1.0, Qt.transparent)
                p.setBrush(QPalette.Window, QBrush(gradient))
                self.artistPage.setPalette(p)
                self.artistPage.setAutoFillBackground(True)
                self.artistPage.setStyleSheet("color: white")

                # artist details
                self.artistTitle.setText(self.artistName)
                self.artistBio = getArtistBio(self.artistId)

                if not self.artistBio == "":
                    self.artistBioText.setText("{} ....".format(self.artistBio[:1000]))
                else:
                    self.artistBioText.setText("No Bio Available")

                # clear lists and reset view
                if len(self.albumList) > 0:
                    self.albumList.clear()
                    self.songList.clear()
                    self.relArtistList.clear()
                    self.artistSongsList.clear()
                    self.artistAlbumsList.clear()
                    self.artistRelatedList.clear()

                    self.songList.hide()
                    self.relArtistList.hide()
                    self.albumList.show()

                self.item = QListWidgetItem()
                self.item.setText("Loading Albums")
                self.albumList.addItem(self.item)

                self.thread = QThread()
                self.threads.append(self.thread)
                self.threadsAlive = len(self.threads)
                self.worker = PopulateWindow(self.artistId)
                self.worker.moveToThread(self.thread)
                self.threads[self.threadsAlive - 1].started.connect(self.worker.getArtistAlbums)
                self.worker.artistAlbumResults.connect(self.populatePage)
                self.worker.done.connect(self.worker.getArtistSongs)
                self.worker.artistSongResults.connect(self.populatePage)
                self.worker.done2.connect(self.worker.getArtistRel)
                self.worker.artistRelResults.connect(self.populatePage)
                self.threads[self.threadsAlive - 1].finished.connect(self.threads[self.threadsAlive - 1].deleteLater)
                self.threads[self.threadsAlive - 1].start()

                self.stackedWidget.setCurrentIndex(3)

        elif name == "View Album":
            # todo
            self.populatePage("album", "", "", "", "")

        elif name == "View Playlist":
            # todo
            self.populatePage("playlist", "", "", "", "")

        else:
            # check if playlist is empty
            self.playlist.isEmpty()

    def populatePage(self, page, val1, val2, val3, val4):
        if page == "artist":
            if val1 == "albums":
                if self.albumList.count() > 0:
                    self.albumList.clear()

                # if no data add item saying so and avoid loop
                if len(val3) == 0:
                    self.item = QListWidgetItem()
                    self.item.setText("No Albums")
                    self.albumList.addItem(self.item)

                else:
                    for i in range(0, len(val2)):
                        self.pixmap_resized = val2[i].scaled(140, 140, Qt.KeepAspectRatio)
                        self.icon = QIcon()
                        self.icon.addPixmap(self.pixmap_resized)
                        self.item = QListWidgetItem()
                        self.item.setIcon(self.icon)
                        self.item.setToolTip(val3[i])
                        self.albumList.addItem(self.item)

                        # store id
                        self.artistAlbumsList.append([val3[i], val2[i], val4[i]])  # name, image, id

            elif val1 == "songs":
                if self.songList.count() > 0:
                    self.songList.clear()

                # if no data add item saying so and avoid loop
                if len(val3) == 0:
                    self.item = QListWidgetItem()
                    self.item.setText("No Albums")
                    self.songList.addItem(self.item)

                else:
                    for i in range(0, len(val2)):
                        self.pixmap_resized = val2[i].scaled(140, 140, Qt.KeepAspectRatio)
                        self.icon = QIcon()
                        self.icon.addPixmap(self.pixmap_resized)
                        self.item = QListWidgetItem()
                        self.item.setIcon(self.icon)
                        self.item.setToolTip(val3[i])
                        self.songList.addItem(self.item)

                        # store id
                        self.artistSongsList.append([val3[i], val2[i], val4[i], self.artistId])

            else:
                if self.relArtistList.count() > 0:
                    self.relArtistList.clear()

                # if no data add item saying so and avoid loop
                if len(val3) == 0:
                    self.item = QListWidgetItem()
                    self.item.setText("No Albums")
                    self.relArtistList.addItem(self.item)

                else:
                    for i in range(0, len(val2)):
                        self.pixmap_resized = val2[i].scaled(140, 140, Qt.KeepAspectRatio)
                        self.icon = QIcon()
                        self.icon.addPixmap(self.pixmap_resized)
                        self.item = QListWidgetItem()
                        self.item.setIcon(self.icon)
                        self.item.setToolTip(val3[i])
                        self.relArtistList.addItem(self.item)

                        # store id
                        self.artistRelatedList.append([val3[i], val2[i], val4[i]])  # name, image, id

        elif page == "album":
            self.stackedWidget.setCurrentIndex(4)

        else:
            self.stackedWidget.setCurrentIndex(5)

    def controlPressed(self, ctrlName=""):

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
            self.playlist.next()

        else:
            self.playlist.previous()

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
        self.currSongArt.show()
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
            logger.error("No user picture available")
            self.missingPic = QPixmap(':images/ico_256.png')
            self.missingPic_resized = self.missingPic.scaled(50, 50, Qt.KeepAspectRatio)
            self.userPicSmall.setPixmap(self.missingPic_resized)

        # populate home window
        self.thread = QThread()

        self.threads.append(self.thread)
        self.threadsAlive = len(self.threads)

        self.worker = PopulateWindow()
        self.worker.moveToThread(self.thread)

        self.threads[self.threadsAlive - 1].started.connect(self.worker.getFeaturedPlaylist)
        self.worker.result.connect(self.populateHomeWindow)
        self.worker.playlistRetrieved.connect(self.worker.getnewReleases)
        self.worker.result2.connect(self.populateHomeWindow)
        self.worker.done.connect(self.worker.getRecomTracks)
        self.worker.result3.connect(self.populateHomeWindow)
        self.threads[self.threadsAlive - 1].finished.connect(self.threads[self.threadsAlive - 1].deleteLater)
        self.threads[self.threadsAlive - 1].start()

    def populateHomeWindow(self, val1, val2, val3, val4, val5, val6, val7):

        if val7 == 0:  # we know its featPlaylist's
            widget = self.featPlaylistsWid
            names = val1
            images = val2
            ids = val3

        elif val7 == 1:
            if len(self.newReleasesList) > 0:
                self.newReleasesList.clear()

            widget = self.newReleasesWid
            names = val1
            artistName = val2
            artistIds = val6
            images = val3
            ids = val4
            type = val5

        else:
            if len(self.relatedTrackList) > 0:
                self.relatedTrackList.clear()

            widget = self.relatedMusicWid
            names = val1
            artistName = val2
            artistIds = val6
            images = val3
            ids = val4
            prevTrackName = val5

            self.relatedMusic.setText("Because you listened to \" {0} \"".format(prevTrackName))

        widget.clear()

        for i in range(0, len(images)):
            self.icon = QIcon()
            self.icon.addPixmap(images[i])

            self.item = QListWidgetItem()
            self.item.setIcon(self.icon)
            if not val7 == 0:
                self.item.setToolTip("{} - {}".format(names[i], artistName[i]))

            else:
                self.item.setToolTip(names[i])

            widget.addItem(self.item)

            if val7 == 1:

                self.newReleasesList.append([names[i],
                                            artistName[i],
                                            images[i],
                                            ids[i],
                                            type[i],
                                            artistIds[i]])

                # If there's no previous song saved we need to show the main window
                if not os.path.isfile(os.path.join('data', "prevTrack.txt")) and i == len(images)-1:
                    MainWindow.show()  # show after last item is appended:


            elif val7 == 2:

                self.relatedTrackList.append([names[i],
                                            artistName[i],
                                            images[i],
                                            ids[i],
                                            artistIds[i]])

                if i == len(images)-1:
                    MainWindow.show()  # show after last item is appended

    def loginFunc(self):

        MainWindow.hide()

        sender = self.MainWindow.sender()
        if sender.text() == 'Login':

            # create separate thread for login function
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

                self.item = QListWidgetItem(self.result[:45])  # Truncate string if too long

                if self.option == "track":
                    self.item.setToolTip(self.results[2][self.results[0].index(self.result)])  # Set hover as artist

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
        self.worker = GetResultDetails(self.results[1][self.id], self.option)

        # determine which data to grab
        if self.option == 'artist':
            self.threads[self.threadsAlive - 1].started.connect(self.worker.artistDetails)

        elif self.option == 'track':
            self.threads[self.threadsAlive - 1].started.connect(self.worker.trackDetails)

        elif self.option == 'album':
            self.threads[self.threadsAlive - 1].started.connect(self.worker.albumDetails)

        else:
            self.worker = GetResultDetails(self.results[1][self.id], self.option, self.results[4][self.id])
            self.threads[self.threadsAlive - 1].started.connect(self.worker.playlistDetails)

        self.worker.moveToThread(self.threads[self.threadsAlive - 1])
        self.worker.result.connect(self.showResultDetails)
        self.worker.error.connect(self.showResultDetails)
        self.threads[self.threadsAlive - 1].finished.connect(self.threads[self.threadsAlive - 1].deleteLater)
        self.threads[self.threadsAlive - 1].start()

    def showResultDetails(self, option, str2, str3, str4, str5, int):

        if option == "track":
            # will use this later for grabbing artist info
            self.artistId = str5
            self.trackArt = str2
            self.trackArtist = str3
            self.trackName = str4
            self.trackPop = int

            # local variables
            image = self.trackArt
            data1 = self.trackArtist
            data2 = self.trackName
            data3 = self.trackPop

            label1 = "Artist"
            label2 = "Song"
            label3 = "Popularity"

        elif option == "artist":

            # local variables
            image = str3
            data1 = str2
            data2 = int
            data3 = str4

            label1 = "Artist"
            label2 = "Followers"
            label3 = "Popularity"

            # will use this later for grabbing artist info
            self.artistId = str5

        elif option == "album":

            # local variables
            image = str3
            data1 = str2
            data2 = str4
            data3 = int

            label1 = "Name"
            label2 = "Artist"
            label3 = "Tracks"

            # will use this later for grabbing artist info
            self.artistId = str5

        else:

            # local variables
            image = str3
            data1 = str2
            data2 = str4
            data3 = int

            label1 = "Name"
            label2 = "Created by"
            label3 = "Tracks"

        try:
            self.data = urllib.request.urlopen(image).read()
            self.pixmap = QPixmap()
            self.pixmap.loadFromData(self.data, 'JPG')
            self.pixmap_resized = self.pixmap.scaled(300, 300, Qt.KeepAspectRatio)
            self.artwork.setPixmap(self.pixmap_resized)
            self.artwork.setGeometry(QRect(580, 100, 300, 300))

        except Exception as err:
            logger.error(err)
            self.missingPic = QPixmap(':images/ico_256.png')
            self.missingPic_resized = self.missingPic.scaled(300, 300, Qt.KeepAspectRatio)
            self.artwork.setPixmap(self.missingPic_resized)
            self.artwork.setGeometry(QRect(580, 100, 300, 300))

        self.resultLabel1.setText("{0}: {1}".format(label1, data1))
        self.resultLabel2.setText("{0}: {1}".format(label2, data2))
        self.resultLabel3.setText("{0}: {1}".format(label3, data3))

        self.artwork.show()
        self.resultLabel1.show()
        self.resultLabel2.show()
        self.resultLabel3.show()

    def resultDoubleClick(self, playWhen, sender=""):

        if sender == "":
            self.name = self.resultList.currentItem().text()

            self.id = self.resultList.currentRow()
            self.songId = self.results[1][self.id]

            # to bypass if statement below
            self.type = "single"

        elif sender == "relMusic":

            self.name = self.relatedTrackList[self.relatedMusicWid.currentRow()][0]
            self.songId = self.relatedTrackList[self.relatedMusicWid.currentRow()][3]
            self.trackArtPlay = self.relatedTrackList[self.relatedMusicWid.currentRow()][2]
            self.artistId = self.relatedTrackList[self.relatedMusicWid.currentRow()][4]

            # to bypass if statement below
            self.type = "single"

        elif sender == "newReleases":
            self.albumId = self.newReleasesList[self.newReleasesWid.currentRow()][3]
            self.type = self.newReleasesList[self.newReleasesWid.currentRow()][4]
            self.trackArtPlay = self.newReleasesList[self.newReleasesWid.currentRow()][2]
            self.artistId = self.newReleasesList[self.newReleasesWid.currentRow()][5]

            if not self.type == "single":
                self.type = self.newReleasesList[self.newReleasesWid.currentRow()][4]

                # todo
                self.populatePage("album", "", "", "", "")

            else:
                self.getTracksData = getData(self.albumId, "albumTracks")
                self.name = self.getTracksData[0][0]
                self.songId = self.getTracksData[1][0]

        elif sender == 'songList':
            self.name = self.artistSongsList[self.songList.currentRow()][0]
            self.songId = self.artistSongsList[self.songList.currentRow()][2]
            self.trackArtPlay = self.artistSongsList[self.songList.currentRow()][1]
            self.artistId = self.artistSongsList[self.songList.currentRow()][3]

            # to bypass if statement below
            self.type = "single"

        if self.name == 'No Internet Connection':
            return

        # prevent double press on same song
        if (not self.grabbingMedia or playWhen == "Play Next") and self.type == "single":

            if not playWhen == "Play Next":
                self.grabbingMedia = True

            # create thread/worker to get details
            self.thread = QThread()

            # get size of threads list/ add thread
            self.threads.append(self.thread)
            self.threadsAlive = len(self.threads)

            self.worker = GetVideoDetails(self.name, self.songId, playWhen, self.artistId)
            self.worker.moveToThread(self.threads[self.threadsAlive - 1])

            self.threads[self.threadsAlive - 1].started.connect(self.worker.getDetails)
            self.worker.result.connect(self.playSong)
            self.worker.error.connect(self.errorSong)
            self.threads[self.threadsAlive - 1].finished.connect(self.threads[self.threadsAlive - 1].deleteLater)
            self.threads[self.threadsAlive - 1].start()

            # notify user that song is being grabbed
            self.mediaState.setText("Grabbing Media, one moment.")

        else:
            if not self.type == "album":
                self.mediaState.setText("Media already being grabbed")

    def errorSong(self, errorMsg):
        self.mediaState.setText(errorMsg)
        self.grabbingMedia = False  # in case of error allow grabbing again

    def playSong(self, url, currSongName, songArtist, songId, playWhen, artistId):

        self.url = url

        # setup item for insertion to current playlist
        self.mediaItem = QListWidgetItem("{0} - {1}".format(currSongName[:20], songArtist[:12]))
        self.audioFile = QUrl(self.url)
        self.media = QMediaContent(self.audioFile)

        # fixes issue with song data being wrong after playlist finishes and another song is added
        if self.playlist.currentIndex() == -1:
            self.playlist.setCurrentIndex(0)

        if playWhen == "Play Now":

            # insert into current row
            if self.playlist.currentIndex() >= 0:
                self.currPlaylistWid.insertItem(self.playlist.currentIndex(), self.mediaItem)
                self.currPlaylistWid.setCurrentItem(self.mediaItem)
                self.playlist.insertMedia(self.playlist.currentIndex(), self.media)
                self.playlist.setCurrentIndex(self.currPlaylistWid.currentRow())

                # add image for song to list
                self.currPlaylistImages.insert(self.playlist.currentIndex(),
                                               [self.trackArtPlay, songArtist, currSongName, songId, artistId])

            else:
                self.currPlaylistWid.insertItem(0, self.mediaItem)
                self.currPlaylistWid.setCurrentItem(self.mediaItem)
                self.playlist.insertMedia(0, self.media)
                self.playlist.setCurrentIndex(self.currPlaylistWid.currentRow())

                # add image for song to list
                self.currPlaylistImages.append([self.trackArtPlay, songArtist, currSongName, songId, artistId])

            self.player.setVolume(self.volumeControl.value())

            # set playing now details
            self.labelSongArtist.setText(songArtist)
            self.labelSongTitle.setText(currSongName)

            # change artwork
            self.changeArtwork(self.currPlaylistImages[self.playlist.currentIndex()][0])

            self.currSongArt.setPixmap(self.currSongPixmap_resized)

            # change button
            if self.controlPlay.isVisible():
                self.controlPause.show()
                self.controlPlay.hide()

            # play song
            self.player.play()

            # allow another song to be grabbed via Play Now
            self.grabbingMedia = False

        else:
            self.mediaState.setText("Adding Media to playlist")

            # check if playlist is empty/ if so add as play now
            if self.currPlaylistWid.count() == 0:
                self.currPlaylistWid.insertItem(0, self.mediaItem)
                self.currPlaylistWid.setCurrentItem(self.mediaItem)
                self.playlist.insertMedia(0, self.media)
                self.playlist.setCurrentIndex(self.currPlaylistWid.currentRow())

                # add image for song to list
                self.currPlaylistImages.append([self.trackArtPlay, songArtist, currSongName, songId, artistId])

                # set playing now details
                self.labelSongArtist.setText(songArtist)
                self.labelSongTitle.setText(currSongName)

                # change artwork
                self.changeArtwork(self.currPlaylistImages[self.playlist.currentIndex()][0])

                self.currSongArt.setPixmap(self.currSongPixmap_resized)

                # change button
                if self.controlPlay.isVisible():
                    self.controlPause.show()
                    self.controlPlay.hide()

                # play song
                self.player.play()

                # allow another song to be grabbed via Play Now
                self.grabbingMedia = False

            else:
                # insert into playlist
                self.currPlaylistWid.insertItem(self.playlist.currentIndex() + 1, self.mediaItem)
                self.playlist.insertMedia(self.playlist.currentIndex() + 1, self.media)
                self.mediaState.setText("Added to playlist")

                # add image for song to list
                self.currPlaylistImages.insert(self.playlist.currentIndex() + 1,
                                               [self.trackArtPlay, songArtist, currSongName, songId, artistId])

        self.playlist.currentIndexChanged.connect(self.playerStateChange)
        self.player.durationChanged.connect(self.setDuration)
        self.player.positionChanged.connect(self.posChanged)
        self.player.mediaChanged.connect(self.updateCurrPlaylist)
        self.player.stateChanged.connect(self.stateChanged)
        self.player.mediaStatusChanged.connect(self.mediaStatus)

    def mediaStatus(self, state):
        if state == 6:
            self.mediaState.setText("Media Buffered")

        elif state == 1:
            self.mediaState.setText("No Media")

        elif state == 4:
            self.mediaState.setText("Stalled Media")

        elif state == 2:
            self.mediaState.setText("Loading Media")

        elif state == 5:
            self.mediaState.setText("Buffering Media")

    def changeArtwork(self, image):

        # check if the image is a QPixmap or url
        if type(image) == str:
            self.data = urllib.request.urlopen(image).read()
            self.currSongPixmap = QPixmap()
            self.currSongPixmap.loadFromData(self.data, 'JPG')
            self.currSongPixmap_resized = self.currSongPixmap.scaled(80, 80, Qt.KeepAspectRatio)
            self.currSongArt.setPixmap(self.currSongPixmap_resized)
        else:
            self.currSongPixmap_resized = image.scaled(80, 80, Qt.KeepAspectRatio)
            self.currSongArt.setPixmap(self.currSongPixmap_resized)

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
            self.labelSongTitle.setText(self.currPlaylistImages[self.playlist.currentIndex()][2])
            self.labelSongArtist.setText(self.currPlaylistImages[self.playlist.currentIndex()][1])

            # change artwork
            self.changeArtwork(self.currPlaylistImages[self.playlist.currentIndex()][0])

    def setArtistPageLink(self, sender=""):
        if sender == "relatedArtist":
            self.artistId = self.artistRelatedList[self.relArtistList.currentRow()][2]
            self.itemClicked("Artist Page")

        else:
            if not self.labelSongArtist.text() == "Artist":
                self.artistId = self.currPlaylistImages[self.playlist.currentIndex()][4]
                self.itemClicked("Artist Page")

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

        elif round(((float(val % 60000))) / 1000) == 60:
            self.currSongPos.setText("{0}:00".format(int(val / 60000)))

        else:
            self.currSongPos.setText("{0}:{1}".format(int(val / 60000), round(((float(val % 60000))) / 1000)))

        # set current track on spotify/locally for later use
        # needs to be played for more than 30 seconds
        # will only check between 30 - 35 seconds to avoid writes at every check after said time.
        if (self.progressMusic.value() >= 30 * 1000) and (self.progressMusic.value() <= 35 * 1000):

            # update related list

            try:
                # check to see if previous song has changed
                prevTrackFile = open(os.path.join('data', "prevTrack.txt"))
                self.trackDetails = prevTrackFile.read().split(',')
                self.prevTrackName = self.trackDetails[1]

            except FileNotFoundError:
                self.prevTrackName = "none"

            # update the previous song
            setCurrentTrack(self.currPlaylistImages[self.playlist.currentIndex()][3],
                            self.currPlaylistImages[self.playlist.currentIndex()][2])

            if not self.prevTrackName == self.currPlaylistImages[self.playlist.currentIndex()][2]:
                self.updateHomeWindow(self.currPlaylistImages[self.playlist.currentIndex()][2])

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
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
        self.searchBtn.setText(_translate("MainWindow", ""))
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

