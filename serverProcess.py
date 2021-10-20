import threading
import socket

class ClientHandler(threading.Thread):
    def __init__(self, comm_socket, likeliestClassValue):
        super(ClientHandler, self).__init__()
        self.comm_socket = comm_socket
        self.likeliestClassValue = likeliestClassValue

    def run(self):
        #print("started thread")
        data = self.comm_socket.send(bytes(str(self.likeliestClassValue), "utf-8"))
        self.comm_socket.close()


#def serverProcess(host_addr, likeliestClass, classCounter):
def serverProcess(host_addr, likeliestClass, classCounter, inferenceLock):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(host_addr)
    s.listen()
    print("server listening on", host_addr)
    while True:
        comm_socket, comm_addr = s.accept()
        # read likeliest class
        inferenceLock.acquire()
        likeliestClass.acquire()
        likeliestClassValue = likeliestClass.value
        likeliestClass.release()
        inferenceLock.release()

        # clean the counter as we're now going to infer the next symbol
        classCounter.acquire()
        for i in range(len(classCounter)):
            classCounter[i] = 0
        classCounter.release()
        handler_thread = ClientHandler(comm_socket, likeliestClassValue)
        handler_thread.start()
