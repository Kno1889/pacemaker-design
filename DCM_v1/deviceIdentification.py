'''
deviceIdentification.py

Version: 0.3
Created By: Elston A.
Date Modified: Oct 21, 2020

Description: deviceIdentification is used to contain the class which specifies the Tkinter 
frame shown when trying to identify a pacemaker.
'''

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as tm

import pages
import settings
import pacemaker

'''
Class: DeviceIdentification

Description:
Tkinter class that defines the window where a user defines the ID of the pacemaker.
The pacemaker must have an ID which is an integer. 
'''
class DeviceIdentification(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # self.rowconfigure(1,weight=1)
        self.columnconfigure((0), weight=1)
        # self.rowconfigure(0,weight=1)
        self.parent = parent
        self.controller = controller

        # Changes to be made:
        # have a connect button
        # Have a quit button

        # Widgets
        label = tk.Label(self, text='Identification Window', font=settings.LARGE_FONT)
        id_label = ttk.Label(self, text="Device ID", font=settings.NORM_FONT)
        b1 = ttk.Button(self, text="Connect",command=lambda: self.dev_ID_register(id))
        id = ttk.Entry(self)
        
        # Widget Placement
        id_label.grid(row=1, column=0, sticky="n", pady=10)
        label.grid(row=0, column=0, sticky="n", pady=10, padx=240)
        id.grid(row=2, column=0, sticky="n")        
        b1.grid(row=3, column=0, sticky="n", pady=30)  # pack()

    # dev id registration handler
    def dev_ID_register(self, dev_id):
        # validation on ID input. Make sure only numbers!
        def is_int(var):
            try:
                int(var)
                return True
            except:
                return False

        # Ensure that the ID is not empty
        if dev_id.get() == None or dev_id.get() == "":
            tm.showinfo(
                "Warn", "There is no device id given. Please enter a device ID.")
            return False
        if is_int(dev_id.get()) == False:
            tm.showerror("Error", "You did not provide a valid ID")
            return False

        # Check if this pacemaker has been identified before
        last_connected = pacemaker.connect(int(dev_id.get()))
        # Ensure to warn the user that a new pacemaker has been connected 
        if last_connected != True:
            tm.showwarning("New ID", settings.newIdErr)

        # clear field
        dev_id.delete(0, tk.END)
        dev_id.insert(0, "")

        # Go back to login page
        self.controller.show_frame(pages.Frames["Login"])

        # allow users to be created
        self.controller.user_menu.entryconfigure(0, state=tk.NORMAL)
        return True
