import tkinter as tk
from Playlist import Playlist

class PlaylistDialog:

    def __init__(self, parent, pl):
        self.response = None

        top = self.top = tk.Toplevel(parent)
        top.protocol("WM_DELETE_WINDOW", self.cancel)
        top.focus_force()
        self.mainLabel = tk.Label(top, text='Choose the playlist below', font='roboto 12 bold')
        self.mainLabel.pack()

        #prep our playlists to choose from
        playlists = ["Select a playlist"]
        for p in pl:
            playlists.append(p.name)

        #define a variable to store current selection
        self.choice = tk.StringVar(top)
        self.choice.set(playlists[0])

        #make the dropdown menu
        self.playlistChoices = tk.OptionMenu(top, self.choice, *playlists)
        self.playlistChoices.pack(padx=(30,30), pady=(20,20))

        self.buttonFrame = tk.Frame(top)

        self.mySubmitButton = tk.Button(self.buttonFrame, text='Accept', command=self.send)
        self.mySubmitButton.grid(row=0, column=0, padx=(10,10), pady=(10,10))
        self.myCancelButton = tk.Button(self.buttonFrame, text='Cancel', command=self.cancel)
        self.myCancelButton.grid(row=0, column=1, padx=(10,10), pady=(10,10))

        self.buttonFrame.pack(padx=(10,10), pady=(10,10))

    def send(self):
        self.response = self.choice.get()
        self.top.destroy()

    def cancel(self):
        self.response = None
        self.top.destroy()


class NewSongDialog:

    def __init__(self, parent):
        self.response = None

        top = self.top = tk.Toplevel(parent)
        top.protocol("WM_DELETE_WINDOW", self.cancel)
        top.focus_force()
        self.mainLabel = tk.Label(top, text='Enter custom song information below:', font='roboto 12 bold')
        self.mainLabel.grid(row=0)

        tk.Label(top, text="*Song Name: ").grid(row=1)
        tk.Label(top, text="Song Artist: ").grid(row=2)
        tk.Label(top, text="Song Rating (0-5): ").grid(row=3)

        self.input1 = tk.Entry(top)
        self.input2 = tk.Entry(top)        
        self.input3 = tk.Entry(top)


        self.input1.grid(row=1, column=1, padx=(7,7), pady=(7,7))
        self.input2.grid(row=2, column=1, padx=(7,7), pady=(7,7))
        self.input3.grid(row=3, column=1, padx=(7,7), pady=(7,7))

        self.mySubmitButton = tk.Button(top, text='Accept', command=self.send)
        self.mySubmitButton.grid(row=5, column=0, padx=(10,10), pady=(10,10))
        self.myCancelButton = tk.Button(top, text='Cancel', command=self.cancel)
        self.myCancelButton.grid(row=5, column=1, padx=(10,10), pady=(10,10))

        self.detailLabel = tk.Label(top, text='It is suggested you use the Import > Song method if internet is available.', font='roboto 9')
        self.detailLabel.grid(row=6, columnspan=2)

    def send(self):
        if (self.input1.get() == ''):
            self.response = None
        else:
            self.response = [self.input1.get(), self.input2.get(), self.input3.get()]

        self.top.destroy()

    def cancel(self):
        self.response = None
        self.top.destroy()


class NewPodcastDialog:

    def __init__(self, parent):
        self.response = None

        top = self.top = tk.Toplevel(parent)
        top.protocol("WM_DELETE_WINDOW", self.cancel)
        top.focus_force()
        self.mainLabel = tk.Label(top, text='Enter Podcast information below:', font='roboto 12 bold')
        self.mainLabel.grid(row=0)

        tk.Label(top, text="*Podcast Name: ").grid(row=1)
        tk.Label(top, text="Podcast Episode Number: ").grid(row=2)
        tk.Label(top, text="Podcast Rating (0-5): ").grid(row=3)

        self.input1 = tk.Entry(top)
        self.input2 = tk.Entry(top)
        self.input3 = tk.Entry(top)        


        self.input1.grid(row=1, column=1, padx=(7,7), pady=(7,7))
        self.input2.grid(row=2, column=1, padx=(7,7), pady=(7,7))
        self.input3.grid(row=3, column=1, padx=(7,7), pady=(7,7))

        self.mySubmitButton = tk.Button(top, text='Accept', command=self.send)
        self.mySubmitButton.grid(row=5, column=0, padx=(10,10), pady=(10,10))
        self.myCancelButton = tk.Button(top, text='Cancel', command=self.cancel)
        self.myCancelButton.grid(row=5, column=1, padx=(10,10), pady=(10,10))


    def send(self):
        if (self.input1.get() == ''):
            self.response = None
        else:
            self.response = [self.input1.get(), self.input2.get(), self.input3.get()]
            
        self.top.destroy()

    def cancel(self):
        self.response = None
        self.top.destroy()


