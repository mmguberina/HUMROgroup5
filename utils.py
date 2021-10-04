import cv2
# rectangle coordinates are the following
#rectangleCoordinates = {'top': t, 
#                       'right': r, 
#                       'bottom': b, 
#                       'left': l}

#######################################
# macros go here for use of use
#####################################
#TOP_START = 10
#RIGHT_START = 350
#BOTTOM_START = 220
#LEFT_START = 590

TOP_START_PERC = 0.020833333333333332
RIGHT_START_PERC = 0.546875
BOTTOM_START_PERC = 0.4583333333333333
LEFT_START_PERC = 0.921875


#BORDER_LIMIT = 10

#BORDER_LIMIT_WIDTH_PERC = 0.02
BORDER_LIMIT_WIDTH_PERC = 0.03
BORDER_LIMIT_HEIGHT_PERC = 0.92
#BORDER_LIMIT_HEIGHT_PERC = 0.93


# NOTE these functions should have checks via assert
# so that they don't something stupid on accident
# (or just don't move if they cant)
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

def showMessage(message, cloned_image, frameShape):
    cv2.putText(cloned_image, message, 
                (int(frameShape['width']/10), int(frameShape['height']/10)), cv2.FONT_HERSHEY_SIMPLEX, 
                0.7, (0,0,255), 2)


def doACounterClockwiseCircle(rectangleCoordinates, frameShape):
    conditionGoLeft = rectangleCoordinates['top'] <= TOP_START \
                        and rectangleCoordinates['bottom'] <= BOTTOM_START  \
                        and rectangleCoordinates['right'] > BORDER_LIMIT

    conditionGoDown = rectangleCoordinates['bottom'] < frameShape['height'] - BORDER_LIMIT \
                        and rectangleCoordinates['right'] <= BORDER_LIMIT 
                        #and rectangleCoordinates['left'] == BOTTOM_START + (LEFT_START - RIGHT_START)

    conditionGoRight = rectangleCoordinates['bottom'] >= frameShape['height'] - BORDER_LIMIT\
                        and rectangleCoordinates['left'] < frameShape['width'] - BORDER_LIMIT
                        # and rectangleCoordinates['top'] == BORDER_LIMIT + (BOTTOM_START - TOP_START)\

    conditionGoUp = rectangleCoordinates['top'] > BORDER_LIMIT \
                        and rectangleCoordinates['left'] >= frameShape['width'] - BORDER_LIMIT
                        #and rectangleCoordinates['right'] == frameShape['width'] - BORDER_LIMIT - (LEFT_START - RIGHT_START) \

    offset = 2
    if conditionGoLeft:
        moveRectangleLeft(rectangleCoordinates, offset)

    if conditionGoDown:
        moveRectangleDown(rectangleCoordinates, offset)

    if conditionGoRight:
        moveRectangleRight(rectangleCoordinates, offset)

    if conditionGoUp:
        moveRectangleUp(rectangleCoordinates, offset)


def doACounterClockwiseCirclePerc(rectangleCoordinates, frameShape, rectangleBoundaries):
#    print(rectangleCoordinates)
#    print("rectangleCoordinates['top'] /frameShape['height'] : ",   rectangleCoordinates['top'] /frameShape['height']   )
#    print("rectangleCoordinates['right'] /frameShape['width'] : ",  rectangleCoordinates['right'] /frameShape['width']  )
#    print("rectangleCoordinates['bottom'] /frameShape['height'] : ", rectangleCoordinates['bottom'] /frameShape['height'])
#    print("rectangleCoordinates['left'] /frameShape['width'] : ",  rectangleCoordinates['left'] /frameShape['width']   )

    conditionGoLeft = rectangleCoordinates['top'] / frameShape['height'] <= rectangleBoundaries['TOP_START_PERC'] \
                        and rectangleCoordinates['right'] / frameShape['width'] > rectangleBoundaries['BORDER_LIMIT_WIDTH_PERC']
                        #and rectangleCoordinates['bottom'] / frameShape['height'] <= rectangleBoundaries['BOTTOM_START_PERC']  \

    #conditionGoDown = rectangleCoordinates['bottom']  / frameShape['height'] < 1 - rectangleBoundaries['BORDER_LIMIT_HEIGHT_PERC'] \
    conditionGoDown = rectangleCoordinates['bottom']  / frameShape['height'] < 1 \
                        and rectangleCoordinates['right']  / frameShape['width'] <= rectangleBoundaries['BORDER_LIMIT_WIDTH_PERC']
                        #and rectangleCoordinates['left'] == BOTTOM_START + (LEFT_START - RIGHT_START)

    #conditionGoRight = rectangleCoordinates['bottom']  / frameShape['height'] >= 1 - rectangleBoundaries['BORDER_LIMIT_HEIGHT_PERC']\
    #                    and rectangleCoordinates['left']  / frameShape['width'] < 1 - rectangleBoundaries['BORDER_LIMIT_WIDTH_PERC']
    conditionGoRight = rectangleCoordinates['bottom']  / frameShape['height'] >= 1 \
                        and rectangleCoordinates['left']  / frameShape['width'] < 1
                        # and rectangleCoordinates['top'] == BORDER_LIMIT + (BOTTOM_START - TOP_START)\

    #conditionGoUp = rectangleCoordinates['top']  / frameShape['height'] > rectangleBoundaries['BORDER_LIMIT_HEIGHT_PERC'] \
    conditionGoUp = rectangleCoordinates['top']  / frameShape['height'] > 0\
                        and rectangleCoordinates['left']  / frameShape['width'] >= 1 - rectangleBoundaries['BORDER_LIMIT_WIDTH_PERC']
                        #and rectangleCoordinates['left']  / frameShape['width'] >= 1 - rectangleBoundaries['BORDER_LIMIT_WIDTH_PERC']
                        #and rectangleCoordinates['right'] == frameShape['width'] - BORDER_LIMIT - (LEFT_START - RIGHT_START) \

