import cv2
import subprocess
import re

child = subprocess.Popen(['ls', './dataset'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
files_in_datadir = child.stdout.read().decode('utf-8').split("\n")
regexImages = re.compile(".*png")
regexLabelFile = re.compile(".*txt")

imagesFiles = []
labelFiles = []

for fil in files_in_datadir:
    rezImg = regexImages.search(fil)
    if rezImg != None:
        imagesFiles.append(rezImg.string)
    rezLabel = regexLabelFile.search(fil)
    if rezLabel != None:
        labelFiles.append(rezLabel.string)


i = 0
frameShape = {'height' : 0, 'width': 0}

outputFile = "showing_dataset.mp4"
vid_writer = cv.VideoWriter(outputFile, cv.VideoWriter_fourcc('M','J','P','G'), 30, (round(cap.get(cv.CAP_PROP_FRAME_WIDTH)),round(cap.get(cv.CAP_PROP_FRAME_HEIGHT))))


while True:
    keypress = cv2.waitKey(1) & 0xFF
    

    capture = cv2.VideoCapture("./dataset/" + imagesFiles[i])
    hasFrame, frame = capture.read()
    (frameShape['height'], frameShape['width']) = frame.shape[:2]
    if not hasFrame:
        print("we done")
    labelFile = open("./dataset/" + labelFiles[i], 'r')
    line = labelFile.readline().split(" ")
    float_x_center = float(line[1])
    float_y_center = float(line[2])
    float_width = float(line[3])
    float_height = float(line[4])


    x_center = int(float_x_center * frameShape['width'] )
    y_center = int(float_y_center * frameShape['height'])
    width    = int(float_width    * frameShape['width'])
    height   = int(float_height   * frameShape['height'])

    rectangleCoordinates = {'top': y_center - height // 2, 
            'right': x_center + width // 2, 
            'bottom': y_center + height // 2, 
            'left': x_center - width // 2}

    cv2.rectangle(frame, (rectangleCoordinates['left'], rectangleCoordinates['top']),
                        (rectangleCoordinates['right'], rectangleCoordinates['bottom']),
                        (0,255,0), 2)


    vid_writer.write(frame.astype(np.uint8))

    cv2.imshow("pda", frame)
    i += 1

    if keypress == ord("n"):
        continue
