'''
Controller.py

Version: 0.1
Created By: Elston A.
Date Modified: Oct 21, 2020

Docstrings
'''

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as tm

import users 
import data

from pages import *
import settings

def popupmsg(msg):
    def exit_popup():
        popup.destroy()

    popup = tk.Tk()
    popup.wm_title("Notice")
    label = ttk.Label(popup, text = msg, font=settings.NORM_FONT)
    label.pack(side="top", expand=True, pady=10)
    B1 = ttk.Button(popup, text="Done", command=exit_popup)
    B1.pack()
    popup.mainloop()

def create_user():
    def exit_create_user():
        #create_user.grab_release()
        create_user.destroy()
    
    def add_user(username, password):
        if users.makeNewUser(username, password):
            tm.showinfo("User Created",settings.createdUserNote)
            exit_create_user()
        else:
            tm.showerror("Error", settings.unableToCreateUser)
            exit_create_user()

    create_user = tk.Tk()
    #create_user.grab_set()
    create_user.minsize(300,100)
    create_user.wm_title("Add a user")
    
    title_text = ttk.Label(create_user, text = "Create a User", font=settings.LARGE_FONT)
    title_text.pack(pady=1)

    user_text = ttk.Label(create_user, text = "username", font=settings.NORM_FONT)
    user_text.pack(expand=True, pady=1)
    username = tk.Entry(create_user)
    username.pack(pady = 1)

    password_text = ttk.Label(create_user, text = "password", font=settings.NORM_FONT)
    password_text.pack(expand=True, pady=1)
    password = tk.Entry(create_user, show="*")
    password.pack(pady = 1)

    B1 = ttk.Button(create_user, text="Add", command=lambda: add_user(username.get(), password.get()))
    B1.pack(pady=2)

    create_user.mainloop()

def delete_user():

    def close_window():
        delete_user.destroy()

    def del_user(user):
        print(user)
        if user == "None":
            close_window()
        elif users.deleteUser(user):
            tm.showinfo("Deleted User", "Successfully deleted user")
            close_window()
        else:
            tm.showerror("Error", settings.cfError)
            close_window()

    raw_user_data = users.getUsers()
    options = []
    for data in raw_user_data:
        options.append(data['name'])
    
    # Tkinter being silly needs two none options for one to be default and for one to show
    # in the dropdown
    options.insert(0,"None")
    options.insert(0,"None")


    delete_user = tk.Tk()
    delete_user.minsize(300,100)
    delete_user.wm_title("Delete a User")

    title_text = ttk.Label(delete_user, text = "Delete a User", font=settings.LARGE_FONT)
    title_text.pack(pady=1)

    choice = tk.StringVar(delete_user)
    choice.set(options[0])

    option = ttk.OptionMenu(delete_user, choice, *options)
    option.pack()

    B1 = ttk.Button(delete_user, text="Delete", command=lambda: del_user(choice.get()))
    B1.pack(pady=2)

    delete_user.mainloop()

def edit_user():
    tm.showerror("Arr M8", "Feature not yet implemented")

class Controller(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Heart DCM")
        tk.Tk.resizable(self, width=True, height=True)
        self.debug_status = False

        container = tk.Frame(self)
        container.grid(row=0, column =0, sticky='NSEW')
        container.grid_columnconfigure(0,weight=1)
        container.grid_rowconfigure(0,weight=1)

        self.create_menu(container)

        self.frames = {}

        for F in Frames.values():
            frame = F(parent = container, controller = self)
            self.frames[F] = frame

            frame.grid(row = 0, column = 0, sticky="NSEW")

        self.show_frame(Frames["Login"])

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

    def create_menu(self, container):
        menubar = tk.Menu(container)

        help_menu = tk.Menu(menubar, tearoff = 0)
        help_menu.add_command(label="Documentation", command = lambda: popupmsg('Not Supported Yet!'))

        user_menu = tk.Menu(menubar, tearoff = 0)
        user_menu.add_command(label="Add User", command = lambda: self.popup(create_user))
        user_menu.add_command(label="Edit User", command = lambda: self.popup(edit_user))
        user_menu.add_command(label="Delete User", command = lambda: self.popup(delete_user))

        version_menu = tk.Menu(menubar, tearoff=0)
        version_menu.add_command(label="Version: {}".format(settings.VERSION))
        version_menu.entryconfigure(0, state = tk.DISABLED)

        debug_menu = tk.Menu(menubar, tearoff= 0)
        debug_menu.add_command(label="Debug: {}".format(self.debug_status), command = lambda: self.toggle_debug(debug_menu))

        menubar.add_cascade(label="Help", menu=help_menu)
        menubar.add_cascade(label="Users", menu=user_menu)
        menubar.add_cascade(label="Debugging", menu=debug_menu)
        menubar.add_cascade(label="Version", menu=version_menu)
        tk.Tk.config(self, menu=menubar)


    def toggle_debug(self, menu):
        #commands for debugging
        self.debug_status = not self.debug_status
        menu.entryconfigure(0, label="Debug: {}".format(self.debug_status))


    def popup(self, f):
        # do stuff to main window
        f()
