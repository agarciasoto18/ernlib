# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 13:33:56 2014

@author: enewton
"""

# one of the GUI packages, chosen b/c it was first to show up in google.
from Tkinter import *
import tkMessageBox
import tkFont
import random

# what to do when timer is pushed (time in milliseconds)
def start_timer(scale,message):
    global extent
    extent = 359.9
    draw_pacman(extent=extent)
    total_time = scale.get()*step
    start_ticking(total_time, message)
    #root.after(total_time+step, lambda:show_alert(message))

def start_ticking(total_time, message, time=0):
    increment = 359.9*step/total_time        
    if time<total_time:
        print stretch_pop.get(), float(time) % (5.*step)
        if stretch_pop.get() and time>0 and time<total_time-(5*step) and (time % (5.*step)) == 0: 
            show_alert("Stretch and look out the window")
        root.after(step, lambda: tick(increment,time=time,total_time=total_time,message=message))
    elif time == total_time:
        show_alert(message)
   
def tick(increment,time,total_time,message):
    global extent
    canvas.delete("all")
    extent = extent-increment
    draw_pacman(extent=extent)
    time += step
    start_ticking(total_time,message,time=time)
    

# what to do when timer is done    
def show_alert(message):
    root.bell()
    # pop up message box with (title, text)
    tkMessageBox.showinfo("Work Timer",message)
    #quit() # quit the GUI

# draw a wedge
def draw_pacman(start=90, extent=360):
    canvas.create_arc(center, start=start, extent=extent, 
                               fill="white")
    canvas.pack()
    
# pick a quote
def pick_quote(quotes, authors):
    tmp = random.randrange(len(quotes))
    quote = quotes[tmp]
    author = authors[tmp]
    myquote = quote + ' \n -- ' + author
    return myquote

root = Tk() # create a root window
root.title("Garden Variety Work Timer") # title the window

bigfont = tkFont.Font(family="Times", size=16)
smallfont = tkFont.Font(family="Times", size=12)

global center
global extent
global step

step = 60000 # for minutes 

# hard coded size in pixels (sorry)
cwidth=200
cheight=cwidth
canvas = Canvas(width=cwidth, height=cheight)
padding = cwidth*0.04

# make a label
clock_label = Label(root, text="Time Remaining", font=bigfont)
clock_label.pack() # put it on the GUI

# center of circle: 
#    (top left x position, top L y, bot R x, bot R y)
#    (0,0) is top left of box
center = padding, padding, cheight-padding, cwidth-padding
extent = 359.9
draw_pacman(extent=extent)
 
stretch_pop = IntVar()
stretch = Checkbutton(root,text="Pop up for stretch breaks?", variable=stretch_pop)
stretch.pack()
stretch_pop.set(1)


#####
# The Work Section
#####

# a frame for the scales and buttons
work_frame = Frame(width=cwidth, height=cwidth*0.25)
work_frame.pack(padx=padding, pady=padding)

work_label = Label(work_frame, text="Work length (minutes)", font=smallfont)
work_label.pack()

# make a scale bar
work_time = Scale(work_frame, from_=1, to=60, 
                  orient=HORIZONTAL, relief=FLAT, length=cwidth)
work_time.pack(padx=padding, pady=padding/2.) 
work_time.set(25)

# make a button, with text on it, and give it something to do
#    activebg,fg for hover colors
work_start = Button(work_frame, text="Start work", font=bigfont,
                    command= lambda: start_timer(work_time,"Take a break!"),
                    bg='white', fg='red', relief=GROOVE,
                    activebackground='gray', activeforeground='red')
work_start.pack()


#####
# The Break Section
#####

quotes = ["What have wealth or grandeur to do with happiness?", 
"There is nothing like staying at home, for real comfort.",
"I cannot fix on the hour, or the spot, or the look or the words, which laid the foundation. It is too long ago. I was in the middle before I knew that I had begun.",
"Vanity and pride are different things, though the words are often used synonymously. A person may be proud without being vain. Pride relates more to our opinion of ourselves, vanity to what we would have others think of us.",
"Friendship is certainly the finest balm for the pangs of disappointed love"]
authors = ["Jane Austen", "Jane Austen", "Jane Austen", "Jane Austen", "Jane Austen"]

break_frame = Frame(width=cwidth, height=cwidth*0.25)
break_frame.pack(padx=padding, pady=padding/2.)

break_label = Label(break_frame, text="Break length (minutes)", font=smallfont)
break_label.pack()

break_time = Scale(break_frame, from_=1, to=10, font=smallfont,
                   orient=HORIZONTAL, length=cwidth)
break_time.pack(padx=padding)
break_time.set(3)

break_start = Button(break_frame, text="Start break", font=bigfont,
                     command= lambda: start_timer(break_time,pick_quote(quotes, authors)),
                     bg='white', fg='blue', relief=GROOVE,
                     activebackground='gray', activeforeground='blue')
break_start.pack()

# run the GUI
root.mainloop()