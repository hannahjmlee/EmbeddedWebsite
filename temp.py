#!/usr/bin/python
import serial
import sys
import time
import os
import io


def readVal():
    count = 0; 
    while True:
        response = ser.readline()
        if count != 0: 
            response = response.translate(None, b'\r\n').decode()
            break
        count = count + 1; 
    print(count)
    return response


ser = serial.Serial("/dev/ttyUSB0", 9600, timeout = 1)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

sio.write(str("C"))
sio.flush()
response = sio.readline(15).strip()
print("Sent C: ", response)
sio.flush()
sio.write(str("b"))
sio.flush()
response = sio.readline()
print("Sent b: " , response)
sio.flush()
sio.write(str("2"))
sio.flush()
response = sio.readline()
print("Sent 2: " , response)
sio.flush()
print("It maybe worked")
ser.close() 

