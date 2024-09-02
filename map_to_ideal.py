import cv2 
import numpy as np

original = cv2.imread("black_score.jpg", cv2.IMREAD_GRAYSCALE)
ideal = cv2.imread("ideal_map.jpg", cv2.IMREAD_GRAYSCALE)
resized_o = cv2.resize(original, ideal.shape)

_, thresh_o = cv2.threshold(resized_o, 120, 255, cv2.THRESH_BINARY)
_, thresh_i = cv2.threshold(ideal, 120, 255, cv2.THRESH_BINARY)

cv2.imshow("Original", thresh_o)
cv2.imshow("Ideal", thresh_i)
cv2.waitKey(0)

contours_o, _ = cv2.findContours(thresh_o, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours_i, _ = cv2.findContours(thresh_i, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

totcx = 0
totcy = 0
thresh = 2
major_prev = 0
score_rings = 0

for circle in contours_i:
  if len(circle) < 5:
    continue
  ellipse = cv2.fitEllipse(circle)
  ((cx, cy), (major_axis, minor_axis), angle) = ellipse
  if abs(major_axis - major_prev) < thresh:
    continue
  
  major_prev = major_axis
  print(ellipse)
  score_rings += 1
  totcx += cx
  totcy += cy

avgcx = totcx / len(contours_o)
avgcy = totcy / len(contours_o)
print(score_rings)