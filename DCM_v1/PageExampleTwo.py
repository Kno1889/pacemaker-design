'''
PageExampleTwo.py

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

 
class PageExampleTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = 'Page Example Two', font=settings.LARGE_FONT)
        label.grid(row=0)#pack(padx=10,pady=10)
        button1 = ttk.Button(self, text="Back to Login", command= lambda: controller.show_frame(pages.Frames["Login"]))
        button1.grid(row=0)#pack()

