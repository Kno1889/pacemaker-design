'''
Controller.py

Version: 0.3
Created By: Elston A.
Date Modified: Oct 21, 2020

Description: Controller contains the class used to modify and control all other Tkinter windows
'''

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as tm

import re
import com
import users

from pages import *
import settings


# Function handles user creation
def create_user(controller):
    def exit_create_user(op):
        # create_user.grab_release()
        op.destroy()
        return 0

    # username validation using regex
    def username_valid(u):
        if(re.search(r"^(?=[a-zA-Z0-9._]{5,12}$)(?!.*[_.]{2})[^_.].*[^_.]$", u)):
            return True
        else:
            return False
    
    # password validation using regex
    def pwd_valid(p):
        if(re.search(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{5,50}$", p)):
            return True
        else:
            return False

    # Add user function utilizes the users.makeNewUser() method. Returns 0 if failure. Returns 1 when sucessful.
    def add_user(controller, username, password):
        if username_valid(username) is not True and settings.debug is False:
            tm.showerror("Username Error", settings.unameErr)
            exit_create_user(create_user)
            return 0
        if pwd_valid(password) is not True and settings.debug is False:
            tm.showerror("Password Error", settings.passErr)
            exit_create_user(create_user)
            return 0

        code = users.makeNewUser(username, password)

        # Manage error codes returned by backend
        err_codes = {
            1: settings.dataType,
            2: settings.nameExists,
            3: settings.maxCapacity
        }

        if code == 0:
            # Successfully added user
            controller.show_frame(pages.Frames["Login"])
            tm.showinfo("User Created", settings.createdUserNote)
            exit_create_user(create_user)
            return 1
        else:
            if type(code) == int and code > 0 and code <= 3:
                tm.showerror("User Creation Error", err_codes[code])
                exit_create_user(create_user)
                return 0
            else:
                # The user should not reach here
                tm.showerror("Error?", settings.unableToCreateUser)
                exit_create_user(create_user)
                return 0

    # Check if the user is currently signed in. Returns true if signed in. Returns false if not signed in.
    def is_signedIn():
        # users.currentUserInfo returns empty list when not signed in.
        if users.currentUserInfo() != []:
            return True
        else:
            return False

    # Make sure to warn the user that they will be signed out when trying to add a user. 
    if is_signedIn():
        tm.showwarning("Warning", "Adding a user logs you out of your current session!")
        users.signOutUser(users.currentUserInfo()[0])
        controller.show_frame(pages.Frames["Login"])
    
    # Tkinter window params
    create_user = tk.Tk()
    create_user.minsize(300, 100)
    create_user.wm_title("Add a user")

    # Widgets
    title_text = ttk.Label(create_user, text="Create a User", font=settings.LARGE_FONT)
    user_text = ttk.Label(create_user, text="username", font=settings.NORM_FONT)
    password_text = ttk.Label(create_user, text="password", font=settings.NORM_FONT)
    B1 = ttk.Button(create_user, text="Add", command=lambda: add_user(controller, username.get(), password.get()))

    username = tk.Entry(create_user)
    password = tk.Entry(create_user, show="*")

    #Widget Alignment
    title_text.pack(pady=1)

    user_text.pack(expand=True, pady=1)
    username.pack(pady=1)

    password_text.pack(expand=True, pady=1)
    password.pack(pady=1)

    B1.pack(pady=2)

    # Create user window loop
    create_user.mainloop()

# Function handles user deletion
def delete_user(controller):

    def close_window():
        delete_user.destroy()
        return 0

    def del_user(user):
        # Handle case when no user is logged in
        if user == []:
            tm.showinfo("No User Logged In")
            close_window()
            return 0
        elif users.deleteUser(user[0]):
            tm.showinfo("Deleted User", "Successfully deleted user")
            # Bring the user back to the login page after deletion
            controller.show_frame(pages.Frames["Login"])
            # Ensure menu controls for users are disabled
            controller.user_menu.entryconfigure(1, state=tk.DISABLED)
            controller.user_menu.entryconfigure(2, state=tk.DISABLED)
            close_window()
            return 1
        else:
            tm.showerror("Error", settings.cfError)
            close_window()
            return 0
    
    tm.showwarning("Warning","The current user will be deleted!")

    # Tkinter window params
    delete_user = tk.Tk()
    delete_user.minsize(300, 100)
    delete_user.wm_title("Delete User")

    # Widgets
    title_text = ttk.Label(delete_user, text="Delete User?", font=settings.LARGE_FONT)
    B1 = ttk.Button(delete_user, text="Delete Current User!", command=lambda: del_user(users.currentUserInfo()))
    
    # Widget Placement
    title_text.pack(pady=1)
    B1.pack(pady=2)

    # Delete Window Loop
    delete_user.mainloop()


# Function which handles editing of users 
def edit_user(controller):
    tm.showerror("Arr M8", "Feature not yet implemented")

'''
Class: Controller

Description:
The Tkinter class which defines the controller of the Tkinter framework being used.
Loads static frames, menues, debugging, etc
'''
class Controller(tk.Tk):
    def __init__(self, *args, **kwargs):

        if settings.connected == False:
            tm.showerror("Error", "No pacemaker connected, exiting!")
            self.destroy()

        # Tkinter window params
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Heart DCM")
        tk.Tk.resizable(self, width=False, height=False)
        self.debug_status = False

        container = tk.Frame(self)
        container.grid_propagate(True)
        self.com_handler = com.Com(settings.COMPORT)
        self.grid_columnconfigure(0, weight=1)

        container.grid(row=0, column=0, sticky='nsew')

        # Load the menu 
        self.create_menu(container)

        self.frames = {}

        # Load all frames in the background
        for F in Frames.values():
            frame = F(parent=container, controller=self)
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        # Bring the desired frame DevID to front 
        self.show_frame(Frames["DevID"])

    # Method used for switching frames
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
    def get_page(self, page_name):
        return self.frames[page_name]

    # Method which handles creation of the menu in Tkinter
    def create_menu(self, container):
        menubar = tk.Menu(container)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Documentation", command=lambda: tm.showwarning("warning",'Not Supported Yet!'))

        self.user_menu = tk.Menu(menubar, tearoff=0)
        self.user_menu.add_command(label="Add New User",        command=lambda: create_user(self))
        self.user_menu.add_command(label="Edit Current User",   command=lambda: edit_user(self))
        self.user_menu.add_command(label="Delete Current User", command=lambda: delete_user(self))
        self.user_menu.entryconfigure(0, state=tk.DISABLED)
        self.user_menu.entryconfigure(1, state=tk.DISABLED)
        self.user_menu.entryconfigure(2, state=tk.DISABLED)

        version_menu = tk.Menu(menubar, tearoff=0)
        version_menu.add_command(label="Version: {}".format(settings.VERSION))
        version_menu.entryconfigure(0, state=tk.DISABLED)

        debug_menu = tk.Menu(menubar, tearoff=0)
        debug_menu.add_command(label="Debug: {}".format(
            settings.debug), command=lambda: self.toggle_debug(debug_menu))

        menubar.add_cascade(label="Help",      menu=help_menu)
        menubar.add_cascade(label="Users",     menu=self.user_menu)
        menubar.add_cascade(label="Debugging", menu=debug_menu)
        menubar.add_cascade(label="Version",   menu=version_menu)
        tk.Tk.config(self, menu=menubar)

    # debug function for setting the application in debugging mode
    def toggle_debug(self, menu):
        # commands for debugging
        settings.debug = not settings.debug
        menu.entryconfigure(0, label="Debug: {}".format(settings.debug))

