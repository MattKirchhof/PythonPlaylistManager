import requests
import xml.etree.cElementTree as ET
from Exceptions import *

class LastFmConnection:
    _apiKey = '58c6585b32cb65fe51d310bb4c34695f'
    _url = 'http://ws.audioscrobbler.com/2.0/'

    # Performs a GET request to the last.fm API and attempts to gather and return the song information.
    def getSongDetails(self, songTitle, songArtist):
        
        requestDetails = {'method': 'track.getInfo', 'api_key': self._apiKey, "artist" : songArtist, "track" : songTitle}
        
        try:
            r = requests.get(self._url, requestDetails)
        except:
            raise GenericConnectionException("An error occured when connecting..")

        print("DEBUG: URL request: " + r.url)

        tree = ET.fromstring(r.text)
        
        if (tree.attrib.get('status') == 'ok'):
            try:
                ImgURL = tree[0].find('album').findall('image')[1].text
            except:
                ImgURL = None

            return [ImgURL, songTitle, songArtist]

        else:
            raise(LastFMException(tree[0].text))

