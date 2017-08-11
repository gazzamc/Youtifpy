###################################
###     Author: Gary McGovern   ###
###     File: functions.py      ###
###################################

from OAuth import *
from server import run_server
import webbrowser
import time
import os.path
import requests
import subprocess
import threading
import wget


def createThread(funcName, threadName, argsPassed=""):
    thread = threading.Thread(target=funcName, name=threadName, args=(argsPassed))
    thread.daemon = True
    thread.start()
    thread.join(1)
    return thread

def monitorThread():
    valid = True

    while valid:
        print(threading.enumerate())
        time.sleep(30)

def auth():
    responseType = "code"
    redirect = "http://127.0.0.1:5000/"
    scope = "user-read-private"
    
    fullpath = '{0}?client_id={1}&response_type={2}&redirect_uri={3}&scope={4}'.format(
        endPoints("auth"),
        clientID,
        responseType,
        redirect,
        scope
    )

    webbrowser.open(fullpath)

def endPoints(endpoint):
    authBaseUrl = "https://accounts.spotify.com/"
    apiBaseUrl = "https://api.spotify.com/"
    ytBaseUrl = "https://www.googleapis.com/"

    if endpoint == "":
        fullUrl = authBaseUrl

    elif endpoint == "auth":
        fullUrl = '{0}authorize'.format(authBaseUrl)
        
    elif endpoint == "token":
        fullUrl = '{0}api/token'.format(authBaseUrl)
        
    elif endpoint == "userData":
        fullUrl = '{0}v1/me'.format(apiBaseUrl)

    elif endpoint == "search":
        fullUrl = '{0}v1/search?q='.format(apiBaseUrl)

    elif endpoint == "artist":
        fullUrl = '{0}v1/artists/'.format(apiBaseUrl)

    elif endpoint == "track":
        fullUrl = '{0}v1/tracks/'.format(apiBaseUrl)

    elif endpoint == "youtube":
        fullUrl = '{0}youtube/v3/'.format(ytBaseUrl)

    else:
        fullUrl = ""
        print("Unknown Endpoint!")
        
    return fullUrl
    
def search(type, query, limit=20, offset=0):
    token = grabToken('token')

    searchRes = requests.get(
        '{0}{1}&type={2}&limit={3}&offset={4}'.format
        (
            endPoints("search"),
            query,
            type,
            limit,
            offset
        ),

        headers = {'Authorization': 'Bearer {0}'.format(token)})

    #check if token is still valid, if not refresh and try again
    if searchRes.status_code == 401:
        refreshToken()

        token = grabToken('token')
        searchRes = requests.get(
            '{0}{1}&type={2}&limit={3}&offset={4}'.format
            (
                endPoints("search"),
                query,
                type,
                limit,
                offset
            ),

            headers={'Authorization': 'Bearer {0}'.format(token)})


    jsonData = searchRes.json()
    results = jsonData['{0}s'.format(type)]['items']

    nameResult = []
    idResult = []
    artistResult = []

    for result in results:
        nameResult.append(result['name'])
        idResult.append(result['id'])

        if type == 'track':
            for artist in result['artists']:
                artistResult.append(artist['name'])

    return nameResult, idResult, artistResult

def getArtist(artistID):
    token = grabToken('token')
    artist = requests.get('{0}{1}'.format
    (
        endPoints("artist"),
        artistID
    ),

    headers={'Authorization': 'Bearer {0}'.format(token)})

    #check if token is still valid, if not refresh and try again
    if artist.status_code == 401:
        refreshToken()

        token = grabToken('token')
        artist = requests.get('{0}{1}'.format
            (
            endPoints("artist"),
            artistID
        ),

            headers={'Authorization': 'Bearer {0}'.format(token)})

    jsonData = artist.json()

    artistDetails = [

        jsonData['uri'],
        jsonData['id'],
        jsonData['images'][0]['url'],
        jsonData['name'],
        jsonData['genres'],
        jsonData['popularity'],
    ]

    return artistDetails

