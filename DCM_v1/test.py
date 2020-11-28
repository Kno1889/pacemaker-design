import modes
from com import Com, ser
from struct import pack, calcsize
from time import sleep

# Corresponds to mode codes in serial excel sheet (uses nominal param values by default)
MODE = 2
c = Com('com5')     # Set to your com port number


print(c.getEgramValues())
