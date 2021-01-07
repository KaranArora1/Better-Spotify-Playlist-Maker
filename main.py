
import spotipy
from spotipy import SpotifyClientCredentials
from spotipy import Spotify
from spotipy import util
from secrets import *
import ujson


def trackInPlaylist(spotify: Spotify, trackname, playlist):

    result = spotify.playlist_tracks(playlist, offset=0, limit=50)

    while result["next"]:
        try:
            if result["items"]["track"][trackname]:
                print("match")
                return True
        except KeyError:
            result = spotify.next(result)
        '''for track in result["items"]:
            track = track["track"]

            if track["name"] == trackname:
                print("match")
                print(trackname)
                return True'''

        #result = spotify.next(result)

    print("miss")
    print(trackname)
    return False


def getPlaylistIDByName(spotify, playlistName):
    playlist_id = ""
    for playlist in spotify.current_user_playlists()["items"]:
        print(playlist["name"])
        if playlist["name"] == playlistName:
            playlist_id = playlist["id"]
            break

    return playlist_id

def main():

    clientRedirect = "http://localhost:8000"

    username = "karan.arora.28"

    scope = "playlist-read-collaborative " \
            "playlist-read-private " \
            "user-library-read " \
            "playlist-modify-public " \
            "playlist-modify-private"

    token = util.prompt_for_user_token(username, scope, clientID, clientSecret, clientRedirect)

    spotify = Spotify(auth=token)

    result = spotify.current_user_saved_tracks(offset=0, limit=50)
    data = {}

    songs = {}

    exceptions = ("Depeche Mode", "Grant Miller", "Madonna", "Ministry", "The Beach Boys", "Mickey & Sylvia",
                  "The Clovers", "Village People", "Frank Sinatra", "Rodríguez", "The Bangles", "U2",
                  "UB40", "Tom Petty", "Faces", "Bobby McFerrin", "Dion", "Fancy", "Eddy Huntington",
                  "Michael Jackson", "OutKast", "Gorillaz", "Diddy", "Lipps Inc.", "Chuck Berry", "Marvin Gaye",
                  "The Kinks", "Count Basie", "Player", "Steve Lawrence", "Nelly", "The Killers", "Billy Idol",
                  "Haddaway", "Blondie")
    dontwant = ("Emile Van Krieken")

    '''while result["next"]:
        for track in result["items"]:
            songs.update(track["track"]["name"])
        result = spotify.next(result)

    data = {username: songs}'''
    num = 0
    playlist_id = ""
    for playlist in spotify.current_user_playlists()["items"]:
        if playlist["name"] == "Computer Generated Old 2":
            playlist_id = playlist["id"]

    exceptions_list = []

    while result["next"]:
        for track in result["items"]:
            num = num + 1
            print(num)

            track = track["track"]

            '''songs.update({track["uri"]:
                              {"track": track["name"],
                               "artist": track["artists"][0]["name"],
                               "artist uri": track["artists"][0]["uri"],
                               "album": track["album"]["name"],
                               "album uri": track["album"]["uri"]
                              }
                          })'''

            album = spotify.album(track["album"]["id"])

            '''if (int(album["release_date"][0:4]) < 2000 or track["artists"][0]["name"] in exceptions): #and int(album["release_date"][0:4]) > 2006)\

                    #print(track["uri"])
                    print(track["id"])
                    print(track["name"])
                    spotify.user_playlist_add_tracks("karan.arora.28", playlist_id, [track["uri"]])'''

            if (int(album["release_date"][0:4]) < 2006) or track["artists"][0]["name"] in exceptions:
                spotify.user_playlist_add_tracks("karan.arora.28", playlist_id, [track["uri"]])

                if track["artists"][0]["name"] not in exceptions_list:
                    exceptions_list.append(track["artists"][0]["name"])

            print(exceptions_list)

            '''else:
                #pid = getPlaylistIDByName(spotify, "Old??")
                pid = "2qSyS6sDfEGSS38cn4GR8U"
                if trackInPlaylist(spotify, track["name"], pid):
                    print(track["name"])
                    print(track["artists"][0]["name"])
                    num = num +1
                    print(num)'''


        result = spotify.next(result)


        #spotify.
        #spotify.user_playlist_create(clientID, "Python Old", False, "")

    #albumuri
    #artist Name and URI
    #when track was added
    #track name and URI

    #From this data, get when album was released, get genres,

    #username -> playlists -> songs -> songs contain all the data about genres and artists, etc.

    '''data = songs

    with open("data.json", "r") as file:
        json = ujson.load(file)
        json.update({username: data})

    with open("data.json", "w") as file:
        ujson.dump(json, file, indent=4)'''


main()
