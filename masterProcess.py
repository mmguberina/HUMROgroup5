import socket
import time
from translation_utils import *

def processOperand(response):
    pass

def processOperation(response):
    pass

# maintain state of text here
def updateGUI(queue, symbol, currentTextInLabel):

    if type(symbol) == int or symbol == "+" or symbol == "-" or symbol == "=":
        currentTextInLabel += " " + str(symbol)
        set_image = 'thinking'

    if symbol == "thumb_up":
        set_image = 'thumb_up'
        currentTextInLabel = ""

    if symbol == "ok":
        set_image = 'smile'
        currentTextInLabel = ""

    if symbol == "not_ok":
        set_image = 'terror'
        currentTextInLabel = ""



#'sleep'  ---> add some counter and the set that in gui

    queue.put({'set_text': currentTextInLabel,
                'set_image': set_image})



    #TODO  if not this, then error, send 0 for now
    return currentTextInLabel

def masterProcess(host_addr, queue, emoji_list):
    classes = getClasses()
    # hand socket thing can be here for all we care

    localIP     = "192.168.234.232"
    localPort   = 5001
    bufferSize  = 1024
    hand_server_addr = (localIP, localPort)

    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    host_middle = "46.239.113.170"
    host_middle_port = 7777
    host_middle_addr = (host_middle, host_middle_port)

    currentTextInLabel = ""

    while True:
#        time.sleep(0.5)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(host_addr)
    #    print("n of sent bytes:", bytes_sent)
        response = s.recv(1024)
        print(response)
        translated_to_symbol = translation_table(int(response), "robot_hand")
        robot_hand_symbol = bytes(str(translated_to_symbol), 'utf-8')
        UDPClientSocket.sendto(robot_hand_symbol, hand_server_addr)
        translated_to_symbol_for_gui = translation_table(int(response), "gui")

        currentTextInLabel = updateGUI(queue, translated_to_symbol_for_gui, currentTextInLabel)

        # NOTE send this to remote middle-server
#        socket_to_middle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        socket_to_middle.connect(host_middle_addr)
#        indentifier = bytes("master:", 'utf-8')
#        socket_to_middle.send(indentifie + response)
#        socket_to_middle.close()
    #    print("n of sent bytes:", bytes_sent)
        


        # here you need to not take the same symbol every time
        s.close()
    
