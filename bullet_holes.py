import numpy as np
import cv2
import sys

def drawMinEnclose(resized,circles):
	(x,y),radius = cv2.minEnclosingCircle(circles)
	center = (int(x),int(y))
	radius = int(radius)
	cv2.circle(resized,center,radius-1,(0,255,0),2)

def get_bullet_holes(imgFile, size=(500, 500), title="Contours", 
                     show=False, verbose=False):
	resized = cv2.resize(imgFile,size)
	gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
	gray_blur = cv2.GaussianBlur(gray, (9, 9), 0)
	ret, thresh = cv2.threshold(gray_blur, 30, 255, cv2.THRESH_BINARY)
	kernel = np.ones((3, 3), np.uint8)
	eroded = cv2.erode(thresh, kernel, iterations=2)
	cont_img = eroded.copy()
	contours, hierarchy = cv2.findContours(cont_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	
	ellipses = []
	if verbose:
		print("Bullet holes")
	for circles in contours:
		area = cv2.contourArea(circles)
		if area < 80 or area > 550:
			continue
		if len(circles) < 5:
			continue
		ellipse = cv2.fitEllipse(circles)
		if verbose:
			print(ellipse)
		ellipses.append(ellipse)
		# drawMinEnclose(resized,circles)
		cv2.ellipse(resized, ellipse, (0,255,0), 2)
	if verbose:
		print("Num bullet holes: ", len(ellipses))
	if show:
		cv2.imshow('Gray', gray)
		cv2.waitKey(0)
		cv2.imshow('Gray Blur', gray_blur)
		cv2.waitKey(0)
		cv2.imshow('Thresholding', thresh)
		cv2.waitKey(0)
		cv2.imshow('Eroded', eroded)
		cv2.waitKey(0)
		cv2.imshow(title, resized)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
	return ellipses
	
	# # Divide the original image by the illumination pattern
	# illumination_corrected = cv2.divide(gray, blur, scale=255)

	# # Apply global or adaptive thresholding
	# _, corrected_thresh = cv2.threshold(illumination_corrected, 127, 255, cv2.THRESH_BINARY) 


def main():
	# if len(sys.argv) == 2:
	# 	imgPath = sys.argv[1]
	# else:
	# 	imgPath = input("Enter the image file: ")
	# imgFile = cv2.imread(imgPath, cv2.IMREAD_COLOR)
	imgFile = cv2.imread("TargetPhotos/20141018_155743.jpg", 1)	
	bullet_holes = get_bullet_holes(imgFile, show=True, verbose=True)
	

if __name__ == '__main__':
	main()
