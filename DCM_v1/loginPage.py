'''
loginPage.py

Version: 0.1
Created By: Elston A.
Date Modified: Oct 21, 2020

Docstrings
'''

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as tm

# potentially make this import cleaner, maybe make special file for making users etc.
import users

import settings
import pages



class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, master = parent)
        self.grid_columnconfigure((0,2),weight=2)
        self.grid_columnconfigure((0,1),weight=1)
        

        page_title = tk.Label(self, text="Login Page", font=settings.LARGE_FONT)
        page_title.grid(row=0, column=1, ipadx=100, ipady=50, columnspan=2) #(side="top", pady=10, padx=10)

        login_label = tk.Label(self, text="Username: ", font=settings.NORM_FONT)
        login_label.grid(row=1, column=1)# pack()

        username_entry = ttk.Entry(self)
        username_entry.grid(row=1, column=2 ) #pack()

        password_label = tk.Label(self, text="Password: ", font=settings.NORM_FONT)
        password_label.grid(row=2, column=1, pady=10)#pack()

        password_entry = ttk.Entry(self, show="*")
        password_entry.grid(row=2, column=2)#pack()

        login_button = ttk.Button(self, text="Login", command= lambda: 
        controller.show_frame(pages.Frames["DefMode"]) if 
        self.authenticate(username_entry, password_entry) 
        else tm.showerror("Validation Error", settings.invalidUserErr)) 
                                                    
        login_button.grid(row=4, column=2, padx=10, pady=20)#pack() 
        print(self.grid_size())
    
    def authenticate(self, username, password):
        ret_val = users.signInUser(username.get(), password.get())
        # clear fields upon login attempt
        username.delete(0,tk.END)
        username.insert(0, "")
        password.delete(0,tk.END)
        password.insert(0, "")
        return ret_val