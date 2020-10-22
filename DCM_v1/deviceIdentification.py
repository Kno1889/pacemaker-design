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
    if dev_id == None or dev_id == "":
        tm.showinfo("Warn", "There is no device id given. Please enter a device ID.")
    last_connected  = pacemaker.connect(int(dev_id.get()))  # probs device id should be string: 1-AA2-DD2 
    if last_connected != True:
        tm.showwarning("New ID", settings.newIdErr)
    controller.show_frame(pages.Frames["Login"])
    return True


class DeviceIdentification(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #self.rowconfigure(1,weight=1)
        self.columnconfigure( (0,5),weight=1, minsize=20)
        self.rowconfigure( (0,5),weight=1, minsize=20)

        label = tk.Label(self, text = 'Identification Window', font=settings.LARGE_FONT)
        label.grid(row=0, sticky="nsew", padx=550, pady=10)#pack(padx=10,pady=10)
        

        id_label = ttk.Label(self, text = "Device ID", font=settings.NORM_FONT )
        id_label.grid(row=1, sticky="nswe", pady=10)

        id = ttk.Entry(self)
        id.grid(row=2, sticky="nswe")

        b1 = ttk.Button(self, text="Connect", command= lambda: dev_ID_proc(controller, id))
        b1.grid(row=3, sticky="nsew", pady=30)#pack()


