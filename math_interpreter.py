# IP ADDRESS (line 8) and COM PORT (Line 23) need to updated for each new machine
import numexpr
import serial
import time
import socket

#localIP = "192.168.234.232"
localIP = "127.0.0.1"
localPort = 5001
bufferSize = 1024
# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

#INIT SERIAL
lastWrittenInputString = ""
lastOutputstringToArduino = ""
arduinoConnected = True
if arduinoConnected:
    ComPort = 'COM4'
    arduino = serial.Serial(port=ComPort, baudrate=9600, timeout=0.1)
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

    if (currentInputString=="O"):
        writeToArduino(currentInputString)
        return
    elif (currentInputString == "X"):
        writeToArduino("5")
        return


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
   # print(x_in)
    x_in = "({" + x_in + "})"
    x = bytes(x_in, 'utf-8')
    if arduinoConnected:
        arduino.write(x)
   # print(x)


def closePyserial():
    if arduinoConnected:
        arduino.close()

while (True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    clientMsg = message.decode('utf-8')
    print(clientMsg)
    newInput(clientMsg)