#    print("conditionGoLeft", conditionGoLeft)
#    print("conditionGoDown", conditionGoDown)
#    print("conditionGoRight", conditionGoRight)
#    print("conditionGoUp", conditionGoUp)

    offset = 6
    if conditionGoLeft:
        #print(rectangleCoordinates)
        rectangleCoordinates = moveRectangleLeft(rectangleCoordinates, offset)
        #print(rectangleCoordinates)

    if conditionGoDown:
        rectangleCoordinates = moveRectangleDown(rectangleCoordinates, offset)

    if conditionGoRight:
        rectangleCoordinates = moveRectangleRight(rectangleCoordinates, offset)

    if conditionGoUp:
        rectangleCoordinates = moveRectangleUp(rectangleCoordinates, offset)

    return rectangleCoordinates



def updateRectangleShape(currentClass, rectangleCoordinates, frameShape):
    if currentClass < 2:
        TOP_START_LOCAL = 10
        RIGHT_START_LOCAL = 350
        BOTTOM_START_LOCAL = 220
        LEFT_START_LOCAL = 590
    if currentClass >= 2 and currentClass <= 15:
        TOP_START_LOCAL = 10
        RIGHT_START_LOCAL = 350 + 100
        BOTTOM_START_LOCAL = 220
        LEFT_START_LOCAL = 590 
    if currentClass >= 16 and currentClass <= 17:
        TOP_START_LOCAL = 10
        RIGHT_START_LOCAL = 350
        BOTTOM_START_LOCAL = 220
        LEFT_START_LOCAL = 590
    if currentClass == 18:
        TOP_START_LOCAL = 10
        RIGHT_START_LOCAL = 350
        BOTTOM_START_LOCAL = 220 - 150
        LEFT_START_LOCAL = 590
    if currentClass >= 19 and currentClass <= 21:
        TOP_START_LOCAL = 10
        RIGHT_START_LOCAL = 350 + 100
        BOTTOM_START_LOCAL = 220
        LEFT_START_LOCAL = 590 
    if currentClass == 22:
        TOP_START_LOCAL = 10
        RIGHT_START_LOCAL = 350 
        BOTTOM_START_LOCAL = 220 - 100
        LEFT_START_LOCAL = 590 

    rectangleCoordinates = {'top': TOP_START_LOCAL, 
                            'right': RIGHT_START_LOCAL, 
                            'bottom': BOTTOM_START_LOCAL, 
                            'left': LEFT_START_LOCAL}
    return rectangleCoordinates
        

def updateRectangleShapeViaPercentages(currentClass, rectangleCoordinates, frameShape):
    if currentClass < 2:
        TOP_START_LOCAL_PERC = 0.020833333333333332
        RIGHT_START_LOCAL_PERC = 0.546875
        BOTTOM_START_LOCAL_PERC = 0.4583333333333333
        LEFT_START_LOCAL_PERC = 0.921875
    if currentClass >= 2 and currentClass <= 15:
        TOP_START_LOCAL_PERC = 0.020833333333333332
        RIGHT_START_LOCAL_PERC = 0.546875 + 0.15625
        BOTTOM_START_LOCAL_PERC = 0.4583333333333333
        LEFT_START_LOCAL_PERC = 0.921875 
    if currentClass >= 16 and currentClass <= 17:
        TOP_START_LOCAL_PERC = 0.020833333333333332
        RIGHT_START_LOCAL_PERC = 0.546875
        BOTTOM_START_LOCAL_PERC = 0.4583333333333333
        LEFT_START_LOCAL_PERC = 0.921875
    if currentClass == 18:
        TOP_START_LOCAL_PERC = 0.020833333333333332
        RIGHT_START_LOCAL_PERC = 0.546875
        BOTTOM_START_LOCAL_PERC = 0.4583333333333333 - 0.3125
        LEFT_START_LOCAL_PERC = 0.921875
    if currentClass >= 19 and currentClass <= 21:
        TOP_START_LOCAL_PERC = 0.020833333333333332
        RIGHT_START_LOCAL_PERC = 0.546875 + 0.15625
        BOTTOM_START_LOCAL_PERC = 0.4583333333333333
        LEFT_START_LOCAL_PERC = 0.921875 
    if currentClass == 22:
        TOP_START_LOCAL_PERC = 0.020833333333333332
        RIGHT_START_LOCAL_PERC = 0.546875
        BOTTOM_START_LOCAL_PERC = 0.4583333333333333 - 0.20833333333333334
        LEFT_START_LOCAL_PERC = 0.921875 
    
    # height / width
