# HUMROgroup5
Repository for group 5's project in the Humanoid robotics course at Chalmers

Here we generate the data needed to train the classifier network.

Right now, we have the following classes

Class name              | Image of class
------------------------|---------------
0_front                 | ![picture alt](./examples/0_front.png "Title is optional")
0_back                  | ![picture alt](./examples/0_back.png "Title is optional")
1_front                 | ![picture alt](./examples/1_front.png "Title is optional")
1_back                  | ![picture alt](./examples/1_back.png "Title is optional")
2_thumb_front           | ![picture alt](./examples/2_thumb_front.png "Title is optional")
2_thumb_back            | ![picture alt](./examples/2_thumb_back.png "Title is optional")
2_front                 | ![picture alt](./examples/2_front.png "Title is optional")
2_back                  | ![picture alt](./examples/2_back.png "Title is optional")
3_thumb_front           | ![picture alt](./examples/3_thumb_front.png "Title is optional")
3_thumb_back            | ![picture alt](./examples/3_thumb_back.png "Title is optional")
3_front                 | ![picture alt](./examples/3_front.png "Title is optional")
3_back                  | ![picture alt](./examples/3_back.png "Title is optional")
4_front                 | ![picture alt](./examples/4_front.png "Title is optional")
4_back                  | ![picture alt](./examples/4_back.png "Title is optional")
5_front                 | ![picture alt](./examples/5_front.png "Title is optional")
5_back                  | ![picture alt](./examples/5_back.png "Title is optional")
+\_right_up_right_front | ![picture alt](./examples/+\_right_up_right_front.png "Title is optional")
+\_right_up_left_front  | ![picture alt](./examples/+\_right_up_left_front.png "Title is optional")
minus                   | ![picture alt](./examples/minus.png "Title is optional")
ok_3_fingers            | ![picture alt](./examples/ok_3_fingers.png "Title is optional")
ok_thubm_up             | ![picture alt](./examples/ok_thubm_up.png "Title is optional")
not_ok_thumb_down       | ![picture alt](./examples/not_ok_thumb_down.png "Title is optional")
equals                  | ![picture alt](./examples/equals.png "Title is optional")
fck_u                   | ![picture alt](./examples/fck_u.png "Title is optional")

##Usage
Make sure to first create the "dataset" directory.

Then start the 
```python 
generateDatasetFromLiveVideo_v2.py 
``` 
script and follow the instruction on the screen.
They will be explained here as well.
First you need to enter your name.
This is done so that we don't accidentally overwrite existing data.
Next, you need to adjust the size and shape of the rectangle
so that it fits your current hand gesture.
This is done with the following key combinations.

keypress      | action
------------- | -------------
h             | move right side to left
j             | move bottom side down
k             | move bottom side up
l             | move right side to right 
y             | finish adjusting

The 

### Configuration variables
#### Capture device 
```python 
camera = cv2.VideoCapture(0) # use computer camera
camera = cv2.VideoCapture("http://192.168.43.1:8080/video") # use camera on LAN
``` 

If you opt for the camera on LAN, install IP Webcam on your Android phone,
or anything which provides equivalent functionality on your phone.
Also, change the URL to match your IP address and comment the unused device.

#### Rectangle speed
```python 
offset = 2
``` 
This variable is the offset by which the rectangle moves in pixels.
It is most certainly too slow on HD, but it is nice on a small 640x480 resolution.
Furthemore, this variables changes the step size when adjusting the rectangle size.
