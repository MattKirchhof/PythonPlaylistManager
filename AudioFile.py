from Artist import Artist
import xml.etree.cElementTree as ET

# Parent audio file class. Contains a file path, name, optional rating, and auto assigns a unique ID for each file.
class AudioFile():
    _fId = 0

    def __init__(self, imURL:str, name:str, rating:int = 0):
        self._imageURL = imURL
        self._name = name
        self._rating = rating

        self._fId = AudioFile._fId
        AudioFile._fId += 1

        print ("AudioFile Created with ID: " + str(self._fId))

    # Builds and saves an XML file of the song to a file
    def saveXML(self):
        root = ET.Element("root")
        audio = ET.SubElement(root, "AudioFile")

        ET.SubElement(audio, "AudioName", name = "AudioName").text = self.name
        ET.SubElement(audio, "Rating", name = "Rating").text = str(self.rating)
        ET.SubElement(audio, "Detail", name = "Detail").text = str(self.getDetail())
        if (self._imageURL != None):
            ET.SubElement(audio, "ImageURL", name = "ImageURL").text = self._imageURL

        tree = ET.ElementTree(root)
        tree.write((self.name + ".xml"))

        print(ET.tostring(root, encoding='utf8').decode('utf8'))


    # Secondary XML function to add itself to the root of an already initialized XML tree and return the result
    def addXML(self, root):
        audio = ET.SubElement(root, "AudioFile")

        ET.SubElement(audio, "AudioName", name = "AudioName").text = self.name
        ET.SubElement(audio, "Rating", name = "Rating").text = str(self.rating)
        ET.SubElement(audio, "Detail", name = "Detail").text = str(self.getDetail())
        if (self._imageURL != None):
            ET.SubElement(audio, "ImageURL", name = "ImageURL").text = self._imageURL

        return root


    def getDetail(self):
        return ""

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name:str):
        self._name = name

    @property
    def rating(self):
        return self._rating
    @rating.setter
    def rating(self, rating:int):
        self._rating = rating

    @property
    def imageURL(self):
        return self._imageURL
    @imageURL.setter
    def imageURL(self, imageURL:str):
        self._imageURL = imageURL


# Is a podcast, a form of audio file. Similar to Song. Stores a file path, name, artist, rating, and episode
class Podcast(AudioFile):
    def __init__(self, imURL:str, sName:str, episode:int = 1, rating:int = 0):
        super().__init__(imURL, sName, rating)
        self._episode = episode

    def getDetail(self):
        return self.episode

    @property
    def episode(self):
        return self._episode
    @episode.setter
    def episode(self, episode:int):
        self._episode = episode
        

# Is a song, a form of audio file. Stores a file path, name, artist, rating
class Song(AudioFile):

    def __init__(self, imURL:str, sName:str, artist:Artist = Artist("No Artist"), rating:int = 0):
        super().__init__(imURL, sName, rating)
        self._artist = artist
        
    def getDetail(self):
        return self.artist.name

    @property
    def artist(self):
        return self._artist
    @artist.setter
    def artist(self, artist:Artist):
        self._artist = artist
        