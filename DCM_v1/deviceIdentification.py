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


class DeviceIdentification(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # self.rowconfigure(1,weight=1)
        self.columnconfigure((0), weight=1)
        # self.rowconfigure(0,weight=1)
        self.parent = parent
        self.controller = controller

        label = tk.Label(self, text='Identification Window',
                         font=settings.LARGE_FONT)
        label.grid(row=0, column=0, sticky="n", pady=10,
                   padx=240)  # pack(padx=10,pady=10)

        id_label = ttk.Label(self, text="Device ID", font=settings.NORM_FONT)
        id_label.grid(row=1, column=0, sticky="n", pady=10)

        id = ttk.Entry(self)
        id.grid(row=2, column=0, sticky="n")

        b1 = ttk.Button(self, text="Connect",
                        command=lambda: self.dev_ID_register(id))
        b1.grid(row=3, column=0, sticky="n", pady=30)  # pack()

    # dev id
    def dev_ID_register(self, dev_id):

        def is_int(var):
            try:
                int(var)
                return True
            except:
                return False

        if dev_id.get() == None or dev_id.get() == "":
            tm.showinfo(
                "Warn", "There is no device id given. Please enter a device ID.")
            return False
        if is_int(dev_id.get()) == False:
            tm.showerror("Error", "You did not provide a valid ID")
            return False

        # probs device id should be string: 1-AA2-DD2
        last_connected = pacemaker.connect(int(dev_id.get()))
        if last_connected != True:
            tm.showwarning("New ID", settings.newIdErr)

        # clear field
        dev_id.delete(0, tk.END)
        dev_id.insert(0, "")

        self.controller.show_frame(pages.Frames["Login"])

        # allow users to be created
        self.controller.user_menu.entryconfigure(0, state=tk.NORMAL)
        return True