#    default_frame_shape = {'height' : 480, 'width' : 640}
#    #this_aspect_ration = frameShape['height'] / frameShape['width']
#    #height_fix = default_frame_shape['height'] / frameShape['height']
#    #width_fix = default_frame_shape['width'] / frameShape['width']
# TODO fix this
    height_fix = 1
    width_fix = 1
    #fix_right = frame
    #default_aspect_ratio = 0.75
    #currentAspectRation = frameShape['height'] / frameShape['width']
    #fix_my_ratio = default_aspect_ratio / currentAspectRation
    rectangleCoordinates = {'top': int(TOP_START_LOCAL_PERC * frameShape['height']) , 
                            'right': int(RIGHT_START_LOCAL_PERC * frameShape['width'] ), 
                            'bottom': int((BOTTOM_START_LOCAL_PERC / height_fix) * frameShape['height']), 
                            'left': int((LEFT_START_LOCAL_PERC / width_fix) * frameShape['width'])}
    return rectangleCoordinates


def updateRectangleManually(currentClass, rectangleCoordinates, frameShape):
    print("======================================================")
    print("You will now input the shape of the rectangle you want.")
    print("Each number is a float from 0 to 1 and denotes the percentage")
    print("of screen in the respective dimension. Top left corner")
    print("of the image is (0,0); numbers raise to left and bottom.")
    print("Be aware that you need to use '.' as the decimal delimiter.")
    success = False
    while(not success):
        inputed = input("TOP_START_PERCENTAGE: ")
        try:
            TOP_START_LOCAL_PERC = float(inputed)
            if float(inputed) < 0 or float(inputed) > 1:
                raise ValueError
        except ValueError:
            print("your previous input was not correct. try again")
            continue
        inputed = input("BOTTOM_START_PERCTAGE: ")
        try:
            BOTTOM_START_LOCAL_PERC = float(inputed)
            if float(inputed) < 0 or float(inputed) > 1:
                raise ValueError
        except ValueError:
            print("your previous input was not correct. try again")
            continue
        inputed = input("LEFT_START_PERCENTAGE: ")
        try:
            RIGHT_START_LOCAL_PERC = float(inputed)
            if float(inputed) < 0 or float(inputed) > 1:
                raise ValueError
        except ValueError:
            print("your previous input was not correct. try again")
            continue
        inputed = input("RIGHT_START_PERCENTAGE: ")
        try:
            LEFT_START_LOCAL_PERC = float(inputed)
            if float(inputed) < 0 or float(inputed) > 1:
                raise ValueError
        except ValueError:
            print("your input was not correct. try again")
            continue
        success = True
        break
    
    rectangleCoordinates = {'top': int(TOP_START_LOCAL_PERC * frameShape['height']) , 
                            'right': int(RIGHT_START_LOCAL_PERC * frameShape['width'] ), 
                            'bottom': int(BOTTOM_START_LOCAL_PERC * frameShape['height']), 
                            'left': int(LEFT_START_LOCAL_PERC * frameShape['width'])}
    # we need to update the global version of these variables as well
    # otherwise our conditions for going in circle are compromized
    rectangleBoundaries = {
    'TOP_START_PERC' : TOP_START_LOCAL_PERC,
    'RIGHT_START_PERC' : RIGHT_START_LOCAL_PERC,
    'BOTTOM_START_PERC' : BOTTOM_START_LOCAL_PERC,
    'LEFT_START_PERC' : LEFT_START_LOCAL_PERC,

    'BORDER_LIMIT_WIDTH_PERC' : 1 - RIGHT_START_PERC,
    'BORDER_LIMIT_HEIGHT_PERC' : 1 - TOP_START_PERC
    }
    return (rectangleCoordinates, rectangleBoundaries)
