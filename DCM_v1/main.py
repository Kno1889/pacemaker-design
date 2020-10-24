'''
main.py

Version: 0.1
Created By: Elston A.
Date Modified: Oct 21, 2020

Description: Script used to run tkinter interface
'''

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as tm

import settings
import controller

def main():

    # Create Tkinter App from Controller Class
    app = controller.Controller()

    # Center Window on screen
    window_width = settings.WIDTH
    window_height  = settings.HEIGHT

    location_x = int((app.winfo_screenwidth()/2) - (window_width/2))
    location_y = int((app.winfo_screenheight()/2) - (window_height/2))
    app.geometry("{}x{}+{}+{}".format(
        window_width,
        window_height,
        location_x,
        location_y
    ))

    # run main tkinter loop
    app.mainloop()

if __name__ == "__main__":
    main()