# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numexpr
import serial
import time

# Set the ComPort of the Arduino here
arduinoConnected = False

if arduinoConnected:
    ComPort = 'COM6'
    arduino = serial.Serial(port=ComPort, baudrate=9600, timeout=.1)
    time.sleep(4)

# global Variables
lastWrittenInputString = ""
lastOutputstringToArduino = ""

# determine if the Input is a number, operator or unkown
def getInputType(i):
    if i =="1" or i =="2" or i=="3" or i == "4" or i == "5" or i == "6" or i == "7" or i == "8" or i == "9" or i == "10":
        output = "number"
    elif i == "+" or  i == "-" or i == "=" or i == "" or i == "x":
        output = "operator"
    else:
        output = "unknownType"
    return output

# This function is called when the image detection recognises a sign or a number
def newInput(currentInputString):
    global lastOutputstringToArduino
    global lastWrittenInputString
    
    currentInputStringSymbolType = getInputType(currentInputString)
    lastInputStringSymbolType = getInputType(lastWrittenInputString)
    
    # Check if the symbol has changed
    if currentInputStringSymbolType != lastInputStringSymbolType:
        if lastInputStringSymbolType == "unknownType":
            write = False
        else:
            write = True
    else:
        write = False
    
    # If the symbol has changed then write the last symbol to the golal Outputstring
    if write:        
        lastOutputstringToArduino = lastOutputstringToArduino + lastWrittenInputString
        
    # Evaluation of equal sign
    if currentInputString == "=":
        ans = numexpr.evaluate(lastOutputstringToArduino)
        
        if ans > 5:
            ans = 5
        elif ans < 0:
            ans = 0
        print("= " + str(ans) )
        message = str(ans)
        writeToArduino(message)
        lastOutputstringToArduino = ""
        lastWrittenInputString = ""
        currentInputString = ""
    
    # Reset sign from Input
    if currentInputString == "x":
        lastWrittenInputString = ""
        lastOutputstringToArduino = ""
    
    print(lastOutputstringToArduino + currentInputString)
    lastWrittenInputString = currentInputString
    return

def writeToArduino(x_in):
    print(x_in)
    x_in = "({" + x_in + "})"
    x = bytes(x_in,'utf-8')
    if arduinoConnected:
        arduino.write(x)
    print(x)
    
def closePyserial():
    if arduinoConnected:
        arduino.close()
    

#Markos Skript
newInput("1")
newInput("+")
newInput("2")
newInput("=")
print("Sol sould be 3")

newInput("10")
newInput("+")
newInput("2")
newInput("=")
print("Sol sould be 5")

newInput("1")
newInput("+")
newInput("1")
newInput("-")
newInput("=")
print("Sol sould be 2")

closePyserial()




