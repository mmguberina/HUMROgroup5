import cv2

def getClasses():
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
    return classes

def updateRectangleManually(rectangleCoordinates):
    doneAdjusting = False
    keypress = cv2.waitKey(1) & 0xFF
    
    if keypress == ord("h"):
        rectangleCoordinates['right'] -= 1
    if keypress == ord("j"):
        rectangleCoordinates['bottom'] +=1
    if keypress == ord("k"):
        rectangleCoordinates['bottom'] -= 1
    if keypress == ord("l"):
        rectangleCoordinates['right'] += 1
    
    if keypress == ord("y"):
        doneAdjusting = True

    return rectangleCoordinates, doneAdjusting

       

def showMessage(message, cloned_image, frameShape):
    cv2.putText(cloned_image, message, 
                (int(frameShape['width']/10), int(frameShape['height']/10)), cv2.FONT_HERSHEY_SIMPLEX, 
                0.7, (0,0,255), 2)

def saveImageAndLabel(user, currentClass, dataPoint_index, frame, rectangleCoordinates, frameShape):

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
    rectangle_width = abs(rectangleCoordinates['right'] - rectangleCoordinates['left']) \
                    / frameShape['width']
    rectangle_width = round(rectangle_width, 6)
    rectangle_height = abs(rectangleCoordinates['bottom'] - rectangleCoordinates['top']) / frameShape['height']
    rectangle_height = round(rectangle_height, 6)
    labelFile.write(str(currentClass) + " " + str(x_center) + " " + str(y_center)  + " " + str(rectangle_width)
                         + " " + str(rectangle_height))
    labelFile.close()


def moveRectangleLeft(rectangleCoordinates, amount):
    rectangleCoordinates['right'] -= amount
    rectangleCoordinates['left'] -= amount
    return rectangleCoordinates


def moveRectangleRight(rectangleCoordinates, amount):
    rectangleCoordinates['right'] += amount
    rectangleCoordinates['left'] += amount
    return rectangleCoordinates

def moveRectangleDown(rectangleCoordinates, amount):
    rectangleCoordinates['top'] += amount
    rectangleCoordinates['bottom'] += amount
    return rectangleCoordinates


def moveRectangleUp(rectangleCoordinates, amount):
    rectangleCoordinates['top'] -= amount
    rectangleCoordinates['bottom'] -= amount
    return rectangleCoordinates


def doACounterClockwiseCircle(rectangleCoordinates, frameShape, borderLimits, offset):
    conditionGoLeft = rectangleCoordinates['top'] <= borderLimits['top'] \
                        and rectangleCoordinates['left'] > borderLimits['left']

    conditionGoDown = rectangleCoordinates['bottom'] < frameShape['height'] - borderLimits['top'] \
                        and rectangleCoordinates['left'] <= borderLimits['left']

    conditionGoRight = rectangleCoordinates['bottom'] >= frameShape['height'] - borderLimits['top'] \
                        and rectangleCoordinates['right'] < frameShape['width'] - borderLimits['left']

    conditionGoUp = rectangleCoordinates['top'] > borderLimits['top'] \
                        and rectangleCoordinates['right'] >= frameShape['width'] - borderLimits['left']

    if conditionGoLeft:
        moveRectangleLeft(rectangleCoordinates, offset)

    if conditionGoDown:
        moveRectangleDown(rectangleCoordinates, offset)

    if conditionGoRight:
        moveRectangleRight(rectangleCoordinates, offset)

    if conditionGoUp:
        moveRectangleUp(rectangleCoordinates, offset)

    return rectangleCoordinates
