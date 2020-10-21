'''
deviceIdentification.py

Version: 0.1
Created By: Elston A.
Date Modified: Oct 21, 2020

Docstrings
'''

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as tm

import pages
import settings
import pacemaker


def dev_ID_proc(controller, dev_id):
    # done some things
    last_connected  = pacemaker.connect(dev_id) # this is weird   # pacemaker.connect(dev_id) returns true if dev_id was connected last, else returns false
    if last_connected != dev_id:
        tm.showwarning("New ID", settings.newIdErr)
    controller.show_frame(pages.Frames["Monitor"])
    return True

def logout(controller):
    # some function
    controller.show_frame(pages.Frames["Login"])

class DeviceIdentification(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = 'Identification Window', font=settings.LARGE_FONT)
        label.grid(row=0)#pack(padx=10,pady=10)

        id_label = ttk.Label(self, text = "Device ID", font=settings.LARGE_FONT )
        id_label.grid(row=1)

        id = ttk.Entry(self)
        id.grid(row=2)

        b1 = ttk.Button(self, text="Okay", command= lambda: dev_ID_proc(controller, id.get()))
        b1.grid(row=3)#pack()

        b1 = ttk.Button(self, text="Logout", command= lambda: logout(controller))
        b1.grid(row=4)#pack()


