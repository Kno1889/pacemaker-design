# Communicate Module
#
# Version 1.1
# Created by: M. Lemcke
# Date Modified: Nov. 27, 2020
#
# Purpose: Process data to send and recieve from the pacemaker through UART serial communication

import serial
from struct import pack, unpack, calcsize
from modes import ranges, Mode
import numpy as np
from time import sleep

UINT_8 = 'B'        # Uint8 format character (1 byte)
UINT_16 = 'H'       # Uint16 format character (2 bytes)
SINGLE = 'f'        # Single format character (4 bytes)
DOUBLE = 'd'        # Double format character (8 bytes)

ser = serial.Serial()


class Com():

    # Initializes class variables and state variable ser parameters
    def __init__(self, port):

        self.dataBuffer = '='
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

    # Sends parameter data of the given mode to the pacemaker to change the current operating mode.
    # Returns false is the serial connection was lost, returns true if successful
    def setPacemakerMode(self, mode):
        if self._startSerial():
            # Add function code and mode number to the binary value
            binary = b"\x16\x55"
            binary += pack(UINT_8, mode.code)
            size = self.dataBuffer[1:]
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

    # requests the current mode information on the pacemaker. Returns a mode object with the name
    # “current” and the mode parameters on the pacemaker. Returns 0 if serial connection was interrupted
    def getPacemakerMode(self):
        if self._startSerial():
            code = -1
            params = {}
            binary = b"\x16\x22" + b"\x00"*(calcsize(self.dataBuffer)+1)
            ser.write(binary)
            sleep(0.1)
            buffer = '=' + UINT_8 + DOUBLE + \
                DOUBLE + UINT_8 + SINGLE + UINT_8 + self.dataBuffer[1:]
            data = ser.read(calcsize(buffer))
            if data:
                data = unpack(buffer, data)[5:]
                code, data = data[0], data[1:]
                params.update(ranges)
                for p in params:
                    params[p], data = data[0], data[1:]
                mode = Mode('current', code, params)
                self._endSerial()
                return mode
            self._endSerial()
        return 0

    # Requests the values read by the pacemaker on the ventricle and atrium signal pins of
    # the heart board. Returns a numpy array of the atrial signal, ventricular signal, and
    # current heart rate. Returns an empty array if serial connection was interrupted
    def getEgramValues(self):
        if self._startSerial():
            binary = b"\x16\x22" + b"\x00"*(calcsize(self.dataBuffer)+1)
            ser.write(binary)
            sleep(0.02)
            buffer = '=' + UINT_8 + DOUBLE + DOUBLE + UINT_16 + SINGLE
            data = ser.read(calcsize(buffer))
            if data:
                data = unpack(buffer, data)
            self._endSerial()
            if data and not data[0]:
                return np.array(data[1:])
        return []

    # Opens the serial connection. Returns true if successful, returns false otherwise
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

    # Closes the serial connection. Returns true if successful, returns false otherwise
    def _endSerial(self):
        try:
            ser.close()
            return True
        except(serial.SerialException):
            print("Lost serial connection")
            return False
