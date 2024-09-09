import numpy as np
import cv2
import sys

def drawMinEnclose(resized,circles):
	(x,y),radius = cv2.minEnclosingCircle(circles)
	center = (int(x),int(y))
	radius = int(radius)
	cv2.circle(resized,center,radius-1,(0,255,0),2)

def sort_ellipses(ellipses):
	sorted_ellipses = sorted(
		ellipses, 
		key=lambda e: (max(e[1]), min(e[1])), 
		reverse=True
	)
	return sorted_ellipses

def filter_centre(ellipses, centreImg=(250,250)):
	thresh = 20
	xi, yi = centreImg
	filtered = []
	for ellipse in ellipses:
		((cx, cy), (major_axis, minor_axis), angle) = ellipse
		if abs(cx - xi) <= thresh and abs(cy - yi) <= thresh:
			filtered.append(ellipse)
	return filtered



def filter_number(ellipses, num=12):
  filtered = []
  if len(ellipses) > num:
    for i in range(0, len(ellipses), 2):
      filtered.append(ellipses[i])
    return filtered
  else:
    return ellipses
    

def get_score_lines(imgFile, title='Black Score',
										size=(500, 500), show=False, verbose=False,write=False):
	resized = cv2.resize(imgFile,size)
	cv2.imshow('Resized', resized)
	cv2.waitKey(0)
	gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
	cv2.imshow('Gray', gray)
	cv2.waitKey(0)
	gray_blur = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
	cv2.imshow('Gray Blur', gray_blur)
	cv2.waitKey(0)
	edges=cv2.Canny(gray_blur,100,200)
	cv2.imshow('Edges', edges)
	cv2.waitKey(0)
 
 
	# ret, threshscore = cv2.threshold(edges, 120, 255, cv2.THRESH_BINARY)
	# cont_score = threshscore.copy()
	# contours_score, hierarchy_score = cv2.findContours(cont_score, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cont_score = edges.copy()
	contours_score, hierarchy_score = cv2.findContours(cont_score, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	
	# cv2.imshow('Thresholding Score', threshscore)
	cv2.imshow('Thresholding Score', edges)
	cv2.waitKey(0)
	#image
	black_score = np.zeros(gray.shape) 
	scorecopy = resized.copy()
	colour = (255,0,0)
	thickness = 1
	#Attributes
	thresh = 2
	major_prev = 0
	ellipses = []
	centre_o = ()
	totcx = 0
	totcy = 0
	score_rings = 0
	if verbose:
		print("Original rings")
	for score_circles in contours_score:
		area = cv2.contourArea(score_circles)
		if area < 100:
			continue
		if len(score_circles) < 5:
			continue
		ellipse = cv2.fitEllipse(score_circles)
		((cx, cy), (major_axis, minor_axis), angle) = ellipse
		if abs(major_axis - major_prev) < thresh:
			continue
		if abs(minor_axis - major_axis) < thresh:
			continue
		totcx += cx
		totcy += cy
		ellipses.append(ellipse)
		major_prev = major_axis
		#image
	ellipses = filter_centre(ellipses)
	ellipses = filter_number(ellipses)
	for ellipse in ellipses:
		cv2.ellipse(black_score, ellipse, colour, thickness, cv2.LINE_8)
		cv2.ellipse(scorecopy, ellipse, colour, thickness, cv2.LINE_8)
			
	score_rings = len(ellipses)
	centre_o = (totcx//score_rings, totcy//score_rings)
	ellipses = sort_ellipses(ellipses)
	if verbose:
		for ellipse in ellipses:
			print(ellipse)
		print("Centre: ", centre_o)
		print("Score Rings: ", score_rings)
	if show:
		cv2.imshow('Contours Score', scorecopy)
		cv2.waitKey(0)
		cv2.imshow(title, black_score)
		cv2.waitKey(0)
		
		
		cv2.destroyAllWindows()
	if write:
		cv2.imwrite('black_score.jpg', black_score)
		for ellipse in ellipses:
			with open("original_ellipses.txt", "a") as f:
				f.write(str(ellipse) + "\n")
	return ellipses, centre_o, black_score

# def get_score_lines(imgFile, title='Black Score',
#                     size=(500, 500), show=False, verbose=False,write=False):
# 	resized = cv2.resize(imgFile,size)
# 	gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
# 	gray_blur = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
# 	ret, threshscore = cv2.threshold(gray_blur, 200, 255, cv2.THRESH_BINARY)
# 	cont_score = threshscore.copy()
# 	contours_score, hierarchy_score = cv2.findContours(cont_score, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	
#   #image
# 	black_score = np.zeros(gray.shape) 
# 	scorecopy = resized.copy()
# 	colour = (255,0,0)
# 	thickness = 1
#   #Attributes
# 	thresh = 2
# 	major_prev = 0
# 	ellipses = []
# 	centre_o = ()
# 	totcx = 0
# 	totcy = 0
# 	score_rings = 0
# 	if verbose:
# 		print("Original rings")
# 	for score_circles in contours_score:
# 		area = cv2.contourArea(score_circles)
# 		if area < 100:
# 			continue
# 		if len(score_circles) < 5:
# 			continue
# 		ellipse = cv2.fitEllipse(score_circles)
# 		((cx, cy), (major_axis, minor_axis), angle) = ellipse
# 		if abs(major_axis - major_prev) < thresh:
# 			continue
# 		totcx += cx
# 		totcy += cy
# 		ellipses.append(ellipse)
# 		major_prev = major_axis
# 		#image
# 		cv2.ellipse(black_score, ellipse, colour, thickness, cv2.LINE_8)
# 		cv2.ellipse(scorecopy, ellipse, colour, thickness, cv2.LINE_8)
			
# 	score_rings = len(ellipses)
# 	centre_o = (totcx//score_rings, totcy//score_rings)
# 	ellipses = sort_ellipses(ellipses)
# 	if verbose:
# 		for ellipse in ellipses:
# 			print(ellipse)
# 		print("Centre: ", centre_o)
# 		print("Score Rings: ", score_rings)
# 	if show:
# 		cv2.imshow('Resized', resized)
# 		cv2.waitKey(0)
# 		cv2.imshow('Gray', gray)
# 		cv2.waitKey(0)
# 		cv2.imshow('Gray Blur', gray_blur)
# 		cv2.waitKey(0)
# 		cv2.imshow('Thresholding Score', threshscore)
# 		cv2.waitKey(0)
# 		cv2.imshow(title, black_score)
# 		cv2.waitKey(0)
# 		cv2.imshow('Contours Score', scorecopy)
# 		cv2.waitKey(0)
		
# 		cv2.destroyAllWindows()
# 	if write:
# 		cv2.imwrite('black_score.jpg', black_score)
# 		for ellipse in ellipses:
# 			with open("original_ellipses.txt", "a") as f:
# 				f.write(str(ellipse) + "\n")
# 	return ellipses, centre_o, black_score

def main():
	# if len(sys.argv) == 2:
	#   imgPath = sys.argv[1]
	# else:
	#   imgPath = input("Enter the image file: ")
	#imgFile = cv2.imread("TargetPhotos/20141018_155743.jpg", 1)
	# imgFile = cv2.imread("TargetPhotos/20141022_194340.jpg", 1)
	imgFile = cv2.imread("TargetPhotos/20140811_192351.jpg", 1)
	score_lines, centre_o, black_score = get_score_lines(imgFile,
																											show=True, verbose=True,
																											write=False)
	

if __name__ == '__main__':
	main()