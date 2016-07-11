'''
Simply display the contents of the webcam with optional mirroring using OpenCV 
via the new Pythonic cv2 interface.  Press <esc> to quit.
'''

import cv2

def show_webcam(mirror=False):
	cam = cv2.VideoCapture(0)
	while True:
		'''
		Get base images
		'''
		ret_val, img = cam.read()
		if mirror: 
			img = cv2.flip(img, 1)
		if cv2.waitKey(1) == 27: 
			break  # esc to quit

		'''
		Processing
		'''
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		blur = cv2.GaussianBlur(gray,(5,5),0)
		ret,thresh1 = cv2.threshold(blur,70,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)


		'''
		Display images to users
		'''
		cv2.imshow('Webcam', img)
		#cv2.imshow('Gray', gray)
		#cv2.imshow('Blur', blur)
		cv2.imshow('Post', thresh1)

	cv2.destroyAllWindows()

def main():
	show_webcam(mirror=False)

if __name__ == '__main__':
	main()