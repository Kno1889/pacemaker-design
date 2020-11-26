'''
loginPage.py

Version: 0.3
Created By: Elston A.
Date Modified: Oct 21, 2020

Description: Contains the Tkinter class for the Login Page Window
'''

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as tm

# potentially make this import cleaner, maybe make special file for making users etc.
import users

import settings
import pages


'''
Class: LoginPage

Description:
The class that defines the Tkinter Frame for the login screen.
'''
class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, master = parent)
        self.grid_columnconfigure((0,2),weight=2)
        self.grid_columnconfigure((0,1),weight=1)

        self.parent = parent
        self.controller = controller

        # Page Widgets
        page_title = tk.Label(self, text="Login Page", font=settings.LARGE_FONT)
        uname_l =    tk.Label(self, text="Username: ", font=settings.NORM_FONT)
        pwd_l =      tk.Label(self, text="Password: ", font=settings.NORM_FONT)

        uname_e = ttk.Entry(self)
        pwd_e =   ttk.Entry(self, show="*")

        login_b = ttk.Button(self, text="Login", command= lambda: self.authenticate(uname_e, pwd_e))
        back_b =  ttk.Button(self, text="Back", command= lambda: self.go_back(uname_e, pwd_e))

        # Alignments
        page_title.grid(row=0, column=1, ipadx=100, ipady=50, columnspan=2) #(side="top", pady=10, padx=10)
        
        uname_l.grid(row=1, column=1) 
        uname_e.grid(row=1, column=2)
        
        pwd_l.grid(row=2, column=1, pady=10)
        pwd_e.grid(row=2, column=2)
        
        login_b.grid(row=4, column=2, padx=10, pady=20)
        back_b.grid(row=5, column=1, padx=10, pady=20, columnspan=2)

    def authenticate(self, username, password):
        if users.signInUser(username.get(), password.get()):
            # Show the heartview frame and start data collection
            self.controller.show_frame(pages.Frames["HeartView"])
            settings.PD_Flag = True

            # enable user deletion and user editing
            self.controller.user_menu.entryconfigure(1, state=tk.NORMAL)
            self.controller.user_menu.entryconfigure(2, state=tk.NORMAL)
        else:
            tm.showerror("Validation Error", settings.invalidUserErr)
        # clear fields upon login attempt
        username.delete(0,tk.END)
        username.insert(0, "")
        password.delete(0,tk.END)
        password.insert(0, "")

    def go_back(self, uname, pwd):
        self.controller.show_frame(pages.Frames["DevID"])
        self.menu_bar()
        uname.delete(0,tk.END)
        uname.insert(0, "")
        pwd.delete(0,tk.END)
        pwd.insert(0, "")

    def menu_bar(self):
        self.controller.user_menu.entryconfigure(0, state=tk.DISABLED)