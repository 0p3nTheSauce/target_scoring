import cv2 
import numpy as np
from collections import Counter

def filter(diffs_rings):
  thresh = 1
  new_diffs = []
  new_diffs.append(diffs_rings[0])
  for i in range(1, len(diffs_rings)):
    if abs(diffs_rings[i] - diffs_rings[i-1]) <= thresh:
      average = round((diffs_rings[i]+ diffs_rings[i-1])/2)
      new_diffs.append(average)
    else:
      new_diffs.append(diffs_rings[i])
  return new_diffs

def fill_in_missing(ideal_radii, ideal_diffs, original_radii, original_diffs):
  #Fill in the missing rings
  if len(ideal_radii) == len(original_radii):
    return original_radii
  mapped_radii = []
  mapped_diffs = []
  num_diff_r1r2 = 1 #difference between first ring and second ring
  num_diff_r2r3 = 1 #difference between second ring and third ring
  num_diff_r8r9r10 = 2 #difference between 8th ring and 9th ring and 9th ring and 10th ring
  num_diff_r3r8 = 5 #difference between 3rd ring and 8th ring
  num_diff_r10r12 = 2 #difference between 10th ring and 12th ring
  missing_rings = [False]*12
  #This should be one of the differences between the 3rd and 8th ring
  most_common_diff = Counter(original_diffs).most_common(1)[0][0]
  
  #First handle the first two rings
  
  #Get last element of mapped diffs ,should be smallest
  first_diff = original_diffs[-1]
  smallest = min(original_diffs)
  if first_diff == smallest: #First two rings must be correct
    mapped_diffs.append(first_diff)
    mapped_radii.extend([original_radii[-2], original_radii[-1]])
  else:
    #the smallest and second smallest ring should be smaller than the most common difference
    smlst_av_ring = original_radii[-1] #smallest available ring
    scnd_smlst_av_ring = original_radii[-2] #second smallest available ring
    if smlst_av_ring < most_common_diff:
      #We are either missing the smallest ring or the second smallest ring
      #The smallest ring should be less than half the most common difference (between 3rd and 8th rings)
      #(Additionally if we are missing the second ring then scnd_smlst_ring < most_common_diff == False) 
      if smlst_av_ring < (most_common_diff / 2):
        #generate the second smallest ring
        missing_rings[-2] = True
        smlst_ring = smlst_av_ring
        scnd_smlst_ring = (smlst_ring / 22 ) * 42 #rough estimate
      else:
        #generate the smallest ring
        missing_rings[-1] = True
        scnd_smlst_ring = smlst_av_ring
        smlst_ring = (scnd_smlst_ring / 42) * 22
    else:
      #We are missing the first two rings 
      #generate the first two rings
      missing_rings[-1] = True
      missing_rings[-2] = True
      smlst_ring = (most_common_diff / 58) * 22 #rough estimate
      scnd_smlst_ring = (smlst_ring / 22 ) * 42
    mapped_radii.extend([scnd_smlst_ring, smlst_ring]) 
      
  #quick test to see if this is working so far
  print("Missing rings: ", missing_rings)
  mapped_radii.extend(original_radii)
  mapped_radii.sort()
  return mapped_radii

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
diffs_rings_i = [] #capture the differences between the radii
print("Ideal Rings")
with open('ideal_ellipses.txt', 'r') as file:
  lines = file.readlines()
ellipses = []
for line in lines:
  line = line.strip()  
  # Convert the string to a tuple and add it to the list
  ellipse = eval(line)
  ((cx, cy), (major_axis, minor_axis), angle) = ellipse
  radius = int((major_axis + minor_axis)//2)
  radii_i.append(radius)
  ellipses.append(ellipse)
ideal_centre = (cx, cy)
score_rings_i = len(ellipses)
# Print the res
#reverse for consistency
ellipses.reverse()
radii_i.reverse()
#Calculate the differences between the radii
for i in range(1, len(radii_i)):
  diffs_rings_i.append(radii_i[i-1] - radii_i[i])

for ellipse in ellipses:
  print(ellipse) 
print("Ideal Centre: ", ideal_centre)
print("Ideal Radii: ", radii_i)
print("Distance between Rings: ", diffs_rings_i)
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
print("Score Rings: ", score_rings_o)
print()

##########################################Mapping##########################################
diffs_rings_o = [] #capture the differences between the radii
#Calculate diffs
for i in range(1, len(radii_o)):
  diffs_rings_o.append(radii_o[i-1] - radii_o[i])
print("Mapped Rings")
for ellipses in mapped_ellipses:
  cv2.ellipse(mapped, ellipses, colour, thickness, cv2.LINE_8)
  print(ellipses)
print("Mapped Centre: ", ideal_centre)
print("Mapped Radii: ", radii_o)
# print("Distance between Rings: ", diffs_rings)
diffs_rings = filter(diffs_rings_o)
print("Filtered Distance between Rings: ", diffs_rings)
print("Score Rings: ", score_rings_o)



filled_in = np.zeros(ideal.shape, np.uint8)
filled_radii = fill_in_missing(radii_i, diffs_rings_i, radii_o, diffs_rings_o)
for rad in filled_radii:
  ellipse = (ideal_centre, (rad, rad), 0)
  cv2.ellipse(filled_in, ellipse, colour, thickness, cv2.LINE_8)

##########################################Display##########################################
cv2.imshow("Original", thresh_o)
cv2.imshow("Ideal", thresh_i)
cv2.imshow("Mapped", mapped)
cv2.imshow("Filled In", filled_in)


# print()




cv2.waitKey(0)
# cv2.imshow("Mapped", mapped)
# cv2.waitKey(0)
cv2.destroyAllWindows()