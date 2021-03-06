def translation_table(classIndex, client):
    if classIndex == 0 or classIndex == 1:
        return 0
    if classIndex == 2 or classIndex == 3:
        return 1
    if classIndex == 4 or classIndex == 5 or classIndex == 6 or classIndex == 7:
        return 2
    if classIndex == 8 or classIndex == 9 or classIndex == 10 or classIndex == 11:
        return 3
    if classIndex == 12 or classIndex == 13:
        return 4
    if classIndex == 14 or classIndex == 15:
        return 5
    if classIndex == 16 or classIndex == 17:
        return "+"
    if classIndex == 18:
        return "-"
    if classIndex == 22:
        return "="

    if classIndex == 19  :  
        return "O"

    if client != "robot_hand":
#        if classIndex == 19  :  
#            return "ok"
        if classIndex == 20:
            return "thumb_up"
        if classIndex == 21 :  
            return "not_ok"
        if classIndex == 23 :  
            return "fck_u"

    return "fail"

def getClasses():
    classes = {
           0  :  "0_front",
           1  :  "0_back",
           2  :  "1_front",
           3  :  "1_back",
           4  :  "2_thumb_front",
           5  :  "2_thumb_back",
           6  :  "2_front",
           7  :  "2_back",
           8  :  "3_thumb_front",
           9  :  "3_thumb_back",
           10 :  "3_front",
           11 :  "3_back",
           12 :  "4_front",
           13 :  "4_back",
           14 :  "5_front",
           15 :  "5_back",
           16 :  "+_right_up_right_front",
           17 :  "+_right_up_left_front",
           18 :  "minus",
           19 :  "ok_3_fingers",
           20 :  "ok_thubm_up",
           21 :  "not_ok_thumb_down",
           22 :  "equals",
           23 :  "fck_u"
           }
    return classes

