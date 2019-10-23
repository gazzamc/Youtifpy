#Required for Authenication token

clientID = "085f4232110a4daab289d7ccf51f73e5"
clientSecret = "65325bbaf339400792975070680b29d1"
ytApiKey = 'AIzaSyAYzeuLncBZ4J3xICZmPWreN0SYmUOTpaU'
baseUrl = "https://accounts.spotify.com/authorize"
tokenUrl = "https://accounts.spotify.com/api/token"
responseType = "code"
redirect = "http://127.0.0.1:5000/"
scope = "user-read-private"

fullpath = '{0}?client_id={1}&response_type={2}&redirect_uri={3}&scope={4}'.format(baseUrl, clientID,  responseType, redirect, scope)