class LoadUserDialog:

    def __init__(self, parent):
        self.response = None

        top = self.top = tk.Toplevel(parent)
        top.protocol("WM_DELETE_WINDOW", self.cancel)
        top.focus_force()
        self.mainLabel = tk.Label(top, text='Enter your user name below:', font='roboto 12 bold')
        self.mainLabel.grid(row=0)

        tk.Label(top, text="*User Name: ").grid(row=1)
        self.input1 = tk.Entry(top)
        self.input1.grid(row=1, column=1, padx=(10,10), pady=(10,10))

        self.mySubmitButton = tk.Button(top, text='Load/Create User', command=self.send)
        self.mySubmitButton.grid(row=5, column=0, padx=(10,10), pady=(10,10))
        self.myCancelButton = tk.Button(top, text='Cancel', command=self.cancel)
        self.myCancelButton.grid(row=5, column=1, padx=(10,10), pady=(10,10))

    def send(self):
        if (self.input1.get() == ''):
            self.response = None
        else:
            self.response = [self.input1.get()]

        self.top.destroy()

    def cancel(self):
        self.response = None
        self.top.destroy()


class ImportPlaylistDialog:

    def __init__(self, parent):
        self.response = None

        top = self.top = tk.Toplevel(parent)
        top.protocol("WM_DELETE_WINDOW", self.cancel)
        top.focus_force()
        self.mainLabel = tk.Label(top, text='Enter the playlist name below:', font='roboto 12 bold')
        self.mainLabel.grid(row=0)

        tk.Label(top, text="*Playlist Name: ").grid(row=1)
        self.input1 = tk.Entry(top)
        self.input1.grid(row=1, column=1, padx=(10,10), pady=(10,10))

        self.mySubmitButton = tk.Button(top, text='Load/Create Playlist', command=self.send)
        self.mySubmitButton.grid(row=5, column=0, padx=(10,10), pady=(10,10))
        self.myCancelButton = tk.Button(top, text='Cancel', command=self.cancel)
        self.myCancelButton.grid(row=5, column=1, padx=(10,10), pady=(10,10))

    def send(self):
        if (self.input1.get() == ''):
            self.response = None
        else:
            self.response = [self.input1.get()]

        self.top.destroy()

    def cancel(self):
        self.response = None
        self.top.destroy()



class ImportSongDialog:

    def __init__(self, parent):
        self.response = None

        top = self.top = tk.Toplevel(parent)
        top.protocol("WM_DELETE_WINDOW", self.cancel)
        top.focus_force()
        self.mainLabel = tk.Label(top, text='Enter your song title below:', font='roboto 12 bold')
        self.mainLabel.grid(row=0)

        tk.Label(top, text="*Song Title: ").grid(row=1)
        self.input1 = tk.Entry(top)
        self.input1.grid(row=1, column=1, padx=(10,10), pady=(10,10))
        
        tk.Label(top, text="*Song Artist: ").grid(row=2)
        self.input2 = tk.Entry(top)
        self.input2.grid(row=2, column=1, padx=(10,10), pady=(10,10))

        self.mySubmitButton = tk.Button(top, text='Search for and Import Song', command=self.send)
        self.mySubmitButton.grid(row=5, column=0, padx=(10,10), pady=(10,10))
        self.myCancelButton = tk.Button(top, text='Cancel', command=self.cancel)
        self.myCancelButton.grid(row=5, column=1, padx=(10,10), pady=(10,10))

        self.detailLabel = tk.Label(top, text='This attempts to find the song title from the last.fm API and import it into your songlist!', font='roboto 9')
        self.detailLabel.grid(row=6, columnspan=2)

    def send(self):
        if (self.input1.get() == '' or self.input2.get() == ''):
            self.response = None
        else:
            self.response = [self.input1.get(), self.input2.get()]

        self.top.destroy()

    def cancel(self):
        self.response = None
        self.top.destroy()


