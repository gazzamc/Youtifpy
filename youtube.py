# Author: Gary McGovern
# functions to grab youtube audio links
# youtube.py

import requests
import re
import urllib.parse
import wget
from bs4 import BeautifulSoup
from OAuth import *
from functions import endPoints

def youtubeSearch(query, name, part='id', maxRes=20):

    query = urllib.parse.quote("{0} {1}".format(query, name))

    searchRes = requests.get(
        '{0}search?part={1}&maxResults={2}&q={3}&key={4}'.format
        (
            endPoints("youtube"),
            part,
            maxRes,
            query,
            ytApiKey
        ),

        )

    jsonData = searchRes.json()

    try:
        # grab first result id only
        videoID = jsonData['items'][0]['id']['videoId']

    except KeyError:
        # grab second result id only
        videoID = jsonData['items'][1]['id']['videoId']

    return videoID



#Temporary workaround, using external site(s)
def grabProtURL(ytID):
    baseUrl = 'http://genyoutube.com/watch?v='

    request = requests.get('{0}{1}'.format(baseUrl,ytID))

    html = BeautifulSoup(request.text, "lxml")
    links = html.findAll('a', href=True)

    for link in links:
        audio = str(link).find('itag=36')

        if audio != -1:
            l = re.search('{0}(.+?){1}'.format('href="','"'), str(link))

            if l:
                audioLink = l.group(1).replace('amp;','')
            break

    return audioLink

### wip, need to figure out how to decipher protected video signatures ###
### Currently grabs unprotected videos ###

def grabUrl(ytID):

    baseUrl = 'http://www.youtube.com/watch?v='
    url = requests.get('{0}{1}'.format(baseUrl,ytID))

    soup = BeautifulSoup(url.text, "lxml")
    div = soup.find("div", {"id" : "player-mole-container"})
    scripts = div.findAll("script")[1].contents

    links = str(scripts).split('u0026url=')

    for link in links:
            audio = link.find('mime%3Daudio%252Fwebm')

            if audio != -1:
                    audioUrlUnformatted = link

                    #clean up url, remove unnecessary stuff
                    #link is unpredictable could end with slash or comma
                    urlSlash = link.find(r'\\')
                    urlComma = link.find(',')

                    if urlSlash < urlComma:
                        urlEnd = urlSlash
                    else:
                        urlEnd = urlComma

                    urlEncoded = link[0: urlEnd]
                    audioUrl = urllib.parse.unquote(urlEncoded)
                    break

    def findString(string, start, end, start2 = ''):

            s = re.search('{0}(.+?){1}'.format(start, end), string)
            if s:
                #This is mainly for grabbing the signature, it's tag is dependant
                if len(s.group(1)) < 10:
                    s = re.search('{0}(.+?){1}'.format(start2, end), string)

                    comma = str(s.group(1)).find(',')

                    if comma != -1:
                        subString = str(s.group(1))[0: comma]

                    else:
                        subString = s.group(1)

                else:
                    subString = s.group(1)

                return subString

    #host = findString(str(audioUrlUnformatted), 'https%3A%2F%2F', '.googlevideo') #'r5---sn-uigxxpx-q0cl'
    #signature = findString(str(audioUrlUnformatted), 's=', r'\\', 'u0026s=')
    #unSecSig = findString(str(audioUrl), 'signature%3D', '%')
    #ei = findString(str(audioUrlUnformatted),'ei%3D', '%') #'Ri95WcLICdKe1gL0rakY'
    #expire = findString(str(audioUrlUnformatted),'expire%3D', '%')
    #id = findString(str(audioUrlUnformatted),'id%3', '%')
    #dur = findString(str(audioUrlUnformatted),'dur%3D', '%')
    #title = findString(str(scripts),'"title":"', '",').replace(' ', '+')
    #ip = findString(str(audioUrlUnformatted),'ip%3D', '%')
    #mn = findString(str(audioUrlUnformatted),'mn%3', '%')
    #mt = findString(str(audioUrlUnformatted),'mt%3D', '%')
    #lmt = findString(str(audioUrlUnformatted),'lmt%3D', '%')
    #clen = findString(str(audioUrlUnformatted),'clen%3D', '%')
    #initcwndbps = findString(str(audioUrlUnformatted),'initcwndbps%3D', '%')

    try:
        # Grab protected link
        protUrl = grabProtURL(ytID)

        return protUrl

    except requests.exceptions.ConnectionError:

        return audioUrl