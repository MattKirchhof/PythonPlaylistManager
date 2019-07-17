from AudioFile import AudioFile, Song, Podcast
from Exceptions import *
from Playlist import Playlist
from Artist import Artist
from User import User
from LastFmConnection import LastFmConnection
from GUI import GUI

#External Packages
import tkinter as tk
from tkinter import simpledialog
from tkinter import StringVar
from tkinter.scrolledtext import ScrolledText

# To make REST and SOAP requests
from urllib.request import urlopen
from suds.client import Client

# To display album art pulled from RESTful request
from PIL import Image, ImageTk #Python Imaging Library
import requests
from io import BytesIO

# To process XML playlists and such
import xml.etree.cElementTree as ET


# Master music player class. Primary model backend that runs the program.
class MusicPlayer():
    _audioList = []
    _masterPlaylistName = "Main Library"

    def __init__(self):
        self._playlists = []
        self.currentPlaylist = None
        self.currentSong = None
        self.currentUser = None

        # Populate our song list for usage (Custom offline songs)
        self._audioList.append(Song(None, "Darude Sandstorm", rating=2))
        self._audioList.append(Song(None, "Baby Dont Hurt Me", rating=1))
        self._audioList.append(Song(None, "I Want To Break Free", rating=4))
        self._audioList.append(Podcast(None, "How Its Made", 1, rating=4))
        self._audioList.append(Podcast(None, "How Its Made", 2, rating=3))
        self._audioList.append(Podcast(None, "How Its Made", 3, rating=3))
        
        self.newPlaylist(self._masterPlaylistName, self._audioList)

        # Populate more with online REST information pulled from last.fm
        self.importSongWithREST("Sweet Mountain River", "Monster Truck")
        self.importSongWithREST("Aural Psynapse", "deadmau5")
        self.importSongWithREST("Piano Man", "Billy Joel")
        self.importSongWithREST("Best Of You", "Foo Fighters")
        self.importSongWithREST("One More Time", "Daft Punk")
        
        # Start our GUI
        self.gui = GUI()
        self.gui.startGUI(self)


    ########
    # Model Functions
    ########
    
    # Loads in the stored information from the current user object
    def loadUserInformation(self):
        self._audioList = self.currentUser.allAudioFiles
        self._playlists = self.currentUser.allPlaylists
        
        self.gui.updatePlaylistBox()
    

    # Saves all program information by updating the user object and serializing/saving to file
    def saveUserInformation(self):
        if (self.currentUser != None):
            self.currentUser.saveUser(self._audioList, self._playlists)
            self.gui.displayMessage("User saved as: " + self.currentUser.name)

        else:
            self.gui.displayMessage("You must first load or create a new user!")


    # Creates a new playlist and adds it the the master list of playlists
    def newPlaylist(self, name:str = None, songs:list = None):

        newPlaylist = Playlist(name)
        if (songs != None):
            for s in songs:
                newPlaylist.addAudio(s)

        self._playlists.append(newPlaylist)

        print("DEBUG: playlist created:" + newPlaylist.name)


    # Creates and adds a new custom song to the master playlist
    def newSong(self, response):
        if (response != None):
            newSong = Song(None, response[0])

            if (response[1] != ''):
                newSong.artist = Artist(response[1])

            if (response[2] != '' and int(response[2]) > 0 and int(response[2]) <= 5):
                newSong.rating = int(response[2])

            self.addAudioToMasterList(newSong)
            self.gui.focusMasterPlaylist()
            
        else:
            self.gui.displayMessage("Incorrect or Missing Song Information!")

    
    # Creates and adds a new custom podcast to the master playlist    
    def newPodcast(self, response):
        if (response != None):
            newPod = Podcast(None, response[0])

            if (response[1] != ''):
                newPod.episode = int(response[1])

            if (response[2] != '' and int(response[2]) > 0 and int(response[2]) <= 5):
                newPod.rating = int(response[2])

            self.addAudioToMasterList(newPod)
            self.gui.focusMasterPlaylist()
            
        else:
            self.gui.displayMessage("Incorrect or Missing Podcast Information!")
    

    # GET function to search for a playlist by name
    def getPlaylist(self, getN:str):
        for p in self._playlists:
            if (p.name == getN):
                return p

        raise NotFoundException("Playlist not found.")


    # GET function to search for an audio file by name and detail
    def getAudio(self, sName:str, detail = None):
        for s in self._audioList:
            if (s.name == sName):

                # No further details given
                if (detail == None):
                    return s
                
                # Further detailed info to check
                elif (type(s) is Song and s.artist.name == str(detail)):
                    return s
                elif (type(s) is Podcast and s.episode == int(detail)):
                    return s

        raise NotFoundException("Audio not found.")


    # Finds and deletes the passed in audio file
    def deleteAudio(self, audio:AudioFile):
        for p in self._playlists:
            for s in p.songList:
                if (s == audio):
                    p.songList.remove(s)
        
        self._audioList.remove(audio)
        self.gui.displayMessage("Song Deleted!")


    # Helper function to add an audio file to the master list
    def addAudioToMasterList(self, audio:AudioFile):
        self._audioList.append(audio)
        self.getPlaylist(self._masterPlaylistName).addAudio(audio)


    # Saves a playlist to an XML file
    def savePlaylistXML(self):
        root = ET.Element("root")
        
        for song in self.currentPlaylist.songList:

            song.addXML(root)

        print(ET.tostring(root, encoding='utf8').decode('utf8'))

        tree = ET.ElementTree(root)
        tree.write((self.currentPlaylist.name + ".xml"))

        self.gui.displayMessage("Playlist successfully exported!")


    # Loads a playlists XML file into the program
    def loadPlaylistXML(self, name):
        try:
            self.getPlaylist(name)
            self.gui.displayMessage("Playlist already created with that name.")

        except NotFoundException: #No playlist exists matching that name yet!
        
            playlistTree = ET.parse(name + ".xml")
            root = playlistTree.getroot()

            newPlaylist = Playlist(name)
            for child in root:

                try: #Song already exists
                    song = self.getAudio(child[0].text, child[2].text)

                    newPlaylist.addAudio(song)
                
                except NotFoundException: #Need to create and add the new song to masters list first
                    song = self.newSong([child[0].text, child[2].text, child[1].text])

                    self.addAudioToMasterList(song)
                
                    newPlaylist.addAudio(self.getAudio(child[0].text, child[2].text))

            self._playlists.append(newPlaylist)

            print("DEBUG: playlist created:" + newPlaylist.name)
            self.gui.updatePlaylistBox()
            self.gui.displayMessage("Playlist " + name + " successfully imported!")
            
    

    # Attempts to import a song with the lastfmConnection class
    # Last fm provides us with xml of the songs details, if it is found
    # Returns a status message to the GUI
    def importSongWithREST(self, songTitle, songArtist):
        try:
            c = LastFmConnection()

            details = c.getSongDetails(songTitle, songArtist)

        except LastFMException as e: # If lastfm returns a query error
            return ( "Error: LastFM error code " + str(e.code) )

        except GenericConnectionException: # If a connection exception occurs
            return ("Error: Unable to establish connection..")


        newSong = Song(details[0], details[1], Artist(details[2]))
        self.addAudioToMasterList(newSong)

        return ("Song successfully imported!")


    # A demonstration of using the suds python package for completing a SOAP request
    # This request gathers song lyrics from a separate SOAP api
    # There are not many lyrics available, so ive hard coded an ac/dc song which is in the api
    def demonstrationSOAP(self):
        self.gui.displayMessage("Running SOAP request...")

        client = Client('http://api.chartlyrics.com/apiv1.asmx?wsdl')
        result = client.service.SearchLyricDirect("AC/DC", "Thunderstruck")
        print (result)

        self.gui.displayMessage("Request complete, details printed in console.")


    ########
    # CLASS PROPERTIES AND PUBLIC VARIABLES
    ########

    @property
    def playlists(self):
        return self._playlists
    @playlists.setter
    def playlists(self, playlists:str):
        self._playlists = playlists

    @property
    def audioList(self):
        return self._playlists
    @audioList.setter
    def audioList(self, audioList:str):
        self._audioList = audioList
    
    @property
    def masterPlaylistName(self):
        return self._masterPlaylistName
    @masterPlaylistName.setter
    def masterPlaylistName(self, masterPlaylistName:str):
        self._masterPlaylistName = masterPlaylistName



# Start our program
mp = MusicPlayer()