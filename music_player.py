"""
Music Player By Vaishali Kirtikumar Nile
IT second Year
197038
"""


import functools
from tkinter import *
import time
from pygame import mixer
from PIL import ImageTk, Image
import sqlite3
import threading
from tkinter import messagebox
import os
from mutagen.mp3 import MP3

mixer.init()

flag = False
lb = []
global paused
sr = 1
ind = -1
after_id = None

# base1
base1 = Tk()
base1.geometry("1570x700")
base1.title("Music Player(MP3) By VAISHALI NILE")
base1.configure(bg="black")

# image
canvas = Canvas(base1, width=300, height=170, bg="black")
canvas.place(x=250, y=150)
img = ImageTk.PhotoImage(Image.open('C:\\Users\\vaish\\Downloads\\music.png'))  # Change path of image
canvas.create_image(0, 0, anchor=NW, image=img)

# database connectivity to create data base
if os.path.isfile("songs.db") == False:
    db = sqlite3.connect("songs.db")
    messagebox.showinfo("TUTORIAL", "New to music player?..A Little Tutorial For Music Player")
    db.execute("create table music (sr_no numeric(10),path varchar(100),name varchar(100))")
    db.commit()
    db.close()
    # creating file count.txt
    file = open("count.txt", 'w')
    file.writelines(str(1))
    file.close()

    lb1 = Label(base1, text="Click here to add songs", fg="green", bg="black")
    lb1.place(x=150, y=330)

    canvas1 = Canvas(base1, width=30, height=30, bg="black")
    canvas1.place(x=200, y=350)
    img1 = ImageTk.PhotoImage(Image.open('C:\\Users\\vaish\\Downloads\\curved_arrow.png'))  # Change path of image
    canvas1.create_image(0, 0, anchor=NW, image=img1)
    flag = True

# reading data from file
file1 = open("count.txt", 'r')
i3 = file1.readlines()
i4 = str(i3)
file1.close()
s1 = i4.replace('(', '', 1)
s3 = s1.replace('[', '')
s4 = s3.replace(']', '')
s5 = s4.replace(',', '')
i = s5.replace('\'', '')


def playlist():
    # function to open new base to crate add songs to database
    global i
    # base2
    base2 = Tk()
    base2.geometry("650x550")
    base2.title("ADD PLAYLIST")
    base2.configure(bg="black")

    text1 = Text(base2, height=30, width=70)
    text1.setvar("COPY .MP3 MUSIC FILE AND PASTE HERE")
    text1.place(x=50, y=10)
    lb = Label(base2, text="COPY .MP3 MUSIC FILE AND PASTE HERE", fg="green")
    lb.place(x=380, y=460)

    def database(sr_no, path, nm):
        db2 = sqlite3.connect("songs.db")
        sr_no = int(sr_no)
        db2.execute(f"insert into music values({sr_no},'{path}','{nm}')")
        db2.commit()
        db2.close()

    def m1():
        global i
        data = text1.get(1.0, END)
        file = open("music_playlist.txt", 'w')
        file.writelines(data)
        file.close()
        file2 = open("music_playlist.txt", 'r')
        data2 = file2.readlines()

        for s in data2:
            d = s.rstrip('\n')
            n = str(d)

            sa3 = n.replace('[', '')
            sa4 = sa3.replace(']', '')
            sa5 = sa4.replace(',', '')
            sa6 = sa5.replace('\'', '')
            n1 = n[21:]

            database(i, sa6, n1)

            i = int(i)
            i = i + 1
            file3 = open("count.txt", 'w')
            file3.writelines(str(i))
            file3.close()

        messagebox.showinfo("Success", "Data Added To Playlist")
        if flag == True:
            lb2 = Label(base1, text="Click here to view playlist", fg="green", bg="black")
            lb2.place(x=500, y=330)
            can1 = Canvas(base1, width=30, height=30, bg="black")
            can1.place(x=550, y=350)
            im1 = PhotoImage(Image.open('C:\\Users\\vaish\\Downloads\\second_curved_arrow.png'))
            # Change path of image
            can1.create_image(0, 0, anchor=NW, image=im1)

    bt1 = Button(base2, text="ADD PLAYLIST", width=13, height=2, command=m1)

    bt1.place(x=300, y=500)


