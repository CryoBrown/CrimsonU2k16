'''
Simply display the contents of the webcam with optional mirroring using OpenCV 
via the new Pythonic cv2 interface.  Press <esc> to quit.
'''

import cv2
import numpy as np
import math

cam = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2(history=750)

class CamError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

def poll_webcam():
    ret_val, img = cam.read()
    if ret_val:
        return img
    else:
        raise CamError("Reading from webcam failed.")

def prepare_box(img, pt1, pt2):
    cv2.rectangle(img, pt1, pt2, (0, 255, 0), 0)
    crop_img = img[pt1[1]:pt2[1], pt1[0]:pt2[0]]
    value = (21, 21)
    blur = cv2.GaussianBlur(crop_img, value, 0)
    fgmask = fgbg.apply(crop_img)
    #post1 = cv2.GaussianBlur(fgmask, value, 5)
    return fgmask

def box_gen(fg, minw, minh, maxw, maxh):
    image, contours, hierarchy = cv2.findContours(fg.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    recs = []

    #max_area = -1
    for i in (contours):
        #area = cv2.contourArea(i)
        #print area
        (x, y, w, h) = cv2.boundingRect(i)
        if w > minw and h > minh and w < maxw and h < maxh:
            recs.append((x, y, w, h))
            # if area >1000:
            #     cv2.rectangle(fgmask, (x, y), (x + w, y + h), (0, 0, 0), 2)
            # else:
            #cv2.rectangle(fg, (x, y), (x + w, y + h), (255, 0, 255), 1)
    return recs

def box_draw(boxes, img):
    for x,y,w,h in boxes:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 1)


def main():
    while cam.isOpened():
        img = poll_webcam()
        fg = fgbg.apply(img)
        blur = cv2.GaussianBlur(fg, (5, 5), 0)
        boxes = box_gen(blur, 150, 250, 300, 600)
        box_draw(boxes, img)
        box_draw(boxes, blur)
        cv2.imshow('Webcam', img)
        cv2.imshow('Post', blur)
        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
