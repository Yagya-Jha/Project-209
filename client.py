#-----------Bolierplate Code Start -----
import socket
from threading import Thread
from tkinter import *
from tkinter import ttk


PORT  = 8080
IP_ADDRESS = '127.0.0.1'
SERVER = None
BUFFER_SIZE = 4096


name = None
listbox =  None
textarea= None
labelchat = None
text_message = None

bgc="#490c5c"
fgc="pink"
bdc="#f73eba"


def openChatWindow():

    global bgc
    global fgc
    global bdc
    print("\n\t\t\t\tIP MESSENGER")

    #Client GUI starts here
    window=Tk()

    window.title('Music Sharing App')
    window.geometry("500x350")
    window.configure(bg=bgc)

    global name
    global listbox
    global textarea
    global labelchat
    global text_message
    global filePathLabel

    namelabel = Label(window, text= "Enter Your Name", font = ("Calibri",10), bg=fgc, highlightthickness=2, highlightbackground=bdc)
    namelabel.place(x=10, y=8)

    name = Entry(window,width =30,font = ("Calibri",10), bg=fgc)
    name.place(x=120,y=8)
    name.focus()

    connectserver = Button(window,text="Connect to Chat Server",bd=1, font = ("Calibri",10), command=connectToServer, bg=fgc)
    connectserver.place(x=350,y=6)

    separator = ttk.Separator(window, orient='horizontal')
    separator.place(x=0, y=35, relwidth=1, height=0.1)

    labelusers = Label(window, text= "Active Users", font = ("Calibri",10), bg=fgc, highlightthickness=2, highlightbackground=bdc)
    labelusers.place(x=10, y=50)

    listbox = Listbox(window,height = 5,width = 67,activestyle = 'dotbox', font = ("Calibri",10), bg=fgc, highlightthickness=2, highlightbackground=bdc)
    listbox.place(x=10, y=70)

    scrollbar1 = Scrollbar(listbox)
    scrollbar1.place(relheight = 1,relx = 1)
    scrollbar1.config(command = listbox.yview)

    connectButton=Button(window,text="Connect",bd=1, font = ("Calibri",10), bg=fgc)
    connectButton.place(x=282,y=160)

    disconnectButton=Button(window,text="Disconnect",bd=1, font = ("Calibri",10), bg=fgc)
    disconnectButton.place(x=350,y=160)

    refresh=Button(window,text="Refresh",bd=1, font = ("Calibri",10), command=showClientsList, bg=fgc)
    refresh.place(x=435,y=160)

    labelchat = Label(window, text="Chat Window", font=("Calibri",10), bg=fgc, highlightthickness=2, highlightbackground=bdc)
    labelchat.place(x=10,y=180)
  
    textarea = Text(window, width=67, height=6, font=("Calibri",10), bg=fgc, highlightthickness=2, highlightbackground=bdc)
    textarea.place(x=10,y=200)
    
    scrollbar2 = Scrollbar(textarea)
    scrollbar2.place(relheight = 1,relx = 1)
    scrollbar2.config(command = textarea.yview)

    text_message = Entry(window, width=45, font=("Calibri", 10), bg=fgc)
    text_message.pack()
    text_message.place(x=98, y=300)
    
    attach = Button(window, text = "Attach and Send", bd = 1, font=("Calibri", 10), bg=fgc)
    attach.place(x=10,y=300)

    file_path_label = Label(window, text="", fg="blue",font=("Calibri", 10), bg=fgc)
    file_path_label.place(x=10,y=300)

    snd_bttn = Button(window, text="Send",font=("Calibri", 10), bg=fgc)
    snd_bttn.place(x=430, y=300)
  
    window.mainloop()

#tiul-> This Is User List

def receiveMessage():
    global SERVER
    global BUFFER_SIZE
    global listbox
    global textarea

    while True:
        chunk = SERVER.recv(BUFFER_SIZE)
        try:
            if("tiul" in chunk.decode() and "1.0," not in chunk.decode()):
                print("HYE")
                letter_list = chunk.decode().split(",")
                listbox.insert(letter_list[0],letter_list[0]+":"+letter_list[1]+": "+letter_list[3]+" "+letter_list[5])
                print(letter_list[0],letter_list[0]+":"+letter_list[1]+": "+letter_list[3]+" "+letter_list[5])
                print(letter_list[1])
            else:
                print("BYE")
                textarea.insert(END,"\n"+chunk.decode('ascii'))
                textarea.see("end")
                print(chunk.decode('ascii'))
        except:
            pass


def showClientsList():
    global listbox
    listbox.delete(0,"end")
    SERVER.send("show list".encode('ascii'))

def connectToServer():
    global SERVER
    global name
    global sending_file

    cname = name.get()
    SERVER.send(cname.encode())


def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    t = Thread(target=receiveMessage)#thread
    t.start()
   
    openChatWindow()

setup()