def volume(event):
    val1 = val.get()
    mixer.music.set_volume(val1 / 10)


def slide(x):
    global after_id
    if after_id is not None:
        sl_label.after_cancel(after_id)
        after_id = None

    time = (mixer.music.get_pos() / 1000)
    slider_bar.set(time)

    after_id = sl_label.after(1000, slide, None)


def play2(event, index):
    global ind
    global paused
    paused = False
    ind = index

    def play1():
        global paused
        if mixer.music.get_busy() == True:
            mixer.music.pause()
            img3 = ImageTk.PhotoImage(Image.open("C:\\Users\\vaish\\Downloads\\play.png"))  # Change path of image
            play_btn2.configure(image=img3)
            play_btn2.image = img3
            paused = True
        else:
            mixer.music.unpause()
            img3 = ImageTk.PhotoImage(Image.open("C:\\Users\\vaish\\Downloads\\pause.png"))  # Change path of image
            play_btn2.configure(image=img3)
            play_btn2.image = img3
            paused = False

    def next1():
        play2(index=ind + 1, event=None)

    def prev1():
        play2(index=ind - 1, event=None)

    im2 = PhotoImage(file="C:\\Users\\vaish\\Downloads\\pause.png")  # Change path of image
    play_btn2 = Button(base1, image=im2, command=play1)
    play_btn2.image = im2
    play_btn2.place(x=380, y=350)

    db5 = sqlite3.connect("songs.db")
    c = db5.cursor()
    ind = index
    nm = lb[ind].cget("text")
    nm = str(nm)
    nm = nm.replace('{', '')
    nm = nm.replace('}', '')
    c.execute(f"select path from music where name='{nm}'")
    path = c.fetchall()

    s = str(path)
    sa1 = s[1:]
    sa1=sa1.replace("(","",1)
    sa3 = sa1.replace('[', '')
    sa4 = sa3.replace(']', '')
    sa5 = sa4.replace(',', '')
    sa6 = sa5.replace('\'', '')
    sa7 = sa6[:-1]
    mixer.music.stop()
    mixer.music.load(sa7)
    i = 0
    while i < len(lb):
        lb[i].configure(bg="white")
        i = i + 1
    lb[ind].configure(bg="pink")
    mixer.music.play()

    def play_time():
        current_time = mixer.music.get_pos() / 1000
        current_time2 = time.strftime('%M:%S', time.gmtime(current_time))
        db5 = sqlite3.connect("songs.db")
        c = db5.cursor()
        nm = lb[ind].cget("text")
        nm = str(nm)
        nm = nm.replace('{', '')
        nm = nm.replace('}', '')
        c.execute(f"select path from music where name='{nm}'")
        path = c.fetchall()

        s = str(path)
        sa1 = s.replace('(', '', 1)
        sa3 = sa1.replace('[', '')
        sa4 = sa3.replace(']', '')
        sa5 = sa4.replace(',', '')
        sa6 = sa5.replace('\'', '')
        sa7 = sa6[:-1]
        current_song = sa7
        song_mut = MP3(current_song)
        length = song_mut.info.length
        current_time3 = time.strftime('%M:%S', time.gmtime(length))
        sl_label.configure(text=f"{current_time2}/{current_time3}")
        sl.configure(to=length)
        sl_label.after(1000, play_time)

    play_time()
    slide(None)

    def sec():
        while True:
            time.sleep(2)
            if mixer.music.get_busy() == 0:
                if paused is False:
                    next1()
                    break

    T = threading.Thread(target=sec)
    T.setDaemon(True)
    def sec1():
        T.start()

    sec1()

    previous_btn.configure(command=prev1)
    next_btn.configure(command=next1)


def assign():
    y1 = 50
    db3 = sqlite3.connect("songs.db")
    cu = db3.cursor()
    q = f"select name from music"
    cu.execute(q)
    name = cu.fetchall()
    i1 = 0
    if flag == True:
        lb3 = Label(base1, text="Click On Songs to play", fg="green", bg="black")
        lb3.place(x=650, y=30)
    for nm in name:
        lb.insert(i1, Label(base1, text=nm, fg="black", font=("Arial Bold", 10)))
        lb[i1].bind("<Button>", functools.partial(play2, index=i1))
        lb[i1].place(x=650, y=y1)
        y1 = y1 + 40
        i1 = i1 + 1


