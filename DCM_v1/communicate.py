# Communicate Module
#
# Version 0.1
# Created by: M. Lemcke
# Date Modified: Nov. 9, 2020
#
# Purpose: Process data to send and recieve from the pacemaker through UART serial communication

import serial
from struct import pack, unpack, calcsize
from modes import ranges
from random import randint
import numpy as np
from time import sleep

UINT_8 = 'B'        # Uint8 format character (1 byte)
UINT_16 = 'H'       # Uint16 format character (2 bytes)
SINGLE = 'f'        # Single format character (4 bytes)

comPort = ''        # Communication port identifier

# Start serial communication
try:
    ser = serial.Serial(port=comPort, baudrate=57600,
                        bytesize=serial.EIGHTBITS)
    # Close old serial connection and start new
    if ser.is_open():
        ser.close()
    ser.open()
except(serial.SerialException):
    print("Cannot connect to serial")


# Dummy function for egram development
def startEgram():
    fn_code = 2
    binary = pack(UINT_8, fn_code)
    return 1


# Add a sampling speed(in sec) and number of data points as parameters
# Return numpy array
# Dummy function for egram development
def getValues(sampleSpeed, dataPoints):
    info = [[], []]
    for i in range(dataPoints):
        # Read serial
        vent = randint(0, 10)
        atr = randint(0, 10)
        info[0].append(vent)
        info[1].append(atr)
        sleep(sampleSpeed)
    return np.array(info)


# Dummy function for egram development
def stopEgram():
    fn_code = 3
    binary = pack(UINT_8, fn_code)
    return 0


# Send all mode information and parameters to pacemaker via serial communication
# Return true if the pacemaker recieved the correct values
def sendParams(mode):
    fn_code = 1
    buffer = '='
    # Add function code and mode number to the binary value
    binary = pack(UINT_8, 0) + pack(UINT_8, fn_code) + pack(UINT_8, mode.code)
    buffer += UINT_8 + UINT_8 + UINT_8
    # Add a binary value for every possible parameter value
    for r in ranges:
        # Determine the number of bytes needed to store the parameter value
        if type(ranges[r][-1]) == list:
            maxVal = ranges[r][-1][-1]
        else:
            maxVal = ranges[r][-1]
        if type(maxVal) == int:
            if maxVal > 255:
                size = UINT_16
            else:
                size = UINT_8
        else:
            size = SINGLE
        match = False
        # Look for matching parameter in given mode
        for p in mode.params:
            if p == r:
                # Add binary value
                value = mode.params[p]
                binary += pack(size, value)
                match = True

        # Create an empty value if parameter isn't used in the given mode
        if not match:
            binary += pack(size, 0)
        buffer += size
    print(unpack(buffer, binary))
    return _getParams(buffer, binary) == unpack(buffer, binary)


# Read the current mode and parameter values on the pacemaker
# Temporary dummy function, will remove binary param in place of reading serial input
def _getParams(buffer, binary):
    return unpack(buffer, binary)
