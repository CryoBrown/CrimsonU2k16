
import cv2
import numpy as np
cam=cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2()
while(cam.isOpened):
   f,img=cam.read()
   if f==True:
       fgmask = fgbg.apply(img)
       print fgmask
       cv2.imshow('track',fgmask)
   if(cv2.waitKey(27)!=-1):
       cam.release()
       cv2.destroyAllWindows()
       #break