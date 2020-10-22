'''
monitor.py

Version: 0.1
Created By: Elston A.
Date Modified: Oct 21, 2020

Docstrings
'''


import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as tm

import users
import modes

import pages
import settings

chosen_mode = None


def exit_session(controller):
    users.signOutUser(users.currentUserInfo()[0])
    controller.show_frame(pages.Frames["DevID"])


def set_mode(controller, mode):
    mode_selected = mode.get()

    if mode_selected != "Choose":
        modes.setCurrentMode(mode_selected)
        controller.show_frame(pages.Frames["Monitor"])

class DefMode(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #self.grid(row =0, column = 0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        #self.rowconfigure((0,1),weight=1)

        page_title = tk.Label(self, text="Mode Selection", font=settings.LARGE_FONT)
        page_title.grid(row=0, column=1, ipadx=100, ipady=50, columnspan=2) #(side="top", pady=10, padx=10)

        mode_label = tk.Label(self, text="Mode: ", font=settings.NORM_FONT)
        mode_label.grid(row=1, column=1)# pack()

        mode_options = [mode.name for mode in modes.allModes()]
        # default text
        mode_options.insert(0, "Choose")


        choice = tk.StringVar(self)
        choice.set(mode_options[0])

        dropdown = ttk.OptionMenu(self, choice, *mode_options)
        dropdown.grid(row = 1, column=2)

        button2 = ttk.Button(self, text="Set", command= lambda: set_mode(controller, choice))
        button2.grid(row=3, column = 2)#pack()

        button1 = ttk.Button(self, text="Exit Session", command= lambda: exit_session(controller))
        button1.grid(row=4, column = 2)#pack()



class Monitor(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #self.grid(row =0, column = 0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        #self.rowconfigure((0,weight=1)

        self.mode = [] if modes.getCurrentMode() is None else modes.getCurrentMode()

        for params in self.mode:
            print(params)

        print(self.mode)

        garbage = {"A":1, "B": 2, "C": "Banana"}
        
        label = tk.Label(self, text = 'DCM', font=settings.LARGE_FONT)
        label.grid(row=0, column=0)#pack(side="top", padx=10,pady=10)

        #controller.after(2000, self.probe_data())

        print(chosen_mode)

        x = 1
        for key in garbage:
            dcm_data_label = tk.Label(self, text = '{} :'.format(key), font=settings.NORM_FONT)
            dcm_value_label = tk.Label(self, text = '{}'.format(garbage[key]), font=settings.NORM_FONT)
            dcm_data_label.grid(row=x, column=0, sticky="nsew")
            dcm_value_label.grid(row=x, column=1,sticky="nsew")
            x += 1

        button1 = ttk.Button(self, text="Exit Session", command= lambda: exit_session(controller))
        button1.grid(row=x+1, column = 2)#pack()
        
    def probe_data(self):
        # Only update if there is no data
        if self.mode == []:
            self.mode = [] if modes.getCurrentMode() is None else modes.getCurrentMode()
