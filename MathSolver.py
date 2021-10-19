# This is a sample Python script.
import numexpr
import serial
import time
import socket

localIP = "192.168.234.232"
localPort = 5001
bufferSize = 1024
msgFromServer = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")
# Listen for incoming datagrams
#INIT SERIAL
lastWrittenInputString = ""
lastOutputstringToArduino = ""
arduinoConnected = True
if arduinoConnected:
    ComPort = 'COM4'
    arduino = serial.Serial(port=ComPort, baudrate=9600, timeout=.1)
    time.sleep(4)

# determine if the Input is a number, operator or unkown
def getInputType(i):
    if i=="0" or i == "1" or i == "2" or i == "3" or i == "4" or i == "5" or i == "6" or i == "7" or i == "8" or i == "9" or i == "10":
        output = "number"
    elif i == "+" or i == "-" or i == "=" or i == "" or i == "x":
        output = "operator"
    else:
        output = "unknownType"
    return output


# This function is called when the image detection recognises a sign or a number
def newInput(currentInputString):
    global lastOutputstringToArduino
    global lastWrittenInputString
    #print("new inout rec")
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
        print("= " + str(ans))
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
    x = bytes(x_in, 'utf-8')
    if arduinoConnected:
        arduino.write(x)
    print(x)


def closePyserial():
    if arduinoConnected:
        arduino.close()

while (True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
   # clientMsg = "Message from Client:{}".format(message)
    clientMsg = message.decode('utf-8')
    #clientIP = "Client IP Address:{}".format(address)
    print(clientMsg)
    newInput(clientMsg)
    #print(clientIP)
    # Sending a reply to client
    #UDPServerSocket.sendto(bytesToSend, address)

"""
from Intepretur import *

ConnectToArduino()
newInput("1")
newInput("+")
newInput("1")
newInput("=")

"""



# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
"""'
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

"""


