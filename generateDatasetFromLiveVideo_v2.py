import cv2
#import numpy as np
#import datetime
from utils_v2 import *



# set/declare the global variables
classes = getClasses()

frameShape = {'height' : 0, 'width': 0}
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
doneAdjusting = False

while(True):
    (grabbed, frame) = camera.read()
   
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
        rectangleCoordinates, doneAdjusting = updateRectangleManually(rectangleCoordinates, offset)

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
