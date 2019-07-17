from AudioFile import AudioFile, Song, Podcast

# Is a playlist, stores a name and a list of songs
class Playlist:
    def __init__(self, name:str):
        self._name = name
        self._songList = []

    # Checks if the playlist contains a specific song instance
    def containsSong(self, audio:AudioFile):
        for a in self._songList:
            if (a == audio):
                return True
        return False
    
    # Adds a song instance to the playlist
    def addAudio(self, audio:AudioFile):
        self._songList.append(audio)

    # Removes a song instance from the playlist
    def removeAudio(self, audio:AudioFile):
        self._songList.remove(audio)


    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name:str):
        self._name = name

    @property
    def songList(self):
        return self._songList
    @songList.setter
    def songList(self, songs:list):
        self._songList = songs