import modes
from com import Com, ser
from struct import pack, calcsize
from time import sleep

# Corresponds to mode codes in serial excel sheet (uses nominal param values by default)
MODE = 0
c = Com('com5')     # Set to your com port number


modes.setCurrentMode(modes.allModes()[MODE])
currentMode = modes.getCurrentMode()
print(c.setPacemakerMode(currentMode))


# Should always print true when you run it. Otherwise there is a problem with the serial connection
