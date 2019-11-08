from __future__ import print_function
import os
from tkinter.filedialog import askdirectory

import socket 

import pygame
from mutagen.id3 import ID3
from tkinter import *

root = Tk()
root.minsize(300,300)


listofsongs = []
realnames = []
currsong=''
sip=''

v = StringVar()
songlabel = Label(root,textvariable=v,width=35)

index = 0

def serverConnect():
    
    
    
    # create a TCP socket for the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
    c, addr = s.accept() # accept connection from client
    sendMusic(s,c,addr)

def clientConnect():
    global sip
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
    host = socket.gethostbyname(sip) # Get local machine name (host to connect to)
    port = 5555               # Reserve a port for your service.


    server_addr = (host, port)
    s.connect(server_addr)
    print('connection to server successful')
    recvMusic(s)

    
def recvMusic(s):
    f = open('testsuccess.mp3','wb') # Open in binary

    while True:
        musfile=s.recv(4096) 
        if not musfile:
            break
        f.write(musfile)
    print('writing to file complete')
    f.close()
    
    
    s.close()               # Close the socket when done
    

def sendMusic(s,c,addr):
    global currsong
    f = open('testfile.mp3','rb') #open in binary //put back currsong variable
    #while True:
    print('here')
    
    print('Got connection from ', addr)
    tosend=f.read()
    c.sendall(tosend)
    print('sending complete')
    c.close() # close connection after processing

def connectToServer(event):
    sub=Toplevel(root)
    sub.title('server address')
    sub.minsize(300,100)
    Label(sub, text="Server IP").grid(row=0)
    e1 = Entry(sub)
    e1.grid(row=0, column=1)
    Button(sub,text='Connect',command=(lambda e=e1,s=sub:get_ip(e,s))).grid(row=3,column=0)
    Button(sub,text='Cancel',command=sub.destroy).grid(row=3,column=1)
   



def get_ip(e1,sub):
    global sip
    sip=e1.get()
    clientConnect()
    sub.destroy()
    
def createServer(event):
    sub=Toplevel(root)
    sub.title('server creation')
    sub.minsize(300,100)
    Button(sub,text='Create',command=(lambda s=sub:set_ip(s))).grid(row=2,column=0)
    Button(sub,text='Cancel',command=sub.destroy).grid(row=2,column=1)

def set_ip(sub):
    serverConnect()
    sub.destroy()

def directorychooser():

    directory = r'C:\Users\Marcus\Desktop\mmusicovernetworktest'
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
    pygame.mixer.music.play()
   

directorychooser()

def updatelabel():
    global index
    global songname
    v.set(realnames[index])
    #return songname

updatelabel()

def nextsong(event):
    global index
    global currsong
    index += 1
    if index>=len(listofsongs):
        index=0
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    updatelabel()
    currsong=listofsongs[index]
    print(currsong)

def prevsong(event):
    global index
    index -= 1
    if index<0:
        index=len(listofsongs)-1
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    updatelabel()
    currsong=listofsongs[index]
    print (currsong)


def stopsong(event):
    pygame.mixer.music.stop()
    v.set("")
    #return songname

def pausesong(event):
    pygame.mixer.music.pause()
    updatelabel()
    #return songname

def unpausesong(event):
    pygame.mixer.music.unpause()
    updatelabel()
    #return songname


label = Label(root,text='Music Player')
label.pack()

listbox = Listbox(root)
listbox.pack()

#listofsongs.reverse()
realnames.reverse()

for items in realnames:
    listbox.insert(0,items)

realnames.reverse()
#listofsongs.reverse()


nextbutton = Button(root,text = 'Next Song')
nextbutton.pack()

previousbutton = Button(root,text = 'Previous Song')
previousbutton.pack()

pausebutton = Button(root,text = 'Pause Song')
pausebutton.pack()

unpausebutton = Button(root,text = 'Unpause Song')
unpausebutton.pack()


stopbutton = Button(root,text='Stop Music')
stopbutton.pack()

clientbutton = Button(root,text='connect to server')
clientbutton.pack()

serverbutton = Button(root,text='create server')
serverbutton.pack()

nextbutton.bind("<Button-1>",nextsong)
previousbutton.bind("<Button-1>",prevsong)
pausebutton.bind("<Button-1>",pausesong)
unpausebutton.bind("<Button-1>",unpausesong)
stopbutton.bind("<Button-1>",stopsong)
clientbutton.bind("<Button-1>",connectToServer)
serverbutton.bind("<Button-1>",createServer)

songlabel.pack()


root.mainloop()