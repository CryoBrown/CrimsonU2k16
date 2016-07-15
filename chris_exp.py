'''
Simply display the contents of the webcam with optional mirroring using OpenCV 
via the new Pythonic cv2 interface.  Press <esc> to quit.
'''
from __future__ import division

import cv2
import numpy as np
import math

cam = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2(history=400)


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


def process_image(img):
    fg = fgbg.apply(img)
    erosion = cv2.erode(fg, None, iterations=1)
    dilation = cv2.dilate(erosion, None, iterations=1)
    blur = cv2.GaussianBlur(dilation, (5, 5), 0)
    return blur


def box_gen(fg, minw, minh, maxw, maxh):
    image, contours, hierarchy = cv2.findContours(fg.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    recs = []

    # max_area = -1
    for i in (contours):
        # area = cv2.contourArea(i)
        # print area
        (x, y, w, h) = cv2.boundingRect(i)
        if w > minw and h > minh and w < maxw and h < maxh:
            recs.append((x, y, w, h))
            # if area >1000:
            #     cv2.rectangle(fgmask, (x, y), (x + w, y + h), (0, 0, 0), 2)
            # else:
            # cv2.rectangle(fg, (x, y), (x + w, y + h), (255, 0, 255), 1)
    return recs


def draw_box(box, img, color, size):
    x, y, w, h = box
    cv2.rectangle(img, (x, y), (x + w, y + h), color, size)


def draw_boxes(boxes, img):
    for box in boxes:
        draw_box(box, img, (255, 255, 255), 1)


def check_box(box, img):
    x, y, w, h = box
    crop_img = img[y:y + h, x:x + w]
    score = 0.0
    denom = crop_img.size
    num = crop_img.sum()
    return num/denom


def choose_fullest_box(boxes, img):
    ratio = -1.0
    best = None
    for box in boxes:
        cur = check_box(box, img)
        if cur > ratio:
            best = box
            ratio = cur
        print cur
    return best


def main():
    while cam.isOpened():
        #Sources
        img = poll_webcam()
        post = process_image(img)
        boxes = box_gen(post, 100, 100, 700, 700)

        #Selection
        best = choose_fullest_box(boxes, post)

        #Display
        draw_boxes(boxes, post)
        if best != None:
            draw_box(best, img, (0, 255, 0), 2)
            draw_box(best, post, (255, 255, 255), 4)
        cv2.imshow('Webcam', img)
        cv2.imshow('Post', post)

        #Quit condition
        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
