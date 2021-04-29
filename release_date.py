import spotipy
#from spotipy import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify
#from spotipy import util
import secrets
import ujson
#import os


# Verify that user inputs numbers (predicate)
# Exceptions (release date is incorrect for album)

# Comments
# More features
# Run using command line args
# User has to enter a valid playlist number


class BetterSpotifyPlaylistMaker:
    
    def __init__(self, username: str):
        
        self.CLIENT_REDIRECT = "http://localhost:8000"
        self.SCOPE = "playlist-read-collaborative " \
                     "playlist-read-private " \
                     "user-library-read " \
                     "playlist-modify-public " \
                     "playlist-modify-private"
        
        self.username = username
        self.sp = self.login() # Spotify object 
        self.name = self.sp.current_user()["display_name"]
        self.filteringOptions = {1: ("Release Date", self.releaseDate), 
                                 2: ("Genre", self.genre)}
    
    # Make sure you login with the correct account (same one as username entered)
    def login(self) -> spotipy.Spotify:
        return spotipy.Spotify(oauth_manager=SpotifyOAuth(client_id=secrets.clientID, client_secret=secrets.clientSecret,
                               redirect_uri=self.CLIENT_REDIRECT, scope=self.SCOPE, username=self.username,
                               show_dialog=True))

    # Add predicate so that we can check if user enters integers when choosing years
    # Verifies that user's input is appropriate
    def verifyInput(self, question: str, acceptableAnswers: list) -> int:

        choice = int(input(self.name + ", " + question))

        while choice not in acceptableAnswers:
            print("Please enter a valid answer.")
            choice = int(input(self.name + ", " + question))

        return choice 
    
    def createPlaylist(self, name: str, description: str):
        return self.sp.user_playlist_create(self.username, name, False, False, "Auto-generated " + description)
    
    # Predicates know the size and contents of compareTo, check if track came before/after/between dates
    def lessThan(self, trackReleaseYear: int, compareTo: tuple) -> bool: 
        return trackReleaseYear < compareTo[0]
    
    def greaterThan(self, trackReleaseYear: int, compareTo: tuple) -> bool: 
        return trackReleaseYear > compareTo[0]

    def betweenRange(self, trackReleaseYear: int, compareTo: tuple) -> bool:
        return compareTo[0] < trackReleaseYear < compareTo[1]

    # Adds tracks to a playlist depending on their release date
    def addByReleaseDate(self, newPlaylistID: str, sourcePlaylistID: str, compareYears: tuple, beforeAfterChoice: int):
        
        add = []
        flag = False

        # Assign the appropriate functor
        if beforeAfterChoice == 1:
            functor = self.lessThan
        elif beforeAfterChoice == 2:
            functor = self.greaterThan
        else:
            functor = self.betweenRange

        # If a playlistID is supplied, use it
        if sourcePlaylistID:
            searchThrough = self.sp.playlist(sourcePlaylistID)["tracks"] #["items"]
        # If the playlistID is none, go through user's saved tracks
        else:
            searchThrough = self.sp.current_user_saved_tracks(limit=50)

        while searchThrough["next"]:
            tracks = searchThrough["items"]
            
            # Grab each track's release date from the appropriate source and add it to the list conditionally
            for track in tracks:
                # If song is not on Spotify (manually added), ignore it
                try:
                    trackYear = int(track["track"]["album"]["release_date"][0:4])

                    if (functor(trackYear, compareYears)):
                        add.append(track["track"]["id"])
                        
                except TypeError:
                    print("Skipped")
            
            # Maximum number of songs you can add at a time is 100 
            # Reset add as it hits 100
            if len(add) > 100:
                self.sp.playlist_add_items(newPlaylistID, add[0:100], None)
                add = add[100:]
            
            searchThrough = self.sp.next(searchThrough)
        
        # Get remaining songs that were not added by loop 
        tracks = searchThrough["items"]

        for track in tracks:
            try:
                trackYear = int(track["track"]["album"]["release_date"][0:4])

                if (functor(trackYear, compareYears)):
                    add.append(track["track"]["id"])
                    
            except TypeError:
                print("Skipped")
        
        if len(add) > 100:
            self.sp.playlist_add_items(newPlaylistID, add[0:100], None)
            add = add[100:]
            
        # If the list is not empty, add the last remaining songs
        if add:
            self.sp.playlist_add_items(newPlaylistID, add, None)

    def addByGenre(self, newPlaylistID: str, sourcePlaylistID: str, genre):
        pass
        add = []

        if sourcePlaylistID:
            searchThrough = self.sp.playlist(sourcePlaylistID)["tracks"]
        else:
            searchThrough = self.sp.current_user_saved_tracks(limit=50)
        
        

    # Print all of a user's playlists (numbered)
    def printPlaylists(self, json):
 
        index = 1
        
        for playlist in json['items']:
            print(str(index) + ": " + playlist["name"])
            index += 1
    
    def printGenres(self, playlistID: str):
        
        index = 1
        tracks = self.sp.playlist(playlistID)["items"]
        genres = {}

        for track in tracks:
            albumID = tracks[track]["album"]["id"]

            album = self.sp.album(albumID)

            for genre in album["genres"]:
                genres.add(genre) 
        
        for genre in genres:
            print(genre)

    # USER HAS TO ENTER A VALID PLAYLIST NUMBER FINISH
    # Prompt user to pick a playlist and return that playlist's ID
    def pickPlaylists(self, json) -> str:
        num = int(input("Which playlist would you like to use to create a new playlist? "))
        #playlist = json["items"][num-1]
        id = json["items"][num-1]["id"]
        #self.writeJSON("playlist.json", self.sp.playlist(id))

        return id
    
    # Driver function for creating playlists by release date
    def releaseDate(self):
        newPlaylistName = input("New playlist name: ")
        beforeAfterChoice = self.verifyInput("before, after, or range? (1/2/3) ", [1, 2, 3])
        
        # Ask for year and create tuple
        if beforeAfterChoice == 1 or beforeAfterChoice == 2:
            year = int(input("What year? "))
            years = (year,)

        # If user chooses 'range', then ask for two years
        else:
            startYear, endYear = input("Range of years (ex: 2002 2010) ").split()
            years = (int(startYear), int(endYear))
                
        choice = self.verifyInput("would you like to search through a playlist(1) or your Liked Songs(2)? ", [1, 2])
        
        # Print playlists, pick one, create a new playlist, and add to that new playlist
        if choice == 1:
            json = self.sp.current_user_playlists()
            self.printPlaylists(json)
            #self.writeJSON("release_date.json", json)

            sourcePlaylistID = self.pickPlaylists(json)
            newPlaylistID = self.createPlaylist(newPlaylistName, "release date")["id"]

            self.addByReleaseDate(newPlaylistID, sourcePlaylistID, years, beforeAfterChoice)

        # Create a new playlist and add to it from Liked Songs
        else:
            newPlaylistID = self.createPlaylist(newPlaylistName, "release date")["id"]
            self.addByReleaseDate(newPlaylistID, None, years, beforeAfterChoice)
    
    def genre(self):
        newPlaylistName = input("New playlist name: ")
        choice = self.verifyInput("Would you like to search through a playlist(1) or your Liked Songs(2)? ", [1, 2])
        
        if choice == 1:
            json = self.sp.current_user_playlists()
            self.printPlaylists(json)
            sourcePlaylistID = self.pickPlaylists(json)

            self.printGenres(sourcePlaylistID)

            genre = str(input("What genre? "))
            genres = (genre,)

            newPlaylistID = self.createPlaylist(newPlaylistName, "genre")["id"]
            self.addByGenre(newPlaylistID, sourcePlaylistID, genres)
        
        else:
            self.printGenres(json)

            genre = str(input("What genre? "))
            genres = (genre,)

            newPlaylistID = self.createPlaylist(newPlaylistName, "genre")["id"]
            self.addByGenre(newPlaylistID, None, genres)

    def printFilteringOptions(self):
        for item in self.filteringOptions.items():
            key = str(item[0])
            optionName = item[1][0]

            print(key + ": " + optionName)

    # Helper to write JSON to a file
    def writeJSON(self, filename: str, json):
        with open(filename, "w") as file:
            # username: xcx8r5lndgmfok5lci3ze8spa
            ujson.dump(json, file, indent=4)
    
    # Run BetterSpotifyPlaylistMaker's methods in one function
    def run(self):
        self.login()

        print()
        self.printFilteringOptions()
        print()

        choice = self.verifyInput("How would you like to filter your songs? ", self.filteringOptions.keys())
        function = self.filteringOptions[choice][1]
        
        function()
    

def main():
    username = input("Enter your username: ")
    playlistMaker = BetterSpotifyPlaylistMaker(username)
    playlistMaker.run()
    
    
main()