# for play button
def next():
    global sr
    sr = sr + 1
    db2 = sqlite3.connect("songs.db")
    cu2 = db2.cursor()
    cu2.execute(f"select path from music where sr_no={sr}")
    path = cu2.fetchone()
    db2.close()

    s = str(path)
    se1 = s[1:]
    se3 = se1.replace('[', '')
    se4 = se3.replace(']', '')
    se5 = se4.replace(',', '')
    se6 = se5.replace('\'', '')
    se7 = se6[:-1]
    mixer.music.load(se7)
    mixer.music.play()


def prev():
    global sr
    sr = sr - 1
    db2 = sqlite3.connect("songs.db")
    cu2 = db2.cursor()
    cu2.execute(f"select path from music where sr_no={sr}")
    path = cu2.fetchone()
    db2.close()
    s = str(path)

    sg1 = s[1:]
    sg3 = sg1.replace('[', '')
    sg4 = sg3.replace(']', '')
    sg5 = sg4.replace(',', '')
    sg6 = sg5.replace('\'', '')
    sg7 = sg6[:-1]
    mixer.music.load(sg7)
    mixer.music.play()


def play():
    paused = None
    db1 = sqlite3.connect("songs.db")
    cu = db1.cursor()
    cu.execute("select path from music")
    data3 = cu.fetchone()

    s = str(data3)
    sh1 = s[1:]
    sh2 = sh1[:-1]
    sh3 = sh2.strip(',')
    sh4 = sh3.strip('\'')
    s51 = sh4.strip('\n')
    n = str(s51)

    mixer.music.load(n)
    mixer.music.play()
    previous_btn.configure(command=prev)
    next_btn.configure(command=next)

    def play4():

        global paused

        if mixer.music.get_busy() == True:
            mixer.music.pause()
            img3 = ImageTk.PhotoImage(Image.open("C:\\Users\\vaish\\Downloads\\play.png"))  # Change path of image
            play_btn2.configure(image=img3)
            play_btn2.image = img3

        else:
            mixer.music.unpause()
            img3 = ImageTk.PhotoImage(Image.open("C:\\Users\\vaish\\Downloads\\pause.png"))  # Change path of image
            play_btn2.configure(image=img3)
            play_btn2.image = img3

    im2 = PhotoImage(file="C:\\Users\\vaish\\Downloads\\pause.png")  # Change path of image
    play_btn2 = Button(base1, image=im2, command=play4)
    play_btn2.image = im2
    play_btn2.place(x=380, y=350)

    db1.commit()
    db1.close()

T1= threading.Thread(target=play)
T1.setDaemon(True)
def play1():
    T1.start()


im = PhotoImage(file="C:\\Users\\vaish\\Downloads\\play.png")  # Change path of image
play_btn = Button(base1, image=im, command=play1)
play_btn.place(x=380, y=350)

im2 = PhotoImage(file="C:\\Users\\vaish\\Downloads\\next.png")  # Change path of image
next_btn = Button(base1, image=im2, command=next)
next_btn.place(x=460, y=350)

im4 = PhotoImage(file="C:\\Users\\vaish\\Downloads\\add_playlist.png")  # Change path of image
btn1 = Button(base1, image=im4, command=assign)
btn1.place(x=510, y=350)

im5 = PhotoImage(file="C:\\Users\\vaish\\Downloads\\add_songs.png")  # Change path of image
bt = Button(base1, image=im5, command=playlist)
bt.place(x=250, y=350)

im3 = PhotoImage(file="C:\\Users\\vaish\\Downloads\\prev.png")  # Change path of image
previous_btn = Button(base1, image=im3, command=prev)
previous_btn.place(x=300, y=350)

val = DoubleVar()
s = Scale(base1, from_=0, to=100, orient=VERTICAL, width=4, bg='black', fg='white', command=volume)
s['variable'] = val
s.set(5)
mixer.music.set_volume(0.5)
s.place(x=200, y=150)

slider_bar = DoubleVar()
sl = Scale(base1, from_=0, to=360, orient=HORIZONTAL, bg="black", command=slide, length=360)
sl['variable'] = slider_bar
sl.place(x=220, y=400)
sl_label = Label(base1, text="0", bg="white")
sl_label.place(x=220, y=400)

base1.mainloop()
