import cv2 
import numpy as np

original = cv2.imread("black_score.jpg", cv2.IMREAD_GRAYSCALE)
ideal = cv2.imread("ideal_map_ellipse.jpg", cv2.IMREAD_GRAYSCALE)
# resized_o = cv2.resize(original, ideal.shape)
resized_o = cv2.resize(original, (500, 500))
# resized_o = cv2.resize(original, ideal.shape)
_, thresh_o = cv2.threshold(resized_o, 120, 255, cv2.THRESH_BINARY)
_, thresh_i = cv2.threshold(ideal, 120, 255, cv2.THRESH_BINARY)

contours_o, _ = cv2.findContours(thresh_o, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# contours_i, _ = cv2.findContours(thresh_i, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

##########################################Ideal##########################################
#Attributes
radii_i = []
ideal_centre = ()
score_rings_i = 0

print("Ideal Rings")
with open('ideal_ellipses.txt', 'r') as file:
  lines = file.readlines()
ellipses = []
for line in lines:
  line = line.strip()  
  # Convert the string to a tuple and add it to the list
  ellipse = eval(line)
  ((cx, cy), (major_axis, minor_axis), angle) = ellipse
  radii_i.append(int((major_axis + minor_axis)//2))
  ellipses.append(ellipse)
ideal_centre = (cx, cy)
score_rings_i = len(ellipses)
# Print the res
#reverse for consistency
ellipses.reverse()
radii_i.reverse()
for ellipse in ellipses:
  print(ellipse) 
print("Ideal Centre: ", ideal_centre)
print("Ideal Radii: ", radii_i)
print("Score Rings: ", score_rings_i)
print()

##########################################Original##########################################
#Attributes
major_prev = 0
totcx_o = 0
totcy_o = 0
score_rings_o = 0
radii_o = []
radius = 0
thresh = 2
#Mapped Image
mapped = np.zeros(ideal.shape, np.uint8)
colour = (255, 0, 0)
thickness = 1
mapped_ellipses = []

print("Original Rings")
for circle in contours_o:
  if len(circle) < 5:
    continue
  ellipse = cv2.fitEllipse(circle)
  ((cx, cy), (major_axis, minor_axis), angle) = ellipse
  if abs(major_axis - major_prev) < thresh:
    continue
  radius= int((major_axis + minor_axis)//2)
  radii_o.append(radius)
  major_prev = major_axis
  print(ellipse)
  mapped_ellipse = (ideal_centre, (radius, radius), 0)
  # cv2.ellipse(mapped, mapped_ellipse, colour, thickness, cv2.LINE_8)
  mapped_ellipses.append(mapped_ellipse)
  score_rings_o += 1
  totcx_o += cx
  totcy_o += cy
original_centre = (totcx_o//score_rings_o, totcy_o//score_rings_o)
print("Original Centre: ", original_centre)
print("Original Radii: ", radii_o)
print("Score Rings: ", score_rings_o)
print()

##########################################Mapping##########################################
print("Mapped Rings")
for ellipses in mapped_ellipses:
  cv2.ellipse(mapped, ellipses, colour, thickness, cv2.LINE_8)
  print(ellipses)
print("Mapped Centre: ", ideal_centre)
print("Mapped Radii: ", radii_o)
print("Score Rings: ", score_rings_o)



##########################################Display##########################################
cv2.imshow("Original", thresh_o)
cv2.imshow("Ideal", thresh_i)
cv2.imshow("Mapped", mapped)


# print()




cv2.waitKey(0)
# cv2.imshow("Mapped", mapped)
# cv2.waitKey(0)
cv2.destroyAllWindows()