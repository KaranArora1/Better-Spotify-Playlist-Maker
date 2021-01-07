
class BetterSpotifyPlaylistMaker:

    def __init__(self, username: str):
        self.username = username
        self.sp = self.login()

    def login(self) -> spotify.Spotify:
        # Erase cache and prompt for user permission
        '''try:
            token = util.prompt_for_user_token(username)
        except:
            os.remove(f".cache-{username}")
            token = util.prompt_for_user_token(username)'''

        return spotipy.Spotify(oauth_manager=SpotifyOAuth(client_id=clientID, client_secret=clientSecret,
                                                          redirect_uri=clientRedirect, scope=scope,
                                                          username=self.username,
                                                          show_dialog=True))

        '''# Create our spotifyObject
        spotifyObject = spotipy.Spotify(auth=token)

        sp = spotipy.Spotify(oauth_manager=SpotifyOAuth(client_id=clientID, client_secret=clientSecret,
                                               redirect_uri=clientRedirect, scope=scope, username=username,
                                                show_dialog=True))

        user = spotifyObject.current_user()

        displayName = user['display_name']'''

    def printPlaylists(self) -> None:
        pass
        x = 0

    def releaseDate(self) -> None:
        choice: str = input(self.username + ", would you like to search through a playlist(0) or your Liked Songs(1)?")

        while choice != "0" or choice != "1":
            print("Please enter a valid answer (0 or 1)")
            choice = input("Would you like to search through a playlist(0) or your Liked Songs(1)?")

        if choice == "0":
            printPlaylists()
            print(self.sp.current_user_playlists())
            # playlistChoice =
        else:
            pass

    def run(self):
        self.login()
        self.releaseDate()


def main():
    username = input("Enter your username: ")
    playlistMaker = BetterSpotifyPlaylistMaker(username)
    playlistMaker.run()


main()