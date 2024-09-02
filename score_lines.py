import numpy as np
import cv2
import sys

def drawMinEnclose(resized,circles):
    (x,y),radius = cv2.minEnclosingCircle(circles)
    center = (int(x),int(y))
    radius = int(radius)
    cv2.circle(resized,center,radius-1,(0,255,0),2)

imgFile = cv2.imread("TargetPhotos/20141018_155743.jpg", 1)
# imgFile = cv2.imread("TargetPhotos/20130826_191912.jpg", 1)
resized = cv2.resize(imgFile,(500,500))
cv2.imshow('Resized', resized)
cv2.waitKey(0)

gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
# gray_blur = cv2.GaussianBlur(gray, (3, 3), 1)
gray_blur = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)

cv2.imshow('Gray', gray)
cv2.waitKey(0)
cv2.imshow('Gray Blur', gray_blur)
cv2.waitKey(0)

ret, threshscore = cv2.threshold(gray_blur, 120, 255, cv2.THRESH_BINARY)

cv2.imshow("Thresholding Score", threshscore)
cv2.waitKey(0)


# kernel = np.ones((3, 3), np.uint8)
# dilated = cv2.dilate(threshscore, kernel, iterations=1)
# cv2.imshow("Dilated", dilated)
# cv2.waitKey(0)

cont_score = threshscore.copy()
contours_score, hierarchy_score = cv2.findContours(cont_score, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

black_score = np.zeros(gray.shape) 

scorecopy = resized.copy()
score_rings = 0

thresh = 2
major_prev = 0
for score_circles in contours_score:
  area = cv2.contourArea(score_circles)
  if area < 100:
    continue
  if len(score_circles) < 5:
    continue
  
  #drawMinEnclose(scorecopy,score_circles)
  ellipse = cv2.fitEllipse(score_circles)
  ((cx, cy), (major_axis, minor_axis), angle) = ellipse
  if abs(major_axis - major_prev) < thresh:
    continue
  major_prev = major_axis
  print(ellipse)
  score_rings += 1
  cv2.ellipse(black_score, ellipse, (255,0,0), 1, cv2.LINE_8)
  cv2.ellipse(scorecopy, ellipse, (255,0,0), 1, cv2.LINE_8)
print(score_rings)
cv2.imshow('Contours Score', scorecopy)
cv2.waitKey(0)
cv2.imshow('Black Score', black_score)
cv2.waitKey(0)

# byteMask = np.asarray(black, dtype=np.uint8)
# cv2.imshow('byteMask',byteMask)
# cv2.waitKey(0)

# holes = cv2.bitwise_and(gray, byteMask)
# cv2.imshow('holes',holes)
# cv2.waitKey(0)

cv2.destroyAllWindows()