def getTrack(trackID):
    token = grabToken('token')

    track = requests.get('{0}{1}'.format
    (
        endPoints("track"),
        trackID
    ),

    headers={'Authorization': 'Bearer {0}'.format(token)})

    #check if token is still valid, if not refresh and try again
    if track.status_code == 401:
        refreshToken()

        track = requests.get('{0}{1}'.format
        (
            endPoints("track"),
            trackID
        ),

        headers={'Authorization': 'Bearer {0}'.format(token)})

    jsonData = track.json()
    trackName = jsonData['name']
    artistName = jsonData['artists'][0]['name']
    trackImage = jsonData['album']['images'][1]['url']
    popularity = jsonData['popularity']

    return trackName, artistName, trackImage, popularity

def requestToken(redirect, clientID, clientSecret):
    code = grabToken('code')
    
    getToken = requests.post(endPoints("token"), data = {
        'grant_type':'authorization_code',
        'code': code,
        'redirect_uri': redirect,
        'client_id': clientID,
        'client_secret': clientSecret
        }
    )

    if(getToken.status_code == 200):
        #extract token and expiry time
        jsonData = getToken.json()
        expires = jsonData['expires_in']
        token = jsonData['access_token']
        rToken = jsonData['refresh_token']
        
        #store token
        tokenFile = open(os.path.join('data', "token.txt"), 'w')
        tokenFile.write(token)
        tokenFile.close()

        #store refresh token
        refTokenFile = open(os.path.join('data', "reftoken.txt"), 'w')
        refTokenFile.write(rToken)
        refTokenFile.close()
        
    else:
        print('Failed to get token. Status code: {0}'.format(getToken))


def refreshToken():
    rToken = grabToken('refresh')
    
    getnewToken = requests.post(endPoints("token"), data = {
        'grant_type':'refresh_token',
        'refresh_token': rToken,
        'client_id': clientID,
        'client_secret': clientSecret
        }
    )
    jsonData = getnewToken.json()
    token = jsonData['access_token']

    #print(jsonData)
    #store token
    tokenFile = open( os.path.join('data', "token.txt"), 'w')
    tokenFile.write(token)
    tokenFile.close()

    print('Valid Token Grabbed')

def grabToken(tokenType):

    if tokenType == 'refresh':
        name = 'refToken'
    elif tokenType == 'token':
        name = 'token'
    else:
        name = 'code'

    tokenFile = open(os.path.join('data', "{0}.txt".format(name)), 'r')
    token = tokenFile.read()

    return token


def prevLogin():
    if not(os.path.isfile(os.path.join('data', "token.txt"))):
       refreshToken()
       

    token = grabToken('token')

    getUserData = requests.get(endPoints("userData"), headers = {'Authorization': 'Bearer {0}'.format(token)})

    # check if token is still valid, if not refresh and try again
    if getUserData.status_code == 401:
        refreshToken()

        getUserData = requests.get(endPoints("userData"), headers = {'Authorization': 'Bearer {0}'.format(token)})

    jsonData = getUserData.json()
    userName = jsonData['display_name']
    userPic = jsonData['images'][0]['url']
    subscrip = jsonData['product']

    if subscrip == 'open':
        subscrip = 'Free'

    return userName, userPic, subscrip

def deleteData():

    if(os.path.isfile(os.path.join('data', "code.txt")) and
       os.path.isfile(os.path.join('data', "reftoken.txt")) and
       os.path.isfile(os.path.join('data', "token.txt"))):
        
        os.remove(os.path.join('data', "code.txt"))
        os.remove(os.path.join('data', "refToken.txt"))
        os.remove(os.path.join('data', "token.txt"))

        print('Deleted')
    else:
        print('No Files to Delete')
    
def login():
    if(os.path.isfile(os.path.join('data', "code.txt")) and
       os.path.isfile(os.path.join('data', "reftoken.txt")) and
       os.path.isfile(os.path.join('data', "token.txt"))):
        
        #check if we have a valid code
        codeFile = open(os.path.join('data', "code.txt"), 'r')
        code = codeFile.read()

        if(len(code) == 0):
            print('Invalid Authorization code')
            print('Attempting to grab another')
            auth()
            
        refreshToken()
        prevLogin()
        
    else:
        createThread(run_server, "server_thread")
        createThread(monitorThread, "monitor_thread")
        auth()

        while not(os.path.isfile(os.path.join('data', "code.txt"))):
            print("Please Login to Continue!!")
            time.sleep(5)

        requestToken(redirect, clientID, clientSecret)