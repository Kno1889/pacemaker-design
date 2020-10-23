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

import traceback

import pages
import settings

chosen_mode = None


def exit_session(controller):
    users.signOutUser(users.currentUserInfo()[0])
    
    # disable all user options
    controller.user_menu.entryconfigure(0, state=tk.DISABLED)
    controller.user_menu.entryconfigure(1, state=tk.DISABLED)
    controller.user_menu.entryconfigure(2, state=tk.DISABLED)

    controller.show_frame(pages.Frames["DevID"])


        
class DefMode(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.columnconfigure(0, weight=1)

        page_title = tk.Label(self, text="Mode Selection", font=settings.LARGE_FONT)
        page_title.grid(row=0, column=0, ipadx=0, ipady=50)

        mode_label = tk.Label(self, text="Mode: ", font=settings.NORM_FONT)
        mode_label.grid(row=1, column=0)# pack()

        mode_options = [mode.name for mode in modes.allModes()]
        # default text
        mode_options.insert(0, "Choose")

        choice = tk.StringVar(self)
        choice.set(mode_options[0])

        dropdown = ttk.OptionMenu(self, choice, *mode_options)
        dropdown.grid(row = 1, column=1)

        b1 = ttk.Button(self, text="Set", command= lambda: self.set_mode(controller, choice))
        b2 = ttk.Button(self, text="Exit Session", command= lambda: exit_session(controller))

        b1.grid(row=3, column = 1)
        b2.grid(row=4, column = 1)

        
    def set_mode(self, controller, mode):
        mode_selected = mode.get()

        if mode_selected != "Choose":
            for mode in modes.allModes(): 
                if mode.name == mode_selected:
                    modes.setCurrentMode(mode)

                    # dynamic loading of the next frame
                    # This is because the data does not exist until after
                    F = pages.customDataFrame["Monitor"]
                    frame = F(parent=self.parent, controller = self.controller)
                    frame.grid(row = 0, column = 0, sticky="NSEW")
                    frame.tkraise()
                    break

'''
Class: Monitor

Description: 
Displays current operating mode and current parameters. Provides options to the user
to edit the current mode, change mode, and exit current session.
'''
class Monitor(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.columnconfigure(0, weight=1)

        self.mode = [] if modes.getCurrentMode() is None else modes.getCurrentMode()

        print(self.mode.params)
        
        label = tk.Label(self, text = 'DCM', font=settings.LARGE_FONT)
        label.grid(row=0, column=0, columnspan=2, pady=20)

        x = 1
        for key in self.mode.params:
            dcm_data_label = tk.Label(self, text = '{} :'.format(key), font=settings.NORM_FONT)
            dcm_value_label = tk.Label(self, text = '{}'.format(self.mode.params[key]), font=settings.NORM_FONT)
            dcm_data_label.grid(row=x, column=0, sticky="nsew")
            dcm_value_label.grid(row=x, column=1,sticky="nsew")
            x += 1


        b1 = ttk.Button(self, text="Edit Parameters", command = lambda: self.edit_params())
        b2 = ttk.Button(self, text="Change Mode", command = lambda: self.change_mode())
        bx = ttk.Button(self, text="Exit Session", command= lambda: exit_session(controller))

        b1.grid(row=x+1, column = 0, sticky="nswe", columnspan=2, pady=10)
        b2.grid(row=x+2, column = 0, sticky="nsew", columnspan=2, pady=10)
        bx.grid(row=x+3, column = 1)

    def edit_params(self):
        # bring up ModeChange delete frame  
        # dynamic loading of the next frame
        # This is because the data does not exist until after
        F = pages.customDataFrame["Edit"]
        frame = F(parent=self.parent, controller = self.controller)
        frame.grid(row = 0, column = 0, sticky="NSEW")
        frame.tkraise()
        self.destroy()

    def change_mode(self):
        # go back to defmode
        self.controller.show_frame(pages.Frames["DefMode"])
        self.destroy()

        
            
class ModeEdit(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.columnconfigure(0, weight=1)
        self.parent = parent
        self.controller = controller

        self.mode = [] if modes.getCurrentMode() is None else modes.getCurrentMode()
        
        # placeholders for labels and entries
        self.entries = []
        self.labels = []

        print(self.mode.params)
        
        label = tk.Label(self, text = 'DCM', font=settings.LARGE_FONT)
        label.grid(row=0, column=0)

        x = 1
        for key in self.mode.params:
            text = tk.StringVar(self, value=self.mode.params[key])
            dcm_data_label = tk.Label(self, text = '{} :'.format(key), font=settings.NORM_FONT)
            dcm_value = tk.Entry(self, textvariable = text)
            dcm_data_label.grid(row=x, column=0, sticky="nsew")
            dcm_value.grid(row=x, column=1,sticky="nsew")

            # store the entries and their labels to rebuild param array
            self.entries.append(dcm_value)
            self.labels.append(dcm_data_label)
            x += 1

        b1 = ttk.Button(self, text="Save", command = lambda: self.save())

        b1.grid(row=x+1, column = 2)
    
    # save the current entered parameters and return back to monitor
    def save(self):
        params = self.get_param_dict()
        
        try:
            status = modes.saveParamValues(modes.getCurrentMode(), params)
            if status == []:
                tm.showinfo("Success", "Successfully changed mode paramters")
            elif type(status) == list and len(status) > 0:
                err_msg = "These paramters are invalid:"
                for i in status:
                    err_msg = err_msg + "\n{}".format(str(i))
                tm.showerror("Error",err_msg )
                return None
            elif status == 1:
                tm.showerror("Error", "The given mode is not valid!")
                return None
            elif status == 2:
                tm.showerror("Error", "The parameters provided are of wrong datatype")
                return None
            else:
                tm.showerror("Error", settings.cfError)
                print(status)
                return None
        except Exception as e:
            tm.showerror("Error", str(e) + "\n\n" + str(traceback.print_exc()))
            return None

        F = pages.customDataFrame["Monitor"]
        frame = F(parent=self.parent, controller = self.controller)
        frame.grid(row = 0, column = 0, sticky="NSEW")
        frame.tkraise()
        self.destroy()

    # recreate parameter array
    def get_param_dict(self):
        params_rebuilt = {}
        for i in range(len(self.entries)):
            params_rebuilt[self.labels[i].cget("text")[:-2]] = float(self.entries[i].get())
        return params_rebuilt