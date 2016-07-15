'''
Simply display the contents of the webcam with optional mirroring using OpenCV 
via the new Pythonic cv2 interface.  Press <esc> to quit.
'''

import cv2
import numpy as np
import math

cam = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2(history=1000)

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
    post1 = cv2.GaussianBlur(fgmask, value, 5)
    return post1, crop_img

def contour_work(thresh1, crop_img, img):
    image, contours, hierarchy = cv2.findContours(thresh1.copy(),
                                                  cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    max_area = -1
    ci = -1
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(cnt)
        if (area > max_area):
            max_area = area
            ci = i
    if ci == -1:
        cnt = 0
    else:
        cnt = contours[ci]
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(crop_img, (x, y), (x + w, y + h), (0, 0, 255), 0)
    hull = cv2.convexHull(cnt)
    drawing = np.zeros(crop_img.shape, np.uint8)
    cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 0)
    cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 0)
    hull = cv2.convexHull(cnt, returnPoints=False)
    defects = cv2.convexityDefects(cnt, hull)
    count_defects = 0
    cv2.drawContours(thresh1, contours, -1, (0, 255, 0), 3)

    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])
        a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
        b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
        c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
        angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 57
        if angle <= 90:
            count_defects += 1
            cv2.circle(crop_img, far, 1, [0, 0, 255], -1)
        # dist = cv2.pointPolygonTest(cnt,far,True)
        cv2.line(crop_img, start, end, [0, 255, 0], 2)
    # cv2.circle(crop_img,far,5,[0,0,255],-1)
    if count_defects == 1:
        cv2.putText(img, "I am Vipul", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
    elif count_defects == 2:
        str = "This is a basic hand gesture recognizer"
        cv2.putText(img, str, (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
    elif count_defects == 3:
        cv2.putText(img, "This is 4 :P", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
    elif count_defects == 4:
        cv2.putText(img, "Hi!!!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
    else:
        cv2.putText(img, "Hello World!!!", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
    # cv2.imshow('drawing', drawing)
    # cv2.imshow('end', crop_img)
    cv2.imshow('Gesture', img)
    all_img = np.hstack((drawing, crop_img))
    cv2.imshow('Contours', all_img)


def main():
    while cam.isOpened():
        img = poll_webcam()
        prep, crop = prepare_box(img, (100, 100), (1100, 700))
        cv2.imshow('Webcam', img)
        cv2.imshow('Post1', prep)
        #cv2.imshow('Post2', crop)
        #contour_work(thresh, crop, img)
        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
