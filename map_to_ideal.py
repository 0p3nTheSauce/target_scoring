import cv2 
import numpy as np

original = cv2.imread("black_score.jpg", cv2.IMREAD_GRAYSCALE)
ideal = cv2.imread("ideal_map.jpg", cv2.IMREAD_GRAYSCALE)
# resized_o = cv2.resize(original, ideal.shape)
resized_o = cv2.resize(original, (500, 500))

_, thresh_o = cv2.threshold(resized_o, 120, 255, cv2.THRESH_BINARY)
_, thresh_i = cv2.threshold(ideal, 120, 255, cv2.THRESH_BINARY)

contours_o, _ = cv2.findContours(thresh_o, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours_i, _ = cv2.findContours(thresh_i, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

##########################################Ideal##########################################

totcx_i = 0
totcy_i = 0
thresh = 2
major_prev = 0
score_rings_i = 0
radii_i = []
mapped_ie = np.zeros(ideal.shape, np.uint8)
print("Ideal Rings")
for circle in contours_i:
  if len(circle) < 5:
    continue
  ellipse = cv2.fitEllipse(circle)
  ((cx, cy), (major_axis, minor_axis), angle) = ellipse
  if abs(major_axis - major_prev) < thresh:
    continue
  radii_i.append(int((major_axis + minor_axis)//2))
  major_prev = major_axis
  print(ellipse)
  cv2.ellipse(mapped_ie, ellipse, (255,0,0), 1, cv2.LINE_8)
  score_rings_i += 1
  totcx_i += cx
  totcy_i += cy
ideal_centre = (int(totcx_i//score_rings_i), int(totcy_i//score_rings_i))
print("Ideal Centre: ", ideal_centre)
print("Ideal Radii: ", radii_i)
print("Score Rings: ", score_rings_i)
print()

##########################################Original##########################################

major_prev = 0
totcx_o = 0
totcy_o = 0
score_rings_o = 0
radii_o = []

print("Original Rings")
for circle in contours_o:
  if len(circle) < 5:
    continue
  ellipse = cv2.fitEllipse(circle)
  ((cx, cy), (major_axis, minor_axis), angle) = ellipse
  if abs(major_axis - major_prev) < thresh:
    continue
  radii_o.append(int((major_axis + minor_axis)//2))
  major_prev = major_axis
  print(ellipse)
  score_rings_o += 1
  totcx_o += cx
  totcy_o += cy
original_centre = (totcx_o//score_rings_o, totcy_o//score_rings_o)
print("Original Centre: ", original_centre)
print("Original Radii: ", radii_o)
print("Score Rings: ", score_rings_o)
print()

##########################################Mapping##########################################

mapped = np.zeros(ideal.shape, np.uint8)
mapped_ic = np.zeros(ideal.shape, np.uint8)
colour = (255, 255, 255) #White
thickness = 1
for i in range(score_rings_o):
  cv2.circle(mapped, ideal_centre, radii_o[i], colour, thickness, cv2.LINE_8)
for i in range(score_rings_i):
  cv2.circle(mapped_ic, ideal_centre, radii_i[i], colour, thickness, cv2.LINE_8)
cv2.imshow("Original", thresh_o)
cv2.imshow("Ideal", thresh_i)
cv2.imshow("Mapped", mapped)


# print()




cv2.imshow("Mapped_ic", mapped_ic)
cv2.imshow("Mapped_ie", mapped_ie)
cv2.waitKey(0)
# cv2.imshow("Mapped", mapped)
# cv2.waitKey(0)
cv2.destroyAllWindows()