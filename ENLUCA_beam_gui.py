#######################################################################################################
####### This file will create a GUI for the input of beam angles to be used in the optimization. ######
######## The work is done by Mia Johanne Larsen (contact: mia@bel.no or +47 482 11 593) as work #######
################# in her masters thesis in biophysics at NTNU in the spring of 2025. ##################
#######################################################################################################

import tkinter as tk
from tkinter import *
from tkinter import Tk, Label, Button, Frame, X
from tkinter import ttk

def beam_gui():
    win = Tk()
    win.title('Enter beam angles')
    
    # Make labels for angles
    beam1 = Label(win, text="Angle, beam 1 (degrees)")
    beam1.grid(column=0, row=0)
    beam1.config(width=40, height=5)
    
    beam2 = Label(win, text="Angle, beam 2 (degrees)")
    beam2.grid(column=0, row=1)
    beam2.config(width=40, height=5)
    
    beam3 = Label(win, text="Angle, beam 3 (degrees)")
    beam3.grid(column=0, row=2)
    beam3.config(width=40, height=5)
    
    # Beam angle entry fields
    ba1_var = StringVar()
    box1 = Entry(win, textvariable=ba1_var)
    box1.grid(column=1, row=0)
    
    ba2_var = StringVar()
    box2 = Entry(win, textvariable=ba2_var)
    box2.grid(column=1, row=1)
    
    ba3_var = StringVar()
    box3 = Entry(win, textvariable=ba3_var)
    box3.grid(column=1, row=2)
    
    def Button_pressed():
        global ba1, ba2, ba3
    
        # Function to safely get a value from an Entry field
        def get_entry_value(entry):
            value = entry.get().strip()  # Get text input as string and strip spaces
            return float(value) if value else None  # Convert if non-empty

        # Retrieve values, checking if entry is empty
        ba1 = get_entry_value(box1)
        ba2 = get_entry_value(box2)
        ba3 = get_entry_value(box3)

        win.destroy()
        
    button = Button(win, text="Save", command=Button_pressed)
    button.grid(column=1, row=3)
    
    win.rowconfigure(3, minsize=50)
    win.columnconfigure(1, minsize=200)
    
    win.mainloop()
    
    return ba1, ba2, ba3