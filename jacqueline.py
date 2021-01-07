import spotipy
from spotipy import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify
from spotipy import util
from secrets import *
import ujson
import os

#IT TIES IT TO WHAT ACCOUNT YOU LOGGED IN WITH WHEN YOU ENTERED THAT USERNAME IN CODE
# I WAS USING
# WHEN JACQUELINE TRIED SIGNING INTO HER ACCOUNT, THE CACHE DIDNT EXIST
# BUT SHOW DIALOG WASN"T ON, SO IT AUTOMATICALLY OPENED SPOTIFY WEBSITE AND LOGGED IN WITH MY ACCOUNT,
# TYING HER OAUTH TO MY DATA

# IF I WASNT LOGGED IN ON SAFARI, IT WOULDVE WORKED

#WHATEVER YOU"RE SIGNED IN WITH ON YOUR BROWSER MATTTERRRSSS IF SHOW DIALOG ISNT ON


#clientRedirect = "http://localhost:8080/"
#clientRedirect = "http://localhost:8888/callback"
clientRedirect = "http://localhost:8000"

username = "xcx8r5lndgmfok5lci3ze8spa"
#username = "karan.arora.28"

scope = "user-library-read"

sp = spotipy.Spotify(oauth_manager=SpotifyOAuth(client_id=clientID, client_secret=clientSecret,
                                               redirect_uri=clientRedirect, scope=scope, username=username,
                                                show_dialog=True))
print(username)
print(sp.current_user())
results = sp.current_user_saved_tracks()

print(results)

#print(results)

'''

#token = util.prompt_for_user_token(username, scope, clientID, clientSecret, clientRedirect)

spotify = Spotify(auth=token)

result = spotify.current_user_saved_tracks(offset=0, limit=50)'''

'''with open("jacqueline.json", "w") as file:
    ujson.dump(results, file, indent=4)'''