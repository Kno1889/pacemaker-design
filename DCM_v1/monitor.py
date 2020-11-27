'''
monitor.py

Version: 0.1
Created By: Elston A.
Date Modified: Oct 21, 2020

Description: Contains classes and methods required for operation of the DCM.
'''



import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as tm

import users
import modes

from com import Com

import traceback
import pages
import settings

c = Com('com5')

##########
# REMOVE # 
# This snippet is because we have not selected a mode
# This snippet pre-selects a mode for testing
##########
m = modes.allModes()
c = 'aoo'
for mode in m:
    if mode.name == c:
        modes.setCurrentMode(mode)
        break
##########

# Log Out of Session


def exit_session(controller):
    # Return Back to Device ID Frame
    controller.show_frame(pages.Frames["DevID"])

    # Call the log out function in the backend
    users.signOutUser(users.currentUserInfo()[0])

    # disable all user menu options
    controller.user_menu.entryconfigure(0, state=tk.DISABLED)
    controller.user_menu.entryconfigure(1, state=tk.DISABLED)
    controller.user_menu.entryconfigure(2, state=tk.DISABLED)


'''
Class: DefMode

Description:
Tkinter class used to define the frame for when the user chooses an
operating mode for the pacemaker. 
'''


class DefMode(tk.Frame):

    def __init__(self, parent, controller):

        # Tkinter Frame Setup
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.columnconfigure(0, weight=1)

        # Widgets
        page_title = tk.Label(self, text="Mode Selection",
                              font=settings.LARGE_FONT)
        mode_label = tk.Label(self, text="Mode: ", font=settings.NORM_FONT)
        b1 = ttk.Button(self, text="Set",
                        command=lambda: self.set_mode(controller, choice))
        b2 = ttk.Button(self, text="Exit Session",
                        command=lambda: exit_session(controller))

        # Get all possible modes and ensure that a default option is "chosen"
        mode_options = [mode.name for mode in modes.allModes()]
        mode_options.insert(0, "Choose")

        # Create a Tkinter string var which is used for dropdown choice
        choice = tk.StringVar(self)
        choice.set(mode_options[0])

        # Define dropdown widget
        dropdown = ttk.OptionMenu(self, choice, *mode_options)

        # Placement of widgets
        page_title.grid(row=0, column=0, ipadx=0, ipady=50)
        mode_label.grid(row=1, column=0)
        dropdown.grid(row=1, column=1)
        b1.grid(row=3, column=1)
        b2.grid(row=4, column=1)

    # Method that handles the setting of the pacemaker mode
    def set_mode(self, controller, mode):
        mode_selected = mode.get()

        # Ensure a valid choice is considered
        if mode_selected != "Choose":
            # Get the mode we want to select. setCurrentMode requires a Mode object
            for mode in modes.allModes():
                if mode.name == mode_selected:
                    # Calls the backend function setCurrentMode()
                    modes.setCurrentMode(mode)

                    c.setPacemakerMode(modes.getCurrentMode())

                    # dynamic loading of the next frame
                    # This is because the data does not exist until after
                    F = pages.customDataFrame["Monitor"]
                    frame = F(parent=self.parent, controller=self.controller)
                    frame.grid(row=0, column=0, sticky="NSEW")
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
        # Tkinter Fame Setup
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.columnconfigure(0, weight=1)

        # Find the current operating mode
        self.mode = [] if modes.getCurrentMode() is None else modes.getCurrentMode()

        if self.mode == []:
            # should not reach here
            tm.showerror(
                "Unexpected Error, no current operating mode for pacemaker")

        label = tk.Label(self, text='DCM', font=settings.LARGE_FONT)
        label.grid(row=0, column=0, columnspan=2, pady=20)

        # Dynamically create widgets for various parameters
        x = 1
        for key in self.mode.params:
            dcm_data_label = tk.Label(
                self, text='{} :'.format(key), font=settings.NORM_FONT)
            dcm_value_label = tk.Label(self, text='{}'.format(
                self.mode.params[key]), font=settings.NORM_FONT)
            dcm_data_label.grid(row=x, column=0, sticky="nsew")
            dcm_value_label.grid(row=x, column=1, sticky="nsew")
            x += 1

        # Button Widgets
        b1 = ttk.Button(self, text="Edit Parameters", command=lambda: self.edit_params())
        b2 = ttk.Button(self, text="Change Mode", command=lambda: self.change_mode())
        b3 = ttk.Button(self, text="Heart Monitor", command=lambda: self.show_heartview())
        bx = ttk.Button(self, text="Exit Session", command=lambda: exit_session(controller))

        # Alignment of Widgets
        b1.grid(row=x+1, column=0, sticky="ns", columnspan=1, pady=5)
        b2.grid(row=x+2, column=0, sticky="ns", columnspan=1, pady=5)
        b3.grid(row=x+3, column=0, sticky="ns", columnspan=1, pady=5)

        bx.grid(row=x+4, column=1)

    def edit_params(self):
        # bring up ModeChange delete frame
        # dynamic loading of the next frame
        # This is because the data does not exist until after
        F = pages.customDataFrame["Edit"]
        frame = F(parent=self.parent, controller=self.controller)
        frame.grid(row=0, column=0, sticky="NSEW")
        frame.tkraise()
        self.destroy()

    def show_heartview(self):
        settings.PD_Flag = True
        self.controller.show_frame(pages.Frames["HeartView"])
        self.destroy()

    def change_mode(self):
        # go back to defmode
        self.controller.show_frame(pages.Frames["DefMode"])
        self.destroy()


