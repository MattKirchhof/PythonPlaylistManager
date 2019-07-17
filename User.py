import pickle


class User:

    # When we initialize a User object, we automatically try to load an existing user, otherwise we create a new one
    def __init__(self, name:str):
        self.name = name
        self._allAudioFiles = None
        self._allPlaylists = None

        try: 
            loadedUser = pickle.load( open( (name + ".pkl"), "rb" ) )

            print("DEBUG: User loaded: " + name + ".pkl")

            self.allAudioFiles = loadedUser.allAudioFiles
            self.allPlaylists = loadedUser.allPlaylists
        
        except:
            # No user exists. We simply initialized a new one in the User constructor
            print("DEBUG: No matching file: "+ name + ".pkl")
            pass


    # When we save a User object, we automatically update its variables (song and playlist lists) and dump it to a file
    def saveUser(self, songlist, playlists):
        self._allAudioFiles = songlist
        self._allPlaylists = playlists

        with open((self.name + '.pkl'), 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

    
    @property
    def allAudioFiles(self):
        return self._allAudioFiles
    @allAudioFiles.setter
    def allAudioFiles(self, songs:list):
        self._allAudioFiles = songs

    @property
    def allPlaylists(self):
        return self._allPlaylists
    @allPlaylists.setter
    def allPlaylists(self, playlists:list):
        self._allPlaylists = playlists

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name:str):
        self._name = name