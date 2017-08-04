###################################
###     Author: Gary McGovern   ###
###     File: player.py         ###
###################################
## Very simple audio player using PyQt5's QMediaPlayer ##
## library.                                            ##

import os
import PyQt5
from PyQt5 import QtMultimedia
from PyQt5.QtMultimedia import (QMediaPlayer, QMediaContent)
from PyQt5.QtCore import *

def playAudio(player, filen, local=True, audioType='mp3'):

    file = QUrl()

    if local:
        #Create QUrl instance and set file path
        file = file.fromLocalFile(os.path.join('music', "{0}.{1}".format
            (
                filen,
                audioType
            )))

    else:
        #Urls seem to play but only briefly, will need to investigate this, I think it might be the buffer
        file = QUrl(filen)

    #Create media content
    media = QMediaContent(file)

    #Set audio role, needs to be done before setMedia
    player.setAudioRole(0)

    #add media to player
    player.setMedia(QMediaContent(media))

    #Set volume
    player.setVolume(9)

    return player