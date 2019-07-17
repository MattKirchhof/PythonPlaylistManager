from Dialog import *
from Exceptions import *
from AudioFile import AudioFile, Song, Podcast
from Artist import Artist
from User import User

#External Packages
import tkinter as tk
from tkinter import simpledialog
from tkinter import StringVar
from tkinter.scrolledtext import ScrolledText
# To display album art pulled from RESTful request
from urllib.request import urlopen
from PIL import Image, ImageTk #Python Imaging Library
import requests
from io import BytesIO


# ------------------ GUI BUILD -------------------

class GUI():
    def startGUI(self, model):
        self._model = model
        self._GUI = tk.Tk() # The master GUI frame

        self._GUI.title("Playlist Manager!")
        self._GUI.geometry('860x420')


        # Menu Bar
        menu = tk.Menu(self._GUI)
        fileDropdown = tk.Menu(menu)
        fileDropdown.add_command(label='New Playlist',command=self.newPlaylistGUI)
        fileDropdown.add_command(label='New Song',command=self.newSongGUI)
        fileDropdown.add_command(label='New Podcast',command=self.newPodcastGUI)
        menu.add_cascade(label='File', menu=fileDropdown)

        importDropdown = tk.Menu(menu)
        importDropdown.add_command(label='Import Song From Web',command=self.importSongGUI)
        importDropdown.add_command(label='Import Playlist From File',command=self.importPlaylistGUI)
        importDropdown.add_command(label='Do SOAP Demo',command=self._model.demonstrationSOAP)
        menu.add_cascade(label='Import', menu=importDropdown)

        exportDropdown = tk.Menu(menu)
        exportDropdown.add_command(label='Export Song to File', command=self.saveXMLGUI)
        exportDropdown.add_command(label='Export Playlist to File', command=self.exportPlaylistGUI)
        menu.add_cascade(label='Export', menu=exportDropdown)

        helpDropdown = tk.Menu(menu)
        helpDropdown.add_command(label='About Us', command=self.aboutUsScreen)
        helpDropdown.add_command(label='Help', command=self.helpMenu)
        menu.add_cascade(label="Help", menu=helpDropdown)

        self._GUI.config(menu=menu)

        # Global font adjuster for more prettyness
        self._GUI.option_add("*Font", "roboto 11")

        # User login/logout Block
        self.logInFrame = tk.Frame(self._GUI)
        self.logInFrame.grid(column=0,row=0, columnspan=2, sticky='W', padx=(20,10), pady=(20,0))

        self.logInButton = tk.Button(self.logInFrame, text="Load User", command=self.loadUserGUI)
        self.logOutButton = tk.Button(self.logInFrame, text="Save User", command=self.saveUserGUI)
        
        self.nameString = StringVar()
        self.userInfo = tk.Label(self.logInFrame, textvariable=self.nameString, font="roboto 12 bold")
        self.nameString.set("No User Loaded..")

        self.logInButton.grid(column=0,row=0, padx=(5,5))
        self.logOutButton.grid(column=1,row=0, padx=(5,5))
        self.userInfo.grid(column=2,row=0, padx=(10,10))

        # Playlist Block
        self.playlistBox = tk.Listbox(self._GUI, width=30, height=12)
        self.playlistBox.configure(exportselection=False)
        for p in self._model.playlists:
            self.playlistBox.insert('end', p.name)
        
        self.playlistBox.bind('<<ListboxSelect>>', self.playlistSelected)
        self.playlistBox.grid(column=0,row=1, padx=(20,10), pady=(20,20))

        # Contents Block
        self.contentsBox = tk.Listbox(self._GUI, width=40, height=12)

        self.contentsBox.bind('<<ListboxSelect>>', self.songSelected)
        self.contentsBox.grid(column=1,row=1, padx=(10,0), pady=(20,20))

        self.scrollbar = tk.Scrollbar(self._GUI, orient='vertical')

        self.contentsBox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.contentsBox.yview)

        self.scrollbar.grid(column=2, row=1, sticky="ns", pady=(10,10) )

        #Buttons Block
        self.buttonFrame = tk.Frame(self._GUI, width=180, height=200)
        self.buttonFrame.grid(column=3,row=1, padx=(10,20), pady=(20,20))

        self.buttonChangeRate = tk.Button(self.buttonFrame, text="Change Audio Rating", command=self.changeRatingGUI)
        self.buttonChangeRate.grid(column=0,row=0, padx=(10,10), pady=(5,5))
        self.buttonAddAudio = tk.Button(self.buttonFrame, text="Add Audio To Playlist", command=self.addAudioGUI)
        self.buttonAddAudio.grid(column=0,row=1, padx=(10,10), pady=(5,5))
        self.buttonRemoveAudio = tk.Button(self.buttonFrame, text="Remove Audio From Playlist", command=self.removeAudioGUI)
        self.buttonRemoveAudio.grid(column=0,row=2, padx=(10,10), pady=(5,5))
        self.buttonDeletePlaylist = tk.Button(self.buttonFrame, text="Delete Playlist", command=self.deletePlaylistGUI)
        self.buttonDeletePlaylist.grid(column=0,row=3, padx=(10,10), pady=(5,5))
        self.buttonDeletePlaylist = tk.Button(self.buttonFrame, text="Delete Audio", command=self.deleteSongGUI)
        self.buttonDeletePlaylist.grid(column=0,row=4, padx=(10,10), pady=(5,5))

        #Song Info SubSection

        self.detailedSongInfoFrame = tk.Frame(self._GUI)
        self.detailedSongInfoFrame.grid(column=0,row=4, rowspan=2, sticky='W', padx=(10,10))

        self.albumArtCanv = tk.Canvas(self.detailedSongInfoFrame, width =64, heigh=64, bg = "white")
        self.albumArtCanv.grid(column = 0, row = 0, rowspan = 2, padx=(10,10), sticky='W')

        # Display the noArt.gif image in album art section
        img = tk.PhotoImage(file = 'noArt.gif')
        self.albumArt = self.albumArtCanv.create_image(32,32, image = img)

        # Adding in song detailed info
        self.songInfoNameString = StringVar()
        self.songInfoName = tk.Label(self.detailedSongInfoFrame, textvariable=self.songInfoNameString, font="roboto 12")
        self.songInfoNameString.set("test")

        self.songInfoArtistString = StringVar()
        self.songInfoArtist = tk.Label(self.detailedSongInfoFrame, textvariable=self.songInfoArtistString, font="roboto 12 bold")
        self.songInfoArtistString.set("test")
        
        self.songInfoName.grid(column=1,row=0, padx=(10,10), sticky="SW")
        self.songInfoArtist.grid(column=1,row=1, padx=(10,10), sticky = "W")

        self._GUI.mainloop()


    ######
    # Functional GUI methods (to change or update the GUIs current state)
    ######

    # Called when a new playlist selection occurs to update the chosen playlist
    def playlistSelected(self,event):
        print("DEBUG: PLAYLIST SELECTION CHANGE")

        try:
            pListName = event.widget.get(event.widget.curselection())

            self._model.currentPlaylist = self._model.getPlaylist(pListName)
            self.updateContentBox()

        except NotFoundException:
            self.displayMessage("Error selecting playlist.")

    

    # Gets the audio selected by the user and stores it in the global currentSong variable
    def songSelected(self, event):
        if (self._model.currentPlaylist != None):
            try:
                songName = event.widget.get(event.widget.curselection()).split("  |  ")
                songInfo = songName[1].split(" - ")
                print("DEBUG: Song selected: " + str(songInfo[0]))
                print("DEBUG: Artist or Episode: " + str(songInfo[1]))

                try:
                    self._model.currentSong = self._model.getAudio(songInfo[0], songInfo[1])
                    self.updateSongDetailBox()
                    
                except NotFoundException as e:
                    print(e)
                    self._model.currentSong = None
                    self.displayMessage("Error finding selected song.")

            # Nothing in the content box to select, or they have de-selected from the box
            except:
                self._model.currentSong = None

        else:
            self.contentsBox.selection_clear(0,'end')



    # Refreshes the contents of the box based on the current playlist
    def updateContentBox(self):
        print("DEBUG: Update Content")

        self._model.currentSong = None
        self.contentsBox.delete(0, 'end')
        self.updateSongDetailBox()

        # Populating our contents box
        for audio in self._model.currentPlaylist.songList:
            if (type(audio) is Song):
                self.contentsBox.insert('end', (self.getRatingString(audio) + audio.name + " - " + audio.artist.name))
            else:
                self.contentsBox.insert('end', (self.getRatingString(audio) + audio.name + " - " + str(audio.episode)))
    

    # Refreshes the contents of the playlist box based on your current list of playlists
    def updatePlaylistBox(self):
        self.playlistBox.delete(0,'end')
        for p in self._model.playlists:
            self.playlistBox.insert('end', p.name)



    # Updates the songs album art if available, as well as its name/artist info
    def updateSongDetailBox(self):
        global currAlbumImg # If the current album is not global, garbage collection collects it!

        if (self._model.currentSong != None):
            # Update art
            if (self._model.currentSong.imageURL != None):
                # LastFM gives images in PNG, therefore we need to convert it to a format TKinter understands
                response = requests.get(self._model.currentSong.imageURL)
                image_bytes = BytesIO(response.content)
                image_PIL = Image.open(image_bytes)
                currAlbumImg = ImageTk.PhotoImage(image_PIL)
                self.albumArtCanv.itemconfig(self.albumArt, image = currAlbumImg)
            else:
                # No art was provided
                currAlbumImg = tk.PhotoImage(file = 'noArt.gif')
                self.albumArtCanv.itemconfig(self.albumArt, image = currAlbumImg)
            
            # Update text
            self.songInfoNameString.set(self._model.currentSong.name)
            if (type(self._model.currentSong) is Song):
                self.songInfoArtistString.set(self._model.currentSong.artist.name)
            else:
                self.songInfoArtistString.set("Episode: " + str(self._model.currentSong.episode))

        else:
            # Nothing selected
            currAlbumImg = tk.PhotoImage(file = 'noArt.gif')
            self.albumArtCanv.itemconfig(self.albumArt, image = currAlbumImg)
            self.songInfoNameString.set("")
            self.songInfoArtistString.set("")


    # Sets focus on the main playlist containing all songs
    def focusMasterPlaylist(self):
        self._model.currentPlaylist = self._model.getPlaylist(self._model.masterPlaylistName)
        self.playlistBox.selection_clear(0,'end')
        self.playlistBox.selection_set(0)
        self._model.currentSong = None
        self.contentsBox.selection_clear(0,'end')
        self.updateContentBox()


    # Displays a message to the user
    def displayMessage(self, message:str):
        self._model.currentSong = None
        self._model.currentPlaylist = None
        self.playlistBox.selection_clear(0,'end')
        self.contentsBox.delete(0, 'end')
        self.contentsBox.insert('end', message)


    
    ######
    # Event GUI methods (which are called when a user clicks a button or wants to perform an explicit action)
    ######

    # Loads a serialized user object and populates the program with its contents, or creates a new user if no user file is found
    def loadUserGUI(self):
        dialog = LoadUserDialog(self._GUI)
        self._GUI.wait_window(dialog.top)

        if (dialog.response != None):
            self._model.currentUser = User(dialog.response[0])
            self.nameString.set("User: " + self._model.currentUser.name)

            if (self._model.currentUser.allAudioFiles != None):

                self._model.loadUserInformation()

                self.displayMessage("User Loaded")
            
            else:
                
                self.displayMessage("New User created")
            

    # Calls the model save method when save is pressed.
    def saveUserGUI(self):
        self._model.saveUserInformation()
        

    # Displays the dialog GUI to create a new playlist
    def newPlaylistGUI(self):
        name = simpledialog.askstring("New Playlist", "Playlist Name: ",
                                parent=self._GUI)
        if (name != None):
            self._model.newPlaylist(name)
            
            #update playlist box to contain new playlist
            self.updatePlaylistBox()
    

    # Displays the dialog GUI for creating new songs
    def newSongGUI(self):
        dialog = NewSongDialog(self._GUI)
        self._GUI.wait_window(dialog.top)

        self._model.newSong(dialog.response)
    

    # Displays the dialog GUI for creating new podcasts    
    def newPodcastGUI(self):
        dialog = NewPodcastDialog(self._GUI)
        self._GUI.wait_window(dialog.top)

        self._model.newPodcast(dialog.response)


    # Deletes the currently selected playlist
    def deletePlaylistGUI(self):
        print("DEBUG: Deleting playlist")
        if (self._model.currentPlaylist != None):
            if (self._model.currentPlaylist.name != self._model.masterPlaylistName):
                dialog = AreYouSureDialog(self._GUI)
                self._GUI.wait_window(dialog.top)

                if (dialog.response == True):
                    self._model.playlists.remove(self._model.currentPlaylist)
                    self._model.currentPlaylist = None
                    self.contentsBox.delete(0, 'end')

                    #update playlist box to remove deleted playlist
                    self.playlistBox.delete(0,'end')
                    for p in self._model.playlists:
                        self.playlistBox.insert('end', p.name)
        
            else:
                self.displayMessage("Do not delete the main song catalogue!")
        else:
            self.displayMessage("You must first select a playlist!")

    
    # Deletes the currently selected song from all playlists and the master audio list
    def deleteSongGUI(self):
        print("DEBUG: Deleting Song")
        if (self._model.currentSong != None):
            dialog = AreYouSureDialog(self._GUI)
            self._GUI.wait_window(dialog.top)

            if (dialog.response == True):
                self._model.deleteAudio(self._model.currentSong)

        else:
            self.displayMessage("You must first select a song!")
        

    # Displays the dialog GUI for adding a selected song to a playlist
    def addAudioGUI(self):
        if (self._model.currentSong != None and self._model.currentPlaylist != None):
            dialog = PlaylistDialog(self._GUI, self._model.playlists)
            self._GUI.wait_window(dialog.top)
            
            if (dialog.response == "Select a playlist"):
                pass # No playlist selected
            elif (dialog.response == None):
                pass # Cancelled
            else:
                chosenPL = self._model.getPlaylist(dialog.response)

                if (not chosenPL.containsSong(self._model.currentSong)):
                    chosenPL.addAudio(self._model.currentSong)
                    
                    index = self.playlistBox.get(0, "end").index(dialog.response)

                    self.playlistBox.selection_clear(0,'end')
                    self.playlistBox.selection_set(index)
                    self._model.currentPlaylist = chosenPL
                    self.updateContentBox()
                else:
                    self.displayMessage("This playlist already contains that song!")
        else:
            self.displayMessage("You must first select a song!")


    # Displays the dialog GUI for removing audio from a playlist
    def removeAudioGUI(self):
        if (self._model.currentPlaylist != None):
            if (self._model.currentPlaylist.name != self._model.masterPlaylistName):
                if (self._model.currentSong != None):
                    self._model.currentPlaylist.removeAudio(self._model.currentSong)
                    self._model.currentSong = None
                    self.updateContentBox()
            else:
                self.displayMessage("Cannot delete songs from the main song catalogue!")
        else:
            self.displayMessage("You must first select a playlist!")
            
    
    # Displays the dialog GUI for changing the rating of a song
    def changeRatingGUI(self):
        if (self._model.currentSong != None):
            rating = simpledialog.askinteger("Update Rating", "Please rate between 1 and 5: ",
                                    parent=self._GUI)
            if (rating != None):
                if (rating > 0 and rating <= 5):
                    self._model.currentSong.rating = rating
                    #update contents box to contain new rating
                    self.updateContentBox()
                else:
                    self.displayMessage("Rating not within bounds!")
        else:
            self.displayMessage("You must first select a song!")\

    
    # Calls the currently selected songs saveXML method
    def saveXMLGUI(self):
        if (self._model.currentSong != None):
            self._model.currentSong.saveXML()
            self.displayMessage(self._model.currentSong.name + " saved to XML..")

        else:
            self.displayMessage("You must first select a song!")


    # Displays the GUI to accept a song name and artist from the user
    # Accepts a return statement from the player function and displays it in the GUI
    def importSongGUI(self):
        dialog = ImportSongDialog(self._GUI)
        self._GUI.wait_window(dialog.top)
        
        resultResponse = self._model.importSongWithREST(dialog.response[0], dialog.response[1])

        self.displayMessage(resultResponse)


    # Accepts a playlist name and calls the model to attempt to import it
    def importPlaylistGUI(self):
        dialog = ImportPlaylistDialog(self._GUI)
        self._GUI.wait_window(dialog.top)

        if (dialog.response != None):
            self._model.loadPlaylistXML(dialog.response[0])
           

    # Calls the currently selected playlists XML method
    def exportPlaylistGUI(self):
        if (self._model.currentPlaylist != None):
            if (self._model.currentPlaylist.name != self._model.masterPlaylistName):
                
                self._model.savePlaylistXML()

            else:
                self.displayMessage("Please choose a custom playlist (not your entire song list) to export!")
        else:
            self.displayMessage("You must first select a playlist!")


    # Helper function to convert numerical rating to a string of stars
    def getRatingString(self, audio:AudioFile):
        ratingStr = ""
        for i in range (audio.rating):
            ratingStr = ratingStr + "*"
        for i in range (5 - audio.rating):
            ratingStr = ratingStr + " -"
        
        return ratingStr + "  |  "


    # Simply displays the help and about menues
    def helpMenu(self):
        dialog = HelpDialog(self._GUI)
        self._GUI.wait_window(dialog.top)

    def aboutUsScreen(self):
        dialog = AboutUsDialog(self._GUI)
        self._GUI.wait_window(dialog.top)