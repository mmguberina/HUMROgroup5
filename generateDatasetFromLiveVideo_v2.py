import cv2
#import numpy as np
#import datetime
from utils_v2 import *


""" 
TODO
    # this rectangle going in a circle thing is stupid and broken
    # and debbuging it is a pain in the ass
    # that is because it is a stupid approach
    # futhermore it generates a limited set of data
    # and it goes around only in 1 shape
    # all in all it is stupid and bad on at least 2 levels
    
    # a new NEW APPROACH is to choose a point
    # and then draw the rectangle so that that point is its center
    # then you can easily check whether the point is valid
    # and you can check the rectangle position validity before drawing it.
    # no online checking, no idiotic uncessary run-time errors.
    # also, you can very easily tell the user where to go by
    # drawing all of the points of the path
    # and that way you also get arbitrary paths for free.
    # not only that, you can resize the rectangle easily while
    # keeping the aspect ratio intact!
    # thus you solve the problem of different distances for free as well
    
    # here we interpret classes in the broadest possible sense.
    # this is done as it that approach may lead to better performance, idk.
    # the labels and names can be easily changed to be the same with a simple script
    # but of course that can't be done in reverse.
"""

# set/declare the global variables
classes = getClasses()

frameShape = {'height' : 0, 'width': 0}
NUM_FRAMES_START = 150
user = input("Please enter you name: ")
dataPoint_index = 0
rectangleBoundaries = {}

completedAClass = False
currentClass = 0

# this one gets the /dev/video0 camera
#camera = cv2.VideoCapture(0)
# NOTE reading from ip works! you just need to check that the ip is right
# and that the ip is correct
#camera = cv2.VideoCapture("http://192.168.43.1:8080/video")
camera = cv2.VideoCapture("http://192.168.1.5:8080/video")

# these are the starting coordinates
# NOTE top and left determine the boudaries of the traced out path
# so ajust that if you want a bigger/smaller path 
rectangleCoordinates = {'top': 10, 
                        'right': 150, 
                        'bottom': 150, 
                        'left': 10}

borderLimits = {'top' : rectangleCoordinates['top'],
                'left' : rectangleCoordinates['left']}

offset = 2

num_frames = 0
newClassRectangleInit = False
numFramesToPause = 0
doneAdjusting = False

while(True):
    (grabbed, frame) = camera.read()
   
    # NOTE don't do this if holding the phone in front of you!
    frame = cv2.flip(frame, 1)
    clone = frame.copy()
    (frameShape['height'], frameShape['width']) = frame.shape[:2]
    


    # display intro message 
    if num_frames < 50:
        showMessage("lookin' good! get comfy :)", clone, frameShape)

    # adjust rectangle
    if num_frames >= 50 and not newClassRectangleInit:
        showMessage("ajust the rentangle for " + classes[currentClass] + " with h/j/k/l, do y if done" + str(classes[currentClass]), 
                clone, frameShape)
        rectangleCoordinates, doneAdjusting = updateRectangleManually(rectangleCoordinates)

        rectangleInFrame = True
        if rectangleCoordinates['bottom'] > frameShape['height']:
            showMessage("you went out of frame with bottom!", 
                clone, frameShape)
            rectangleInFrame = False
        if rectangleCoordinates['right'] > frameShape['width']:
            showMessage("you went out of frame with right!", 
                clone, frameShape)
            rectangleInFrame = False

        if doneAdjusting and rectangleInFrame:
            newClassRectangleInit = True
            numFramesAtInit = num_frames


    # before starting, show an example image
    # TODO take a picture of your hand showing each example
    #if num_frames >= 50 and newClassRectangleInit:
    if newClassRectangleInit:
        showMessage("show " + classes[currentClass] + " in rectangle",
                    clone, frameShape)
        rectangleCoordinates = doACounterClockwiseCircle(rectangleCoordinates, frameShape, borderLimits, offset)

        # we're done with a class if the rectangle went back to the upper right corner
        if (num_frames > numFramesAtInit + 2
                and 
                rectangleCoordinates['top']  <= borderLimits['top'] 
                and 
                rectangleCoordinates['left'] <= borderLimits['left']):

            if currentClass < len(classes):
                currentClass += 1

                print("CHANGE!!:")
                print("show " + classes[currentClass] + " in rectangle")
                showMessage("show " + classes[currentClass] + " in rectangle",
                            clone, frameShape)
                newClassRectangleInit = False
            else:
                print("This data recording session is done! Thanks for your time!")
                break


            # write image and label file to disc in ./dataset
        if num_frames % 5 == 0:
            saveImageAndLabel(user, currentClass, dataPoint_index, frame, rectangleCoordinates, frameShape)
            dataPoint_index = dataPoint_index + 1


    # draw the rectangle
    cv2.rectangle(clone, (rectangleCoordinates['left'], rectangleCoordinates['top']),
                        (rectangleCoordinates['right'], rectangleCoordinates['bottom']),
                        (0,255,0), 2)
    num_frames += 1
    cv2.imshow("Video Feed", clone)
    cv2.waitKey(1)




# free up memory 'cos why not be nice
camera.release()
cv2.destroyAllWindows()
