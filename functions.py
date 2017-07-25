# Author: Gary McGovern
# functions.py

from OAuth import *
import webbrowser
import time
import os.path
import requests
import subprocess

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
    
    print(fullpath)
    #webbrowser.open(fullpath)

def endPoints(endpoint):
    authBaseUrl = "https://accounts.spotify.com/"
    apiBaseUrl = "https://api.spotify.com/"

    if endpoint == "":
        fullUrl = authBaseUrl

    elif endpoint == "auth":
        fullUrl = '{0}authorize'.format(authBaseUrl)
        
    elif endpoint == "token":
        fullUrl = '{0}api/token'.format(authBaseUrl)
        
    elif endpoint == "userData":
        fullUrl = '{0}v1/me'.format(apiBaseUrl)

    else:
        fullUrl = ""
        print("Unknown Endpoint!")
        
    return fullUrl
    

def requestToken(redirect, clientID, clientSecret):
    codeFile = open(os.path.join('data', "code.txt"), 'r')
    code = codeFile.read()
    
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
    refTokenFile = open(os.path.join('data', "reftoken.txt"), 'r')
    rToken = refTokenFile.read()
    
    getnewToken = requests.post(endPoints("token"), data = {
        'grant_type':'refresh_token',
        'refresh_token': rToken,
        'client_id': clientID,
        'client_secret': clientSecret
        }
    )
    jsonData = getnewToken.json()
    token = jsonData['access_token']
    
    #store token
    tokenFile = open( os.path.join('data', "token.txt"), 'w')
    tokenFile.write(token)
    tokenFile.close()

    print('Valid Token Grabbed')

def prevLogin():
    if not(os.path.isfile(os.path.join('data', "token.txt"))):
       print("No Previous login")
       
    else:
        tokenFile = open( os.path.join('data', "token.txt"), 'r')
        token = tokenFile.read()

        getUserData = requests.get(endPoints("userData"), headers = {'Authorization': 'Bearer {0}'.format(token)})
        jsonData = getUserData.json()

        userName = jsonData['display_name']
        userPic = jsonData['images'][0]['url']
        return userName, userPic


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
            subprocess.Popen("server.py 1", shell=True)
            auth()
            
        refreshToken()
        prevLogin()
        
    else:
        subprocess.Popen("server.py 1", shell=True)
        auth()

        while not(os.path.isfile(os.path.join('data', "code.txt"))):
            print("Please Login to Continue!!")
            time.sleep(5)
        requestToken(redirect, clientID, clientSecret)
