import spotipy
from spotipy import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify
from spotipy import util
from secrets import *
import ujson
import os


# Verify that user inputs numbers (predicate)
# Exceptions (release date is incorrect for album)


class BetterSpotifyPlaylistMaker:
    
    def __init__(self, username: str):
        
        self.CLIENT_REDIRECT = "http://localhost:8000"
        self.SCOPE = "playlist-read-collaborative " \
                     "playlist-read-private " \
                     "user-library-read " \
                     "playlist-modify-public " \
                     "playlist-modify-private"
        
        self.username = username
        self.sp = self.login()
        self.name = self.sp.current_user()["display_name"]
        
    def login(self) -> spotipy.Spotify:
        return spotipy.Spotify(oauth_manager=SpotifyOAuth(client_id=clientID, client_secret=clientSecret,
                               redirect_uri=self.CLIENT_REDIRECT, scope=self.SCOPE, username=self.username,
                               show_dialog=True))

    # Add predicate so that we can check if user enters integers when choosing years
    def verifyInput(self, question: str, acceptableAnswers: list) -> int:

        choice = int(input(self.name + ", " + question))

        while choice not in acceptableAnswers:
            print("Please enter a valid answer.")
            choice = int(input(self.name + ", " + question))

        return choice 
    
    def createPlaylist(self, name: str, description: str):
        return self.sp.user_playlist_create(self.username, name, False, False, "Auto-generated " + description)
    
    def lessThan(self, trackReleaseYear: int, compareTo: tuple) -> bool: 
        return trackReleaseYear < compareTo[0]
    
    def greaterThan(self, trackReleaseYear: int, compareTo: tuple) -> bool: 
        return trackReleaseYear > compareTo[0]

    def betweenRange(self, trackReleaseYear: int, compareTo: tuple) -> bool:
        return compareTo[0] < trackReleaseYear < compareTo[1]

    def addByReleaseDate(self, newPlaylistID: str, sourcePlaylistID: str, compareYears: tuple, beforeAfterChoice: str) -> None:
        
        add = []

        if beforeAfterChoice == 1:
            functor = self.lessThan
        elif beforeAfterChoice == 2:
            functor = self.greaterThan
        else:
            functor = self.betweenRange

        if sourcePlaylistID:
            searchThrough = self.sp.playlist(sourcePlaylistID)["tracks"]["items"]
        else:
            searchThrough = self.sp.current_user_saved_tracks()["items"]
        
        for track in searchThrough:
            trackYear = int(track["track"]["album"]["release_date"][0:4])

            if (functor(trackYear, compareYears)):
                add.append(track["track"]["id"])
        
        if add:
            self.sp.playlist_add_items(newPlaylistID, add, None)

    def printPlaylists(self, json) -> None:
 
        index = 1
        
        for playlist in json['items']:
            print(str(index) + ": " + playlist["name"])
            index += 1

    def pickPlaylists(self, json) -> str:
        num = int(input("Which playlist would you like to use to create a new playlist?"))
        playlist = json["items"][num-1]
        id = json["items"][num-1]["id"]
        self.writeJSON("playlist.json", self.sp.playlist(id))

        return id
    
    def releaseDate(self) -> None:
        newPlaylistName = input("New playlist name?")
        beforeAfterChoice = self.verifyInput("before, after, or range? (1/2/3)", [1, 2, 3])
        
        if beforeAfterChoice == 1 or beforeAfterChoice == 2:
            year = int(input("What year?"))
            years = (year,)
        else:
            startYear, endYear = input("Range of years (ex: 2002 2010)").split()
            years = (int(startYear), int(endYear))
                
        choice = self.verifyInput("would you like to search through a playlist(1) or your Liked Songs(2)?", [1, 2])
        
        if choice == 1:
            json = self.sp.current_user_playlists()
            self.printPlaylists(json)
            self.writeJSON("release_date.json", json)
            sourcePlaylistID = self.pickPlaylists(json)
            newPlaylistID = self.createPlaylist(newPlaylistName, "release date")["id"]
            self.addByReleaseDate(newPlaylistID, sourcePlaylistID, years, beforeAfterChoice)
        else:
            json = self.sp.current_user_saved_tracks()
            newPlaylistID = self.createPlaylist(newPlaylistName, "release date")["id"]
            self.addByReleaseDate(newPlaylistID, None, years, beforeAfterChoice)

    def writeJSON(self, filename: str, json):
        with open(filename, "w") as file:
            # username: xcx8r5lndgmfok5lci3ze8spa
            ujson.dump(json, file, indent=4)
    
    def run(self):
        self.login()
        self.releaseDate()
    

def main():
    username = input("Enter your username: ")
    playlistMaker = BetterSpotifyPlaylistMaker(username)
    playlistMaker.run()
    
    
main()