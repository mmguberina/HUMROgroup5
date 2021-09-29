import cv2
import numpy as np
#import datetime
from utils import *
import time

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
       22  : "equals"
        }



frameShape = {'height' : 0, 'width': 0}
NUM_FRAMES_START = 150
user = "marko"
dataPoint_index = 0


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
    rectangleCoordinates = {'top': TOP_START, 
                            'right': RIGHT_START, 
                            'bottom': BOTTOM_START, 
                            'left': LEFT_START}
    # this is needed to keep track of the time
    # but also when saving the images
    num_frames = 0

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
            showMessage("lookin' good! get comfy :)", clone, frameShape)

        # warm up the user
        if num_frames >= 50 and num_frames < 150:
            showMessage("follow the rectangle! start with " + str(classes[currentClass]), 
                    clone, frameShape)

        # before starting, show an example image
        # TODO take a picture of your hand showing each example
        if num_frames >= NUM_FRAMES_START:
            showMessage("show " + classes[currentClass] + " in rectangle",
                        clone, frameShape)
            # this works
            #moveRectangleLeft(rectangleCoordinates, 1)
            # this is in testing
            doACounterClockwiseCircle(rectangleCoordinates, frameShape)

            # we're done with a class if the rectangle went back to the upper right corner
            if rectangleCoordinates['top'] == BORDER_LIMIT \
                    and rectangleCoordinates['left'] == frameShape['width'] - BORDER_LIMIT:
                if currentClass < len(classes):
                    currentClass += 1
                    rectangleCoordinates = updateRectangleShape(currentClass, rectangleCoordinates)

                    print("CHANGE!!:")
                    print("show " + classes[currentClass] + " in rectangle")
                    showMessage("show " + classes[currentClass] + " in rectangle",
                                clone, frameShape)
                    cv2.imshow("Video Feed", clone)
                    time.sleep(2)
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

        num_frames += 1
        cv2.imshow("Video Feed", clone)




        # maybe use this for further hacking as  well?
        # observe the keypress by the user
        keypress = cv2.waitKey(1) & 0xFF

        # if the user pressed "q", then stop looping
        if keypress == ord("q"):
            break


    # free up memory 'cos why not be nice
    camera.release()
    cv2.destroyAllWindows()
