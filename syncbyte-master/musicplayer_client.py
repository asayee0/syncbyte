from __future__ import print_function
import os, pickle, socket, pygame
from tkinter.filedialog import askdirectory
from mutagen.id3 import ID3
from tkinter import *
from threading import Thread
import time

root = Tk()
root.title('SyncPlay Client')
root.minsize(300,60)
listofsongs = []
realnames = []
currsong=''
sip=''
song_info={
    "song_data":'',
    "time_stamp":'',
    "song_title":''
}
v = StringVar()
songlabel = Label(root,textvariable=v,width=35)
index = 0

def directorychooser():
    global currsong
    directory = os.getcwd()
    directory=os.path.join(directory,'music')
    os.chdir(directory)
    for files in os.listdir(directory):
        if files.endswith(".mp3"):
            realdir = os.path.realpath(files)
            audio = ID3(realdir)
            realnames.append(audio['TIT2'].text[0])
            listofsongs.append(files)
    pygame.mixer.init()
    pygame.mixer.music.load(listofsongs[0])
    currsong=listofsongs[0]
    print(currsong)
    song_info["song_title"]=currsong
    return True

def updatelabel():
    global index
    v.set(realnames[index])
   
def clientConnect():
    global sip
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
    host = socket.gethostbyname(sip) # Get local machine name (host to connect to)
    port = 5555               # Reserve a port for your service.
    server_addr = (host, port)
    s.connect(server_addr)
    print('Connection to server successful')
    while True:
        try:
            recvMusic(s)
        except:
            print('Error in recvMusic(s)')
            time.sleep(7)
    
def recvMusic(s):
    data=b''
    has_file=False
    print('Receiving file')
    while True:
        musfile=s.recv(4096)
        try:
            if musfile.decode()=="done":
                has_file=True
                break
        except:
            pass
        data+=musfile
        if not musfile:  
            print('File received')
            break
    if(has_file):
        pickled_info = pickle.loads(data)
        f = open(pickled_info["song_title"]+'_sb.mp3','wb') # Open in binary
        f.write(pickled_info["song_data"])
        print('Writing to file complete')
        f.close()
        pygame.mixer.music.load(pickled_info["song_title"]+'_sb.mp3')
        pygame.mixer.music.play(loops=0,start=int(int(pickled_info["time_stamp"])/1000)+4)

def get_ip(e1,sub):
    global sip
    sip=e1.get()
    sub.destroy()
    clientConnect()

class Controls:
    def connectToServer(event = None):
        sub=Toplevel(root)
        sub.title('Enter server address')
        sub.minsize(300,100)
        Label(sub, text="Server IP").grid(row=0)
        e1 = Entry(sub)
        e1.grid(row=0, column=1)
        Button(sub,text='Connect',command=(lambda e=e1,s=sub:get_ip(e,s))).grid(row=3,column=1)
        Button(sub,text='Cancel',command=sub.destroy).grid(row=3,column=2)

def screenMain():
    connectButton = Button(root, text='Connect to server')
    exitbutton = Button(root, text='Exit')
    connectButton.pack()
    exitbutton.pack()
    connectButton.bind("<Button-1>", lambda event: Controls.connectToServer())
    exitbutton.bind("<Button-1>", lambda event: exit())
    Thread(target = Controls.connectToServer, daemon=True).start()
    root.mainloop()

def main():
    directorychooser()
    updatelabel()
    screenMain()

if __name__ == "__main__":
    main()