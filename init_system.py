import time
from multiprocessing import Process, Value, Array
from inferenceProcess import inferenceProcess
from serverProcess import serverProcess
from masterProcess import masterProcess



if __name__ == "__main__":
    # init shared variables into shared memory
    likeliestClass = Value('i', 9)
    classCounter = Array('i', [0 for i in range(24)])
    
    # init inference process 
    inference_process = Process(target=inferenceProcess, args=(likeliestClass, classCounter,))
    inference_process.daemon = True
    inference_process.name = "inference"


    # set things up for the server process
    host = ''
    port = 7777
    host_addr = (host, port)
    server_process = Process(target=serverProcess, args=(host_addr, likeliestClass, classCounter,))
    server_process.name = "tcp_server"
    server_process.daemon = True

    # set up master process
    master_process = Process(target=masterProcess, args=(host_addr,))
    master_process.name = "master"

    # start the processes
    inference_process.start()
    server_process.start()
    time.sleep(0.2)
    master_process.start()

    # run the gui process
    # run the master process here


    # and now do nothing
    inference_process.join()
    masterProcess.join()
    server_process.join()

