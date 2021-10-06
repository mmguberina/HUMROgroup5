import cv2
#import numpy as np
#import datetime
from utils import *
import time
# TODO remove after done debugging
import pdb

## TODO
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
classes = {
       0  : "0_front",
       1  : "0_back",
       2  : "1_front",
       3  : "1_back",
       4  : "2_thumb_front",
       5  : "2_thumb_back",
       6  : "2_front",
       7  : "2_back",
       8  : "3_thumb_front",
       9  : "3_thumb_back",
       10 : "3_front",
       11 : "3_back",
       12 : "4_front",
       13 : "4_back",
       14  : "5_front",
       15  : "5_back",
       16  : "+_right_up_right_front",
       17  : "+_right_up_left_front",
       18  : "minus",
       19  : "ok_3_fingers",
       20  : "ok_thubm_up",
       21  : "not_ok_thumb_down",
       22  : "equals",
       23  : "fck_u"
        }



frameShape = {'height' : 0, 'width': 0}
NUM_FRAMES_START = 1500
user = input("Please enter you name: ")
dataPoint_index = 0
rectangleBoundaries = {}


if __name__ == "__main__":

    completedAClass = False
    currentClass = 0
    # this one gets the /dev/video0 camera
    camera = cv2.VideoCapture(0)
    # reading from ip works! you just need to check that the ip is right
    # and that the ip is correct
    #camera = cv2.VideoCapture("http://192.168.43.1:8080/video")
    
    # these need to be updated
    # also they need to be scaled according to the number of pixels
    # NOTE LEFT AND RIGHT ARE FLIPPED FOR WHATEVER REASON!!!!!!!!!!!!
    rectangleCoordinates = {'top': 0, 
                            'right': 0, 
                            'bottom': 0, 
                            'left': 0}
    #rectangleCoordinates = updateRectangleShapeViaPercentages(0, rectangleCoordinates, 
    # this is needed to keep track of the time
    # but also when saving the images
    num_frames = 0


    newClassRectangleInit = False
    numFramesToPause = 0
    while(True):
        (grabbed, frame) = camera.read()
        # possibly we'll need to resize the frame
        #frame = imutils.resize(frame, width=700)
       
        # don't do this if holding the phone in front of you!
        frame = cv2.flip(frame, 1)
        # if a copy a the frame is needed do it now
        clone = frame.copy()
        # get the height and width of the frame
        (frameShape['height'], frameShape['width']) = frame.shape[:2]
        

        # get the rectangle
        cv2.rectangle(clone, (rectangleCoordinates['left'], rectangleCoordinates['top']),
                            (rectangleCoordinates['right'], rectangleCoordinates['bottom']),
                            (0,255,0), 2)

        # display intro message 
        if num_frames < 50:
            if num_frames == 0:
                rectangleCoordinates = updateRectangleShapeViaPercentages(currentClass, rectangleCoordinates, frameShape)
            showMessage("lookin' good! get comfy :)", clone, frameShape)

        # warm up the user
        if num_frames >= 50 and num_frames < NUM_FRAMES_START - 1:
            showMessage("follow the rectangle! start with " + str(classes[currentClass]), 
                    clone, frameShape)

        # before starting, show an example image
        # TODO take a picture of your hand showing each example
        if num_frames >= NUM_FRAMES_START:
            print("rectangleCoordinates", rectangleCoordinates)
            print("rectangleBoundaries", rectangleBoundaries)
            
            showMessage("show " + classes[currentClass] + " in rectangle",
                        clone, frameShape)
            if not newClassRectangleInit:
                if numFramesToPause == 0:
                    numFramesToPause = 30 
                    (rectangleCoordinates, rectangleBoundaries) = updateRectangleManually(currentClass, rectangleCoordinates, frameShape)

            else:
                rectangleCoordinates = doACounterClockwiseCirclePerc(rectangleCoordinates, frameShape, rectangleBoundaries)
    
                # we're done with a class if the rectangle went back to the upper right corner
                if num_frames > NUM_FRAMES_START + 10 and rectangleCoordinates['top'] / frameShape['width'] <= rectangleBoundaries['BORDER_LIMIT_WIDTH_PERC'] \
                        and rectangleCoordinates['left']  / frameShape['width'] >= 1 - rectangleBoundaries['BORDER_LIMIT_WIDTH_PERC']:
                    if currentClass < len(classes):
                        currentClass += 1
    
                        print("CHANGE!!:")
                        print("show " + classes[currentClass] + " in rectangle")
                        showMessage("show " + classes[currentClass] + " in rectangle",
                                    clone, frameShape)
                        cv2.imshow("Video Feed", clone)
                        newClassRectangleInit = False
                    else:
                        print("This data recording session is done! Thanks for your time!")
                        break

    
                # write to file
                if num_frames % 5 == 0:
                    # enable when ready to roll, let's not clog system memory just yet
                    cv2.imwrite("./dataset/" + user + "_" + str(currentClass)  + "_" + str(dataPoint_index) + ".png", frame)
                    # immediately write the appropriate label file
                    # it should have the same name as the picture name and the following content:
                    # <object-class> <x_center> <y_center> <width> <height>
                    # object class is the 0 - (Nclasses - 1) class index
                    # the rest are floats 0 - 1, describing position relative to image shape
                    # x_ and y_center are centerOfRectangle / int_widthOfImageInPixels 
                    # and int_heightOfImageInPixels respectively 
                    # and width and height are for the rectangle and are calculated like the center
                    labelFile = open("./dataset/" + user + "_" + str(currentClass)  + "_" + str(dataPoint_index) + ".txt", "w+")
                    x_center = ((rectangleCoordinates['left'] + rectangleCoordinates['right']) / 2.0)  \
                                    / frameShape['width']
                    x_center = round(x_center, 6)
                    y_center = ((rectangleCoordinates['top'] + rectangleCoordinates['bottom']) / 2.0)  \
                                    / frameShape['height']
                    y_center = round(y_center, 6)
                    rectangle_width = (rectangleCoordinates['left'] - rectangleCoordinates['right']) \
                                    / frameShape['width']
                    rectangle_width = round(rectangle_width, 6)
                    rectangle_height = (rectangleCoordinates['bottom'] - rectangleCoordinates['top']) / frameShape['height']
                    rectangle_height = round(rectangle_height, 6)
                    labelFile.write(str(currentClass) + " " + str(x_center) + " " + str(y_center)  + " " + str(rectangle_width)
                                         + " " + str(rectangle_height))
                    labelFile.close()
    
                    # update index
                    dataPoint_index = dataPoint_index + 1
            if not newClassRectangleInit:
                numFramesToPause -= 1
                if numFramesToPause == 0:
                    inputed = input("Are you satisfied with the triangle shape[Y/n]?")
                    if inputed == "Y" or inputed == "y":
                        newClassRectangleInit = True
                    else:
                        numFramesToPause = 30



        num_frames += 1
        cv2.imshow("Video Feed", clone)




        # maybe use this for further hacking as  well?
        # observe the keypress by the user
        keypress = cv2.waitKey(1) & 0xFF

        # if the user pressed "q", then stop looping
        #if keypress == ord("q"):
        #    break

        if keypress == ord("h"):
        #    rectangleBoundaries['RIGHT_START_PERC'] -= 0.01
            rectangleCoordinates['right'] -= 1
        if keypress == ord("j"):
        #    rectangleBoundaries['BOTTOM_START_PERC'] += 0.01
            rectangleCoordinates['bottom'] +=1
        if keypress == ord("k"):
        #    rectangleBoundaries['TOP_START_PERC'] -= 0.01
            rectangleCoordinates['top'] -= 1
        if keypress == ord("l"):
        #    rectangleBoundaries['LEFT_START_PERC'] += 0.01
            rectangleCoordinates['left'] += 1


    # free up memory 'cos why not be nice
    camera.release()
    cv2.destroyAllWindows()
