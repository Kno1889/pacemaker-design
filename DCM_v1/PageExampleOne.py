'''
PageExampleOne.py

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
 


class PageExampleOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #self.grid(row =0, column = 0, sticky="nsew")
        self.columnconfigure((1,4), weight=1)
        self.rowconfigure((0,1),weight=1)

        garbage = {"A":1, "B": 2, "C": "Banana"}
        
        label = tk.Label(self, text = 'Page Example One', font=settings.LARGE_FONT)
        label.grid(row=0, column=0)#pack(side="top", padx=10,pady=10)

        x = 1
        for key in garbage:
            dcm_data_label = tk.Label(self, text = '{} :'.format(key), font=settings.NORM_FONT)
            dcm_value_label = tk.Label(self, text = '{}'.format(garbage[key]), font=settings.NORM_FONT)
            dcm_data_label.grid(row=x, column=0, sticky="nsew")
            dcm_value_label.grid(row=x, column=1,sticky="nsew")
            x += 1

        button1 = ttk.Button(self, text="Back to Login", command= lambda: controller.show_frame(pages.Frames["Login"]))
        button1.grid(row=x+1, column = 2)#pack()