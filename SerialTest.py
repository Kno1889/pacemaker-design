
import serial
from struct import pack

UINT_8 = 'B'        # Uint8 format character (1 byte)
UINT_16 = 'H'       # Uint16 format character (2 bytes)
SINGLE = 'f'        # Single format character (4 bytes)

comPort = 'COM5'    # Communication port identifier

# Initialize serial connection parameters
ser = serial.Serial(port=comPort, baudrate=9600, bytesize=serial.EIGHTBITS,
                    stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, timeout=0)

ser.close()
ser.open()
ser.write(b'hello')
