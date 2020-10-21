'''
pages.py

Version: 0.1
Created By: Elston A.
Date Modified: Oct 21, 2020

Docstrings
'''

from loginPage import *
from PageExampleOne import *
from PageExampleTwo import *

# Page imports. Import the page above and throw it into the array below

Frames = {
    "Login": LoginPage, 
    "exampleOne": PageExampleOne, 
    "exampleTwo": PageExampleTwo
    }

