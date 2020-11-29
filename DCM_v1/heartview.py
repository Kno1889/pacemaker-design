'''
HeartView.py

Version: 0.3
Created By: Elston A.
Date Modified: Nov 18, 2020

Description: Contains the Tkinter class for the Login Page Window
'''

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as tm

# potentially make this import cleaner, maybe make special file for making users etc.
import users
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import settings
import pages

import plotter
import com
import modes

'''
Class: LoginPage

Description:
The class that defines the Tkinter Frame for the login screen.
'''
class HeartView(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, master = parent)
        self.grid_columnconfigure((0,2),weight=2)
        self.grid_columnconfigure((0,1),weight=1)

        self.parent = parent
        self.controller = controller

        # default values for the string var 
        self.activity_rate = tk.StringVar()
        self.activity_rate.set("hello")

        # Page Widgets
        page_title = tk.Label(self, text="EGram", font=settings.LARGE_FONT)
        logout_session_b = ttk.Button(self, text = "Exit Session", command=lambda:self.exit_session() )
        edit_settings_b = ttk.Button(self, text = "View Parameters", command=lambda:self.view_params() )
        plot_atr_check = tk.Checkbutton(self, text = "Plot Atrial", command=lambda:self.toggle_atr_plot())
        plot_vtr_check = tk.Checkbutton(self, text = "Plot Ventricle", command=lambda:self.toggle_vtr_plot())
        activity_rate = tk.Label(self, textvariable=self.activity_rate)

        plot_atr_check.select()
        plot_vtr_check.select()

        canvas = FigureCanvasTkAgg(plotter.f, self)
        canvas.draw()

        # Alignments
        page_title.grid(row=0, column=0, ipadx=0, ipady=10) #(side="top", pady=10, padx=10)
        edit_settings_b.grid(row=1, column = 0, sticky="n")
        logout_session_b.grid(row=2, column = 0, sticky="n")
        plot_atr_check.grid(row=3, column = 0, sticky='n')
        plot_vtr_check.grid(row=4, column = 0, sticky='n')
        activity_rate.grid(row=5, column = 0, sticky='n')
        canvas.get_tk_widget().grid(row=0,column=1, rowspan=6)
        
    def exit_session(self):
        settings.PD_Flag = False
        self.controller.show_frame(pages.Frames["DevID"])
        # Call the log out function in the backend
        users.signOutUser(users.currentUserInfo()[0])
        # disable all user menu options
        self.controller.user_menu.entryconfigure(0, state=tk.DISABLED)
        self.controller.user_menu.entryconfigure(1, state=tk.DISABLED)
        self.controller.user_menu.entryconfigure(2, state=tk.DISABLED)
        self.menu_bar()

    def view_params(self):
        settings.PD_Flag = False
        F = pages.customDataFrame["Monitor"]
        frame = F(parent=self.parent, controller=self.controller)
        frame.grid(row=0, column=0, sticky="NSEW")
        frame.tkraise()

    def toggle_atr_plot(self):
        settings.PLOT_ATR = not settings.PLOT_ATR

    def toggle_vtr_plot(self):
        settings.PLOT_VTR = not settings.PLOT_VTR

    def update_activity_rate(self):
        self.activity_rate.set(str(plotter.r_val))

    def set_curr_mode(self):
        c = com.COM(settings.COMPORT)
        curr_mode = c.getPacemakerMode()
        modes.setCurrentMode(curr_mode)

    def menu_bar(self):
        self.controller.user_menu.entryconfigure(0, state=tk.DISABLED)