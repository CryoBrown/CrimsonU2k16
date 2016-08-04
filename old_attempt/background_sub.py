
import cv2
backsub = cv2.createBackgroundSubtractorMOG2()

import numpy as np
cam=cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2()
while(cam.isOpened):
   ret, frame=cam.read()
   if ret==True:
       fgmask = fgbg.apply(frame)
       image, contours, hierarchy = cv2.findContours(fgmask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

       max_area = -1
       for i in (contours):
           # cnt = contours[i]
           area = cv2.contourArea(i)
           print area
           (x, y, w, h) = cv2.boundingRect(i)
           if w > 20 and h > 20:
               # if area >1000:
               #     cv2.rectangle(fgmask, (x, y), (x + w, y + h), (0, 0, 0), 2)
               # else:
                cv2.rectangle(fgmask, (x, y), (x + w, y + h), (255, 0, 255), 1)



       cv2.imshow('track',fgmask)
   if(cv2.waitKey(27)!=-1):
       cam.release()
       cv2.destroyAllWindows()
       #break












#
# import cv2
# import numpy as np
# cam=cv2.VideoCapture(0)
# fgbg = cv2.createBackgroundSubtractorMOG2()
# while(cam.isOpened):
#    f,img=cam.read()
#    if f==True:
#        fgmask = fgbg.apply(img)
#        print fgmask
#        cv2.imshow('track',fgmask)
#    if(cv2.waitKey(27)!=-1):
#        cam.release()
#        cv2.destroyAllWindows()
#        #break