class AreYouSureDialog:

    def __init__(self, parent):
        self.response = None

        top = self.top = tk.Toplevel(parent)
        top.protocol("WM_DELETE_WINDOW", self.cancel)
        top.focus_force()
        self.mainLabel = tk.Label(top, text='Are you sure:', font='roboto 12 bold')
        self.mainLabel.grid(row=0, column=0, columnspan=2, padx=(10,10), pady=(10,10))


        self.mySubmitButton = tk.Button(top, text='Yes!', command=self.send)
        self.mySubmitButton.grid(row=1, column=0, padx=(20,10), pady=(10,10))
        self.myCancelButton = tk.Button(top, text='No.', command=self.cancel)
        self.myCancelButton.grid(row=1, column=1, padx=(10,20), pady=(10,10))


    def send(self):
        self.response = True
        self.top.destroy()

    def cancel(self):
        self.response = False
        self.top.destroy()


class AboutUsDialog:

    def __init__(self, parent):

        top = self.top = tk.Toplevel(parent)
        top.protocol("WM_DELETE_WINDOW", self.cancel)
        top.focus_force()
        self.title = tk.Label(top, text='MusicPlayer^tm', font='roboto 12 bold')
        self.info1 = tk.Label(top, text='We are a small independent student at the university of Guelph.', font='roboto 10')
        self.info2 = tk.Label(top, text='We developed this music player in an effort to save the environment.', font='roboto 10')
        self.info3 = tk.Label(top, text='Please view the Help menu for information about the program!', font='roboto 10')
        self.title.grid(row=0, column=0, padx=(10,10), pady=(10,10))
        self.info1.grid(row=1, column=0, padx=(10,10), pady=(10,10))
        self.info2.grid(row=2, column=0, padx=(10,10), pady=(10,10))
        self.info3.grid(row=3, column=0, padx=(10,10), pady=(10,10))

        self.mySubmitButton = tk.Button(top, text='Cool!', command=self.cancel)
        self.mySubmitButton.grid(row=4, column=0, padx=(20,10), pady=(10,10))

    def cancel(self):
        self.top.destroy()

class HelpDialog:

    def __init__(self, parent):

        top = self.top = tk.Toplevel(parent)
        top.protocol("WM_DELETE_WINDOW", self.cancel)
        top.focus_force()
        self.title = tk.Label(top, text='How to use the program..', font='roboto 12 bold')
        self.info1 = tk.Label(top, text='This program is a simple playlist manager program. Inside of it, you can create,', font='roboto 10')
        self.info2 = tk.Label(top, text='manage and share playlists of your favourite tunes. This program is not meant to', font='roboto 10')
        self.info3 = tk.Label(top, text='play your music, but instead it stores information about any song in the world.', font='roboto 10')
        self.info4 = tk.Label(top, text='All you need to do is search for the song with our easy to use song importing system,', font='roboto 10')
        self.info5 = tk.Label(top, text='or create a new song yourself. Then add and remove them from your playlists as you please!', font='roboto 10')
        self.title.grid(row=0, column=0, padx=(10,10), pady=(10,10))
        self.info1.grid(row=1, column=0, padx=(10,10), pady=(1,1))
        self.info2.grid(row=2, column=0, padx=(10,10), pady=(1,1))
        self.info3.grid(row=3, column=0, padx=(10,10), pady=(1,1))
        self.info4.grid(row=4, column=0, padx=(10,10), pady=(1,1))
        self.info5.grid(row=5, column=0, padx=(10,10), pady=(1,1))

        self.mySubmitButton = tk.Button(top, text='Lets try it out!', command=self.cancel)
        self.mySubmitButton.grid(row=6, column=0, padx=(20,10), pady=(10,10))

    def cancel(self):
        self.top.destroy()