'''
Class: Mode Edit

Description:
Tkinter class used for defining the window where the user would change the parameters
of the pacemaker. 
'''


class ModeEdit(tk.Frame):
    def __init__(self, parent, controller):
        # Tkinter Fame Setup
        tk.Frame.__init__(self, parent)
        self.columnconfigure(0, weight=1)
        self.parent = parent
        self.controller = controller

        # Get the current mode
        self.mode = [] if modes.getCurrentMode() is None else modes.getCurrentMode()

        if self.mode == []:
            # should not reach here
            tm.showerror(
                "Unexpected Error, no current operating mode for pacemaker")

        # placeholders for labels and entries
        self.entries = []
        self.labels = []

        label = tk.Label(self, text='DCM', font=settings.LARGE_FONT)
        label.grid(row=0, column=0)

        # display all the mode paramters with entry widgets
        x = 1
        for key in self.mode.params:
            text = tk.StringVar(self, value=self.mode.params[key])
            dcm_data_label = tk.Label(
                self, text='{} :'.format(key), font=settings.NORM_FONT)
            dcm_value = tk.Entry(self, textvariable=text)
            dcm_data_label.grid(row=x, column=0, sticky="nsew")
            dcm_value.grid(row=x, column=1, sticky="nsew")

            # store the entries and their labels to rebuild param array
            self.entries.append(dcm_value)
            self.labels.append(dcm_data_label)
            x += 1

        b1 = ttk.Button(self, text="Save", command=lambda: self.save())

        b1.grid(row=x+1, column=2)

    # save the current entered parameters and return back to monitor
    def save(self):

        # recreate the param dict
        params = self.get_param_dict()

        # Save paramters and handle any errors the backend returns
        try:
            status = modes.saveParamValues(modes.getCurrentMode(), params)
            if status == []:
                tm.showinfo("Success", "Successfully changed mode paramters")
                c.setPacemakerMode(modes.getCurrentMode())
            elif type(status) == list and len(status) > 0:
                err_msg = "These paramters are invalid:"
                for i in status:
                    err_msg = err_msg + "\n{}".format(str(i))
                tm.showerror("Error", err_msg)
                return None
            elif status == 1:
                tm.showerror("Error", "The given mode is not valid!")
                return None
            elif status == 2:
                tm.showerror(
                    "Error", "The parameters provided are of wrong datatype")
                return None
            else:
                tm.showerror("Error", settings.cfError)
                return None
        except Exception as e:
            tm.showerror("Error", str(e) + "\n\n" + str(traceback.print_exc()))
            return None

        # Recreate the Monitor frame which was deleted
        F = pages.customDataFrame["Monitor"]
        frame = F(parent=self.parent, controller=self.controller)
        frame.grid(row=0, column=0, sticky="NSEW")
        frame.tkraise()
        self.destroy()

    # recreate parameter array
    def get_param_dict(self):
        params_rebuilt = {}
        for i in range(len(self.entries)):
            params_rebuilt[self.labels[i].cget(
                "text")[:-2]] = float(self.entries[i].get())
        return params_rebuilt
