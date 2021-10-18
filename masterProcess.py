import socket
import time

def masterProcess(host_addr):
    while True:
        time.sleep(1)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(host_addr)
    #    print("n of sent bytes:", bytes_sent)
        response = s.recv(1024)

        # here you need to not take the same symbol every time
        print("received response:", response)
        s.close()
    
