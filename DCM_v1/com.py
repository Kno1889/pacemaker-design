# Communicate Module
#
# Version 1.0
# Created by: M. Lemcke
# Date Modified: Nov. 19, 2020
#
# Purpose: Process data to send and recieve from the pacemaker through UART serial communication

import serial
from struct import pack, unpack, calcsize
from modes import ranges, Mode
from random import randint
import numpy as np
from time import sleep

UINT_8 = 'B'        # Uint8 format character (1 byte)
UINT_16 = 'H'       # Uint16 format character (2 bytes)
SINGLE = 'f'        # Single format character (4 bytes)

ser = serial.Serial()


class Com():
    def __init__(self, port):

        self.dataBuffer = ''
        self.comPort = port

        for r in ranges:
            # Determine the number of bytes needed to store the parameter values
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
            self.dataBuffer += size

        try:
            ser.port = self.comPort
            ser.baudrate = 115200
            ser.bytesize = serial.EIGHTBITS
            ser.stopbits = serial.STOPBITS_ONE
            ser.parity = serial.PARITY_NONE
            ser.timeout = 1
        except(serial.SerialException):
            print("Serial cannot be connected")

    # Send all mode information and parameters to pacemaker via serial communication
    # Returns true if sucessful, return false if no device connected
    def setPacemakerMode(self, mode):
        if self._startSerial():
            # Add function code and mode number to the binary value
            binary = b"\x16\x55"
            binary += pack(UINT_8, mode.code)
            size = self.dataBuffer
            # Add a binary value for every possible parameter value
            for r in ranges:
                match = False
                # Look for matching parameter in given mode
                for p in mode.params:
                    if p == r:
                        # Add binary value
                        value = mode.params[p]
                        binary += pack(size[0], value)
                        size = size[1:]
                        match = True
                # Create an empty value if parameter isn't used in the given mode
                if not match:
                    binary += pack(size[0], 0)
                    size = size[1:]
            ser.write(binary)
            self._endSerial()
            return True
        return False

    # Read the current mode and parameter values on the pacemaker
    # Returns a Mode object created using the parameters recieved from the pacemaker, returns 0 if no device connected
    # Frontend will find the existing mode object with the same code number and pass it to the saveParamValues() function
    # in the modes module with the params dict variable in the mode object returned
    # Temporary dummy function
    def getPacemakerMode(self):
        if self._startSerial():
            code = -1
            params = {}
            binary = b"\x16\x22" + b"\x00"*(calcsize(self.dataBuffer)+1)
            ser.write(binary)
            sleep(0.1)
            buffer = '=' + UINT_8 + self.dataBuffer
            data = ser.read(calcsize(self.dataBuffer)+1)
            data = unpack(buffer, data)
            code, data = data[0], data[1:]
            params.update(ranges)
            for p in params:
                params[p], data = data[0], data[1:]
            mode = Mode('current', code, params)
            return mode
        return 0

    # Function to get the device ID of the connected pacemaker
    # Returns device id number, returns 0 if no device connected
    def getDeviceID(self):
        if self._startSerial():
            binary = b"\x16\x44" + b"\x00"*(calcsize(self.dataBuffer)+1)
            ser.write(binary)
            sleep(0.1)
            deviceID = 0
            # Serial read id number
            self._endSerial()
            return deviceID
        return 0

    # Tells the pacemaker to start sending egram data
    # Returns true if sucessful, return false if no device connected
    def startEgram(self):
        if self._startSerial():
            binary = b"\x16\x11" + b"\x00"*(calcsize(self.dataBuffer)+1)
            ser.write(binary)
            return True
        return False

    # Tells the pacemaker to stop sending egram data
    # Returns true if sucessful, return false if egram is not open
    def stopEgram(self):
        if ser.isOpen():
            binary = b"\x16\x33" + b"\x00"*(calcsize(self.dataBuffer)+1)
            ser.write(binary)
            self._endSerial()
            return True
        return False

    # Retrieves egram data given a sampling speed(in sec) and number of data points
    # Return numpy array, return false if egram is not running
    # Dummy function for egram development
    def getEgramValues(self, sampleSpeed, dataPoints):
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

    # Start serial communication
    # Return true if successful, return false if no device connected
    def _startSerial(self):
        try:
            # Close old serial connection and start new
            if ser.isOpen():
                ser.close()
            ser.open()
            return True
        except(serial.SerialException):
            print("Lost serial connection")
            return False

    # Stop serial communication
    # Return true if successful, return false if no device connected
    def _endSerial(self):
        try:
            ser.close()
            return True
        except(serial.SerialException):
            print("Lost serial connection")
            return False
