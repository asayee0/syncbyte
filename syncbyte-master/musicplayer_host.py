from __future__ import print_function
import os, pickle, socket, pygame
from tkinter.filedialog import askdirectory
from mutagen.id3 import ID3
from tkinter import *
from threading import Thread
import time

root = Tk()
root.title('SyncPlay Server')
root.minsize(300,300)
listofsongs = []
realnames = []
currsong=''
sip=''
c=''
addr=''
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
    pygame.mixer.music.play()
    return True

def updatelabel():
    global index
    v.set(realnames[index])
    return True

def listenForClient():
    # get the address of localhost
    host = socket.gethostbyname('localhost')
    port = 5555

    # set options to circumvent proper socket release
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # create pair for host address (this machine)
    host_addr = (host, port)
    s.bind(host_addr) # bind socket to aforementioned address

    # make socket at server listen for incoming inconnections
    s.listen(10)
    print('Starting to listen for requests')
    return True

def serverConnect():
    global s
    global c
    global addr
    c, addr = s.accept() # accept connection from client
    sendMusic(s,c,addr)
    
def sendMusic(s,c,addr):
    global currsong
    f = open(currsong,'rb') #open in binary //put back currsong variable 
    print('Got connection from ', addr)
    tosend=f.read()
    song_info["song_title"]=currsong
    song_info["song_data"]=tosend
    song_info["time_stamp"]=str(pygame.mixer.music.get_pos())
    pickled_info=pickle.dumps(song_info)
    c.sendall(pickled_info)    #send pickled_info
    time.sleep(7)
    c.send(bytes("done",'utf-8'))
    print('sending complete')

class Controls:

    def nextsong(event):
        global index
        global currsong
        global s
        global c
        global addr  
        index += 1
        if index>=len(listofsongs):
            index=0
        pygame.mixer.music.load(listofsongs[index])
        pygame.mixer.music.play()
        updatelabel()
        currsong=listofsongs[index]
        song_info["song_title"]=currsong
         
        sendMusic(s,c,addr)
        print(currsong)

    def prevsong(event):
        global index
        global currsong
        global s
        global c
        global addr  
        index -= 1
        if index<0:
            index=len(listofsongs)-1
        pygame.mixer.music.load(listofsongs[index])
        pygame.mixer.music.play()
        updatelabel()
        currsong=listofsongs[index]
        song_info["song_title"]=currsong
        sendMusic(s,c,addr)
        print (currsong)

    def stopsong(event):
        pygame.mixer.music.stop()
        v.set("")

    def pausesong(event):
        pygame.mixer.music.pause()
        updatelabel()

    def unpausesong(event):
        pygame.mixer.music.unpause()
        updatelabel()


def screenMain():
    global result
    label = Label(root,text='Playlist')
    label.pack()

    listbox = Listbox(root)
    listbox.pack()
    realnames.reverse()
    for items in realnames:
        listbox.insert(0,items)
    realnames.reverse()
    message = Label(root,text='Current Song')
    message.pack()
    songlabel.pack()

    nextbutton = Button(root,text = 'Next Song')
    previousbutton = Button(root,text = 'Previous Song')
    pausebutton = Button(root,text = 'Pause Song')
    unpausebutton = Button(root,text = 'Unpause Song')
    stopbutton = Button(root,text='Stop Music')
    exitbutton = Button(root, text='Exit')
    exitbutton.pack(side=BOTTOM)
    previousbutton.pack(side=LEFT)
    pausebutton.pack(side=LEFT)
    stopbutton.pack(side=LEFT)
    nextbutton.pack(side=RIGHT)
    unpausebutton.pack(side=RIGHT)


    nextbutton.bind("<Button-1>",Controls.nextsong)
    previousbutton.bind("<Button-1>",Controls.prevsong)
    pausebutton.bind("<Button-1>",Controls.pausesong)
    unpausebutton.bind("<Button-1>",Controls.unpausesong)
    stopbutton.bind("<Button-1>",Controls.stopsong)
    exitbutton.bind("<Button-1>", lambda event: exit())

    Thread(target = serverConnect, daemon=True).start()
    root.mainloop()

def main():
    listenForClient()
    directorychooser()
    updatelabel()
    screenMain()

if __name__ == "__main__":
    main()