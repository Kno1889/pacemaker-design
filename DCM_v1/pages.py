'''
pages.py

Version: 0.3
Created By: Elston A.
Date Modified: Oct 21, 2020

Purpose: Keeping track of Tkinter frames in a single place
'''

from loginPage import *
from monitor import *
from deviceIdentification import *

# Page imports. Import the page above and throw it into the array below

# Frames that can be loaded on startup
Frames = {
    "Login": LoginPage,
    "DefMode": DefMode,
    "DevID": DeviceIdentification, 
    }

# Frames that need previous frame data
# Cannot be loaded on startup
customDataFrame = {
    "Monitor": Monitor,
    "Edit": ModeEdit,
}
