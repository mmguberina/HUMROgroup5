import cv2 as cv
import argparse
import sys
import numpy as np
import os.path

# utility functions

# Get the names of the output layers
def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# Draw the predicted bounding box
def drawPred(frame, classes,classId, conf, left, top, right, bottom):
    # Draw a bounding box.
    #    cv.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 3)
    cv.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 3)

    label = '%.2f' % conf
        
    # Get the label for the class name and its confidence
    if classes:
        assert(classId < len(classes))
        label = '%s:%s' % (classes[classId], label)

    #Display the label at the top of the bounding box
    labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    top = max(top, labelSize[1])
    cv.rectangle(frame, (left, top - round(1.5*labelSize[1])), (left + round(1.5*labelSize[0]), top + baseLine), (0, 0, 255), cv.FILLED)
    #cv.rectangle(frame, (left, top - round(1.5*labelSize[1])), (left + round(1.5*labelSize[0]), top + baseLine),    (255, 255, 255), cv.FILLED)
    cv.putText(frame, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0), 2)

# Remove the bounding boxes with low confidence using non-maxima suppression
def postprocess(frame, classes, outs, confThreshold, nmsThreshold):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    classIds = []
    confidences = []
    boxes = []
    # Scan through all the bounding boxes output from the network and keep only the
    # ones with high confidence scores. Assign the box's class label as the class with the highest score.
    classIds = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    # Perform non maximum suppression to eliminate redundant overlapping boxes with
    # lower confidences.
    indices = cv.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    for i in indices:
        i = i[0]
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        drawPred(frame, classes, classIds[i], confidences[i], left, top, left + width, top + height)
    return classIds




def inferenceProcess(likeliestClass, classCounter):

    # Initialize the parameters
    confThreshold = 0.5  #Confidence threshold
    #confThreshold = 0.1  #Confidence threshold
    nmsThreshold = 0.4  #Non-maximum suppression threshold
    #nmsThreshold = 0.05  #Non-maximum suppression threshold
    
    inpWidth = 320  #608     #Width of network's input image
    inpHeight = 320 #608     #Height of network's input image
    
    parser = argparse.ArgumentParser(description='Object Detection using YOLO in OPENCV')
    parser.add_argument('--image', help='Path to image file.')
    parser.add_argument('--video', help='Path to video file.')
    parser.add_argument("--device", default="cpu", help="Device to inference on")
    args = parser.parse_args()
            
    # Load names of classes
    classesFile = "hand_gestures.names";
    
    classes = None
    with open(classesFile, 'rt') as f:
        classes = f.read().rstrip('\n').split('\n')
    
    # Give the configuration and weight files for the model and load the network using them.
    
    modelConfiguration = "./yolov4-tiny-hand_gestures.cfg";
    modelWeights = "../trained_nets/yolov4-tiny-hand_gestures_best.weights";
    
    net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
    if args.device == "cpu":
        net.setPreferableBackend(cv.dnn.DNN_TARGET_CPU)
        print("Using CPU device")
    elif args.device == "gpu":
        net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
        net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA)
        print("Using GPU device")
    
    # Process inputs
    winName = 'Deep learning object detection in OpenCV'
    cv.namedWindow(winName, cv.WINDOW_NORMAL)
    
    if (args.image):
        # Open the image file
        if not os.path.isfile(args.image):
            print("Input image file ", args.image, " doesn't exist")
            sys.exit(1)
        cap = cv.VideoCapture(args.image)
    elif (args.video):
        # Open the video file
        if not os.path.isfile(args.video):
            print("Input video file ", args.video, " doesn't exist")
            sys.exit(1)
        cap = cv.VideoCapture(args.video)
    else:
        # Webcam input
        cap = cv.VideoCapture(0)
    
    ########################################################################
    # we have to count what we have found in last 10 frames
    # and we'll use that as the actual prediction
    CLASS_INFERENCE_THRESHOLD = 15
    symbol_infered = False
    likeliestClass.acquire()
    likeliestClassLockAcquired = True
    
    while cv.waitKey(1) < 0:
        # get frame from the video
        hasFrame, frame = cap.read()
        
        # Stop the program if reached end of video
        if not hasFrame:
            print("Done processing !!!")
            cv.waitKey(3000)
            break
    
        # Create a 4D blob from a frame.
        blob = cv.dnn.blobFromImage(frame, 1/255, (inpWidth, inpHeight), [0,0,0], 1, crop=False)
    
        # Sets the input to the network
        net.setInput(blob)
    
        # Runs the forward pass to get output of the output layers
        outs = net.forward(getOutputsNames(net))
    
        # Remove the bounding boxes with low confidence
        classIndeces = postprocess(frame, classes, outs, confThreshold, nmsThreshold)

        # update confidence counter and likeliestclass

        classCounter.acquire()
        if symbol_infered == False and likeliestClassLockAcquired == False:
            likeliestClass.acquire()
            likeliestClassLockAcquired = True
        symbol_infered = False
        for i in range(len(classes)):
            if i in classIndeces:
                classCounter[i] += 1
                classCounter[i] = max(classCounter[i], CLASS_INFERENCE_THRESHOLD)
                if classCounter[i] == CLASS_INFERENCE_THRESHOLD:
                    symbol_infered = True
                    if likeliestClassLockAcquired == True:
                        likeliestClass.value = i
                        likeliestClass.release()
                        likeliestClassLockAcquired = False
                    else:
                        likeliestClass.acquire()
                        likeliestClass.value = i
                        likeliestClass.release()
                        likeliestClassLockAcquired = False

            else:
                if classCounter[i] > 0:
                    classCounter[i] -= 1

        classCounter.release()
    
    
        # Put efficiency information. The function getPerfProfile returns the overall time for inference(t) and the timings for each of the layers(in layersTimes)
        t, _ = net.getPerfProfile()
        label = 'Inference time: %.2f ms' % (t * 1000.0 / cv.getTickFrequency())
        #cv.putText(frame, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
    
    
        cv.imshow(winName, frame)
