import socket
import time

def processOperand(response):
    pass

def processOperation(response):
    pass

def updateGUI(queue, response):
    queue.put({'set_text': response})



def masterProcess(host_addr, queue, emoji_list):
    classes = {
           0  :  "0_front",
           1  :  "0_back",
           2  :  "1_front",
           3  :  "1_back",
           4  :  "2_thumb_front",
           5  :  "2_thumb_back",
           6  :  "2_front",
           7  :  "2_back",
           8  :  "3_thumb_front",
           9  :  "3_thumb_back",
           10 :  "3_front",
           11 :  "3_back",
           12 :  "4_front",
           13 :  "4_back",
           14 :  "5_front",
           15 :  "5_back",
           16 :  "+_right_up_right_front",
           17 :  "+_right_up_left_front",
           18 :  "minus",
           19 :  "ok_3_fingers",
           20 :  "ok_thubm_up",
           21 :  "not_ok_thumb_down",
           22 :  "equals",
           23 :  "fck_u"
           }

    while True:
        time.sleep(0.5)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(host_addr)
    #    print("n of sent bytes:", bytes_sent)
        response = s.recv(1024)
        print(response)
        updateGUI(queue, response)

        # here you need to not take the same symbol every time
        s.close()
    
