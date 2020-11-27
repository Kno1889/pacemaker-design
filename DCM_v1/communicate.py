# Communicate Module
#
# Version 0.1
# Created by: M. Lemcke
# Date Modified: Nov. 12, 2020
#
# Purpose: Process data to send and recieve from the pacemaker through UART serial communication

import serial
from struct import pack, unpack, calcsize
from modes import ranges, Mode
from random import randint
import numpy as np
from time import sleep

import settings

UINT_8 = 'B'        # Uint8 format character (1 byte)
UINT_16 = 'H'       # Uint16 format character (2 bytes)
SINGLE = 'f'        # Single format character (4 bytes)

SYNCH = 22           # Serial synch code

# Initialize serial connection parameters
ser = serial.Serial(port=settings.COMPORT, baudrate=115200, bytesize=serial.EIGHTBITS,
                    stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, timeout=0)


# Function to get the device ID of the connected pacemaker
# Returns device id number, returns 0 if no device connected
def getDeviceID():
    if _startSerial():
        _sendCommand(4)
        deviceID = 0
        # Serial read id number
        _endSerial()
        return deviceID
    return 0


# Tells the pacemaker to start sending egram data
# Returns true if sucessful, return false if no device connected
# Dummy function for egram development
def startEgram():
    if _startSerial():
        _sendCommand(2)
        return True
    return False


# Retrieves egram data given a sampling speed(in sec) and number of data points
# Return numpy array, return false if egram is not running
# Dummy function for egram development
def getEgramValues(sampleSpeed=1, dataPoints=1):
    if ser.isOpen():
        info = [[], []]
        for i in range(dataPoints):
            # Serial read ventrical and atrium signal
            vent = randint(0, 10)
            atr = randint(0, 10)
            info[0].append(vent)
            info[1].append(atr)
            sleep(sampleSpeed)
        return np.array(info)
    return False


# Tells the pacemaker to stop sending egram data
# Returns true if sucessful, return false if egram is not open
# Dummy function for egram development
def stopEgram():
    if ser.isOpen():
        _sendCommand(3)
        _endSerial()
        return True
    return False


# Send all mode information and parameters to pacemaker via serial communication
# Returns true if sucessful, return false if no device connected
def setPacemakerMode(mode):
    if _startSerial():
        fn_code = 85
        buffer = '='
        # Add function code and mode number to the binary value
        # binary = pack(UINT_8, SYNCH) + pack(UINT_8, fn_code) + \
        #     pack(UINT_8, mode.code)
        binary = b"\x16\x55" + pack(UINT_8, mode.code)
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
        ser.write(binary)
        print(calcsize(buffer))
        print(unpack(buffer, binary))
        _endSerial()
        return True
    return False


# Read the current mode and parameter values on the pacemaker
# Returns a Mode object created using the parameters recieved from the pacemaker, returns 0 if no device connected
# Frontend will find the existing mode object with the same code number and pass it to the saveParamValues() function
# in the modes module with the params dict variable in the mode object returned
# Temporary dummy function
def getPacemakerMode():
    if _startSerial():
        _sendCommand(5)
        # Serial read mode code and parameter values
        code = 4
        params = {}
        currMode = Mode('current', code, params)
        _endSerial()
        return currMode
    return 0


# Sends a command to the pacemaker with given function code
def _sendCommand(fn_code):
    binary = pack(UINT_8, SYNCH) + pack(UINT_8, fn_code)
    # Serial write binary


# Start serial communication
# Return true if successful, return false if no device connected
def _startSerial():
    try:
        # Close old serial connection and start new
        if ser.isOpen():
            ser.close()
        ser.open()
        return True
    except(serial.SerialException):
        print("Cannot connect to serial")
        return False


# Stop serial communication
# Return true if successful, return false if no device connected
def _endSerial():
    try:
        ser.close()
        return True
    except(serial.SerialException):
        print("Cannot connect to serial")
        return False


# ser.close()
# ser.open()
# ser.write(pack(UINT_8, 22))
