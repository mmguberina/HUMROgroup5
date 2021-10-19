import tkinter as tk
import threading
from PIL import ImageTk, Image
from multiprocessing import Queue
import time
import random
#import os


class GetCommandThread(threading.Thread):
    def __init__(self, queue, localQueue, _check):
        super(GetCommandThread, self).__init__()
        self.queue = queue
        self.localQueue = localQueue
        self._check = _check

    def run(self):
        print("worker thread doing stuff")
        commands = self.queue.get()
        # maybe just wait untill it's non-empty with another blocking call?
        # then .get() from the main thread
        self.localQueue.put(commands)
#        if random.randint(0, 1) == 0:
#            self.localQueue.put({'set_image': 'smile', 'set_text': "ready to work" })
#        else:
#            self.localQueue.put({'set_image': 'thumb_up', 'set_text': "updated" })

        if self._check.get() == 0:
            self._check.set(1)
        #    print('registered new callback')
        else:
            self._check.set(0)
        #    print('registered new callback')


class GUI:
    def __init__(self, root, queue, emojis):
        self.root = root
        self.queue = queue
        self.localQueue = Queue()
#        self.localQueue.put({'set_image': 'smile', 'set_text': "Ready to Work!" })
        # load the images
        self.emojis = {}
#        pathToMe = os.getcwd() + "/"
        for emoji in emojis:
            self.emojis[emoji] = ImageTk.PhotoImage(Image.open(emojis[emoji]))
        
        # create image and text labels
        self.imageLabel = tk.Label(root, image=self.emojis['smile'])
        self.textLabel = tk.Label(root, text="Ready to Work!")
        
        # add a quit button
        self.quit_button = tk.Button(self.root, text="Quit", bg="#5E99FF", fg="#ffffff", command=self.root.destroy) 

        # hack socket reading into the event loop
        # thinking about this, i could just trigger on image change [ upside smile emoji ]
        self._check = tk.IntVar(value=0)                                                                       
        self._check.trace_add('write', self.callback) #kepp track of that variable and trigger callback if changed
        self.imageLabel.pack()
        self.textLabel.pack()
        self.quit_button.pack()
        self.callback() # start the loop
       
        # NOTE we can get away with just pack here (but possibly put it on a grid to
        # make it look better)


    def setImage(self, imageName):
        self.imageLabel.configure(image=self.emojis[imageName])
        self.imageLabel.image = self.emojis[imageName]
    
    def setText(self, textString):
        self.textLabel.configure(text=textString)
    
    
    def callback(self, event=None, *args):
        if not self.localQueue.empty():
            commands = self.localQueue.get()
            print(commands)
            # get commands here
            if 'set_image' in commands:
                self.setImage(commands['set_image'])
            if 'set_text' in commands:
                self.setText(commands['set_text'])
        
        #print("started thread")
        getCommandThread = GetCommandThread(self.queue, self.localQueue, self._check)
        getCommandThread.start()


# start this from init_system
if __name__ == "__main__":
    queue = Queue()

    emojis = {
            'sleep' : "./emojis/sleep_emoji.png",  
            'smile' : "./emojis/smile_emoji.png",  
            'terror' : "./emojis/terror_emoji.png",  
            'thinking' :"./emojis/thinking_emoji.png", 
            'thumb_up' : "./emojis/thumb_up_emoji.png",
            'crying' : "./emojis/crying_emoji.png"
            }

    root = tk.Tk()
    gui = GUI(root, queue, emojis)
    
    root.mainloop()
