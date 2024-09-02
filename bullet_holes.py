import numpy as np
import cv2
import sys

def drawMinEnclose(resized,circles):
    (x,y),radius = cv2.minEnclosingCircle(circles)
    center = (int(x),int(y))
    radius = int(radius)
    cv2.circle(resized,center,radius-1,(0,255,0),2)

imgFile = cv2.imread("TargetPhotos/20141018_155743.jpg", 1)

resized = cv2.resize(imgFile,(500,500))
cv2.imshow('Resized', resized)
cv2.waitKey(0)

gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

gray_blur = cv2.GaussianBlur(gray, (9, 9), 0)
# gray_blur = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)

cv2.imshow('Gray', gray)
cv2.waitKey(0)
cv2.imshow('Gray Blur', gray_blur)
cv2.waitKey(0)

ret,thresh = cv2.threshold(gray_blur,30,255,cv2.THRESH_BINARY)
# cv2.imshow("OTSU Thresholding", thresh)
cv2.imshow("Thresholding", thresh)
cv2.waitKey(0)

kernel = np.ones((3, 3), np.uint8)
eroded = cv2.erode(thresh, kernel, iterations=2)
cv2.imshow("Eroded", eroded)
cv2.waitKey(0)

cont_img = eroded.copy()
contours, hierarchy = cv2.findContours(cont_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# create a blank image for the bytemask... WHY named BYTE mask?
black = np.zeros(gray.shape)

for circles in contours:
	area = cv2.contourArea(circles)
	if area < 80 or area > 350:
			continue

	if len(circles) < 5:
			continue

	ellipse = cv2.fitEllipse(circles)
	drawMinEnclose(resized,circles)
	cv2.ellipse(black, ellipse, (255,255,255), -1, 2)
cv2.imshow('Contours', resized)
cv2.waitKey(0)

# byteMask = np.asarray(black, dtype=np.uint8)
# cv2.imshow('byteMask',byteMask)
# cv2.waitKey(0)

# holes = cv2.bitwise_and(gray, byteMask)
# cv2.imshow('holes',holes)
# cv2.waitKey(0)

cv2.destroyAllWindows()
