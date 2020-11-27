'''
settings.py

Version: 0.3
Created By: Elston A.
Date Modified: Oct 21, 2020

Description: Settings is used for holding global variables and state strings
'''

# Global Variables
VERSION = 0.30
LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 8)
WIDTH = 720
HEIGHT = 480

COMPORT = 'COM3'    # Communication port identifier

debug = False

connected = True

# Get pacemaker data
PD_Flag = False

# State Return Strings
invalidUserErr = '''The username or password you have entered is incorrect. \n\n
                                Please try again.'''
createdUserNote = "You have successfully created a new user!"
unableToCreateUser = "Unable to create. Undefined Error!"
dataType = "Data Type Error!"
nameExists = "A User With This Name Already Exists!"
maxCapacity = "Pacemaker At Max Capacity!"
cfError = "Catastrophic Failure!"
newIdErr = "The device ID does not match the previously connected device ID\n This is a different pacemaker!"
unameErr = "Please enter a valid username\nA username must be 4-12 characters long\nA username must only contain letters and numbers!"
passErr = '''The password you have entered does not meet requirements.
Must be within 5-50 characters and contain:
-One upper case (A-Z)
-One lower case (a-z)
-One number (0-9)
-One symbol (?!,._;:)'''