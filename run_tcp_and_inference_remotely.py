import sys
from multiprocessing import Process, Value, Array, Queue, Lock
from inferenceProcess import inferenceProcess
from serverProcess import serverProcess
from masterProcess import masterProcess
from gui import GUI

import tkinter as tk

# you need to call tkinter at the end of main
# because it needs to be in main
# thankfully, the rest is already separated into its own thing
# COMUNICATE VIA multiprocessing.Queue, it's a blocking call 
# and is way more convenient than sockets (and since this
# is 100% local, there's no need for sockets)

# the way to add an event to tkinter event loop is demonstrated in:
# ~/programs/tkinter_exact_scenarion_i_want_alternative.py



if __name__ == "__main__":
    # init shared variables into shared memory
    # NOTE if remote you need to start inference_- and server_processes 
    # by calling ssh user@host -e 'python script_that_starts_those_two' (or whatever flag for the command)
    # TODO use proper arg parser and actually write the remote part of the code
#    if sys.argv[1] == "remote":
#        remote = True
#    else:
#        remote = False
    likeliestClass = Value('i', 0)
    classCounter = Array('i', [0 for i in range(24)])
    inferenceLock = Lock()

    # this is used to communicate between the master and gui processes
    
    # init inference process 
    #inference_process = Process(target=inferenceProcess, args=(likeliestClass, classCounter, ))
    inference_process = Process(target=inferenceProcess, args=(likeliestClass, classCounter, inferenceLock))
    inference_process.daemon = True
    inference_process.name = "inference"

    # set things up for the server process
    host = ''
    port = 7777
    host_addr = (host, port)
    server_process = Process(target=serverProcess, args=(host_addr, likeliestClass, classCounter, inferenceLock))
    server_process.name = "tcp_server"
    server_process.daemon = True


    # start the processes
    inference_process.start()
    time.sleep(0.5)
    server_process.start()

    inference_process.join()
    server_process.join()

