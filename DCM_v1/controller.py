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

from pages import *
import settings



def create_user(controller):
    def exit_create_user():
        # create_user.grab_release()
        create_user.destroy()

    def add_user(controller, username, password):
        if(username == ""):
            tm.showerror("User Creation Error","Username is blank!\nPlease enter a username")
            return 0
        code = users.makeNewUser(username, password)

        err_codes = {
            1: settings.dataType,
            2: settings.nameExists,
            3: settings.maxCapacity
        }

        if code == 0:
            tm.showinfo("User Created", settings.createdUserNote)
            controller.show_frame(pages.Frames["Login"])
            exit_create_user()
        else:
            if type(code) == int and code > 0 and code <= 3:
                tm.showerror("User Creation Error", err_codes[code])
            else:
                tm.showerror("Error?", settings.unableToCreateUser)
                exit_create_user()

    def is_signedIn():
        if users.currentUserInfo() != []:
            return True
        else:
            return False

    if is_signedIn():
        tm.showwarning("Warning", "Adding a user will log you out of your current session!")
    
    create_user = tk.Tk()
    create_user.minsize(300, 100)
    create_user.wm_title("Add a user")

    title_text = ttk.Label(create_user, text="Create a User", font=settings.LARGE_FONT)
    title_text.pack(pady=1)

    user_text = ttk.Label(create_user, text="username", font=settings.NORM_FONT)
    user_text.pack(expand=True, pady=1)
    username = tk.Entry(create_user)
    username.pack(pady=1)

    password_text = ttk.Label(create_user, text="password", font=settings.NORM_FONT)
    password_text.pack(expand=True, pady=1)
    password = tk.Entry(create_user, show="*")
    password.pack(pady=1)

    B1 = ttk.Button(create_user, text="Add", command=lambda: add_user(controller, username.get(), password.get()))
    B1.pack(pady=2)

    create_user.mainloop()


def delete_user(controller):

    def close_window():
        delete_user.destroy()

    def del_user(user):
        if user == []:
            tm.showinfo("No User Logged In")
            close_window()
        elif users.deleteUser(user[0]):
            tm.showinfo("Deleted User", "Successfully deleted user")
            controller.show_frame(pages.Frames["Login"])
            controller.user_menu.entryconfigure(1, state=tk.DISABLED)
            controller.user_menu.entryconfigure(2, state=tk.DISABLED)
            close_window()
        else:
            tm.showerror("Error", settings.cfError)
            close_window()
    tm.showwarning("Warning","The current user will be deleted!")
    delete_user = tk.Tk()
    delete_user.minsize(300, 100)
    delete_user.wm_title("Delete User")

    title_text = ttk.Label(delete_user, text="Delete User?", font=settings.LARGE_FONT)
    title_text.pack(pady=1)

    B1 = ttk.Button(delete_user, text="Delete Current User!", command=lambda: del_user(users.currentUserInfo()))
    B1.pack(pady=2)

    delete_user.mainloop()


def edit_user(controller):
    tm.showerror("Arr M8", "Feature not yet implemented")


class Controller(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Heart DCM")
        tk.Tk.resizable(self, width=False, height=False)
        self.debug_status = False

        container = tk.Frame(self)
        container.grid_propagate(True)

        self.grid_columnconfigure(0, weight=1)
        # self.grid_rowconfigure(0,weight=1)
        container.grid(row=0, column=0, sticky='nsew')

        self.create_menu(container)

        self.frames = {}

        for F in Frames.values():
            frame = F(parent=container, controller=self)
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Frames["DevID"])

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

    def create_menu(self, container):
        menubar = tk.Menu(container)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Documentation", command=lambda: tm.showwarning("warning",'Not Supported Yet!'))

        self.user_menu = tk.Menu(menubar, tearoff=0)
        self.user_menu.add_command(label="Add New User", command=lambda: create_user(self))
        self.user_menu.add_command(label="Edit Current User", command=lambda: edit_user(self))
        self.user_menu.add_command(label="Delete Current User", command=lambda: delete_user(self))
        self.user_menu.entryconfigure(0, state=tk.DISABLED)
        self.user_menu.entryconfigure(1, state=tk.DISABLED)
        self.user_menu.entryconfigure(2, state=tk.DISABLED)

        version_menu = tk.Menu(menubar, tearoff=0)
        version_menu.add_command(label="Version: {}".format(settings.VERSION))
        version_menu.entryconfigure(0, state=tk.DISABLED)

        debug_menu = tk.Menu(menubar, tearoff=0)
        debug_menu.add_command(label="Debug: {}".format(
            self.debug_status), command=lambda: self.toggle_debug(debug_menu))

        menubar.add_cascade(label="Help", menu=help_menu)
        menubar.add_cascade(label="Users", menu=self.user_menu)
        menubar.add_cascade(label="Debugging", menu=debug_menu)
        menubar.add_cascade(label="Version", menu=version_menu)
        tk.Tk.config(self, menu=menubar)

    def toggle_debug(self, menu):
        # commands for debugging
        self.debug_status = not self.debug_status
        menu.entryconfigure(0, label="Debug: {}".format(self.debug_status))

    def popup(self, f):
        # do stuff to main window
        f()
