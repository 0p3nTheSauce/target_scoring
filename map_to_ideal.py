import cv2 
import numpy as np
from collections import Counter
import sys

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

def calculate_diffs(radii):
  diffs = []
  for i in range(1, len(radii)):
    diffs.append(radii[i-1] - radii[i])
  filtered = filter(diffs)
  return filtered

def reorder(radii):
  #prepare for next fill in 
  radii.sort()
  radii.reverse()
  #calculate diffs
  diffs = calculate_diffs(radii)
  return radii, diffs

def fill_from(missing_rings, radii, most_common_diff, from_ring):
  sixth_ring = 0
  seventh_ring = 0
  eighth_ring = 0
  ninth_ring = 0
  tenth_ring = 0
  eleventh_ring = 0
  twelfth_ring = 0
  from_copy = from_ring
  if from_ring == 6:
    #We are missing the 6th ring onwards
    missing_rings[-6] = True
    #generate the 6th ring
    sixth_ring = radii[-5] + most_common_diff
    from_ring += 1
  if from_ring == 7:
    #We are missing the 7th ring onwards
    missing_rings[-7] = True
    #generate the 7th ring
    if sixth_ring == 0:
      sixth_ring = radii[-6] + most_common_diff
    seventh_ring = sixth_ring + most_common_diff
    from_ring += 1
  if from_ring == 8:
    #we are missing the 8th ring onwards
    missing_rings[-8] = True
    #generate the 8th ring
    if seventh_ring == 0:
      seventh_ring = radii[-7] + most_common_diff
    eighth_ring = seventh_ring + most_common_diff
    from_ring += 1
  if from_ring == 9:
    #We are missing the 9th ring onwards
    missing_rings[-9] = True
    #generate the 9th ring
    if eighth_ring == 0:
      eighth_ring = radii[-8] + most_common_diff
    ninth_ring = eighth_ring + (most_common_diff / 2)
    from_ring += 1
  if from_ring == 10:
    #we are missing the 10th ring onwards
    missing_rings[-10] = True
    #generate the 10th ring
    if ninth_ring == 0:
      ninth_ring = radii[-9] + (most_common_diff / 2)
    tenth_ring = ninth_ring + (most_common_diff / 2)
    from_ring += 1
  if from_ring == 11:
    #We are missing the 11th ring onwards
    missing_rings[-11] = True
    #generate the 11th ring
    if tenth_ring == 0:
      tenth_ring = radii[-10] + (most_common_diff / 2)
    eleventh_ring = tenth_ring + most_common_diff
    from_ring += 1
  if from_ring == 12:
    #We are missing the 12th ring
    missing_rings[-12] = True
    #generate the 12th ring
    if eleventh_ring == 0:
      eleventh_ring = radii[-11] + most_common_diff
    twelfth_ring = eleventh_ring + most_common_diff
  added_rings = [sixth_ring, seventh_ring, eighth_ring, ninth_ring, tenth_ring, eleventh_ring, twelfth_ring]
  radii.extend(added_rings[from_copy:])
  radii, diffs = reorder(radii)
  return radii, diffs, missing_rings
    
  
def fill_in_missing(ideal_radii, original_radii, original_diffs):
  #TODO: Try with multiple missing rings
  #TODO: Maybe mess around with filling from only 3 or 4 rings
  #Fill in the missing rings
  if len(ideal_radii) == len(original_radii):
    return original_radii, original_diffs
  elif len(original_radii) < 4: 
    #This function could work with 3 if the first 3 rings are captured,
    #but better to be on the conservative side. Even 4 rings may not work
    #in all cases
    print("Not enough rings to reliably fill in")
    return [], []
  mapped_radii = []
  mapped_radii.extend(original_radii)
  mapped_diffs = []
  #Types of differences:
  # - difference between first ring and second ring (unique) (smallest) (one)
  # - difference between second ring and third ring (very similar to most common) (one)
  # - differences between 3rd ring and 8th ring (most common) (five)
  # - differences between 8th ring and 9th ring and 9th ring and 10th ring (half of most common) (two)
  # - differences between the 10th ring and 12th ring (most common) (two)
  missing_rings = [False]*12
  #This should be one of the differences between the 3rd and 8th ring
  most_common_diff = Counter(original_diffs).most_common(1)[0][0]
  
  #First handle the first two rings
  
  #Get last element of original diffs ,should be smallest
  first_diff = original_diffs[-1]
  smallest = min(original_diffs)
  if first_diff != smallest: 
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
        mapped_radii.append(scnd_smlst_ring)
      else:
        #generate the smallest ring
        missing_rings[-1] = True
        scnd_smlst_ring = smlst_av_ring
        smlst_ring = (scnd_smlst_ring / 42) * 22
        mapped_radii.append(smlst_ring)
    else:
      #We are missing the first two rings 
      #generate the first two rings
      missing_rings[-1] = True
      missing_rings[-2] = True
      smlst_ring = (most_common_diff / 58) * 22 #rough estimate
      scnd_smlst_ring = (smlst_ring / 22 ) * 42
      mapped_radii.extend([scnd_smlst_ring, smlst_ring]) 
    #Prepare for next fill in
    mapped_radii, mapped_diffs = reorder(mapped_radii)
    print("Updated radii: ", mapped_radii)
    print("Updated diffs: ", mapped_diffs)
  else:
    mapped_diffs.extend(original_diffs)
  
  #Now we can handle the next 6 rings. They should have the most common difference
  #Starting one ring at a time and fixing efficiency later
  
  #get the second last element of original diffs. should be somewhere in the range of 
  #the most common difference
  threshold = most_common_diff * 0.1
  second_last_diff = mapped_diffs[-2]
  if abs(second_last_diff - most_common_diff) > threshold:
    #We are missing the 3rd ring
    missing_rings[-3] = True
    #generate the 3rd ring
    third_ring = round((mapped_radii[-2] + mapped_radii[-3]) / 2)#rougly the average of the 2nd and 4th ring
    mapped_radii.append(third_ring)
    #prepare for next fill in
    mapped_radii, mapped_diffs = reorder(mapped_radii)
    
  #The next 5 diffs shoud be the most common difference
  
  #get the third last element of original diffs.
  third_last_diff = mapped_diffs[-3]
  if third_last_diff != most_common_diff:
    #We are missing the 4th ring
    missing_rings[-4] = True
    #generate the 4th ring
    fourth_ring = mapped_radii[-3] + most_common_diff
    mapped_radii.append(fourth_ring)
    #prepare for next fill in
    mapped_radii, mapped_diffs = reorder(mapped_radii)
  
  #get the fourth last element of original diffs.
  fourth_last_diff = mapped_diffs[-4]
  if fourth_last_diff != most_common_diff:
    #We are missing the 5th ring
    missing_rings[-5] = True
    #generate the 5th ring
    fifth_ring = mapped_radii[-4] + most_common_diff
    mapped_radii.append(fifth_ring)
    #prepare for next fill in
    mapped_radii, mapped_diffs = reorder(mapped_radii)
  
  if len(mapped_diffs) < 5:
    #We are missing the 6th ring onwards
    mapped_radii, mapped_diffs, missing_rings = fill_from(missing_rings, mapped_radii, most_common_diff, 6)
  else:
    #get the fifth last element of original diffs.
    fifth_last_diff = mapped_diffs[-5]
    if fifth_last_diff != most_common_diff:
      #We are missing the 6th ring
      missing_rings[-6] = True
      #generate the 6th ring
      sixth_ring = mapped_radii[-5] + most_common_diff
      mapped_radii.append(sixth_ring)
      #prepare for next fill in
      mapped_radii, mapped_diffs = reorder(mapped_radii)
  
  if len(mapped_diffs) < 6:
    #we are missing the 7th ring onwards
    mapped_radii, mapped_diffs, missing_rings = fill_from(missing_rings, mapped_radii, most_common_diff, 7)
  else:
    #get the sixth last element of original diffs.
    sixth_last_diff = mapped_diffs[-6]
    if sixth_last_diff != most_common_diff:
      #We are missing the 7th ring
      missing_rings[-7] = True
      #generate the 7th ring
      seventh_ring = mapped_radii[-6] + most_common_diff
      mapped_radii.append(seventh_ring)
      #prepare for next fill in
      mapped_radii, mapped_diffs = reorder(mapped_radii)
  
  if len(mapped_diffs) < 7:
    #we are missing the 8th ring onwards
    mapped_radii, mapped_diffs, missing_rings = fill_from(missing_rings, mapped_radii, most_common_diff, 8)
  else:
    #get the seventh last element of original diffs.
    seventh_last_diff = mapped_diffs[-7]
    if seventh_last_diff != most_common_diff:
      #We are missing the 8th ring
      missing_rings[-8] = True
      #generate the 8th ring
      eighth_ring = mapped_radii[-7] + most_common_diff
      mapped_radii.append(eighth_ring)
      #prepare for next fill in
      mapped_radii, mapped_diffs = reorder(mapped_radii)
    
  #the ninth ring is the sub ring, and has roughly half the most common difference
  if len(mapped_diffs) < 8:
    #We are missing the 9th ring onwards
    mapped_radii, mapped_diffs, missing_rings = fill_from(missing_rings, mapped_radii, most_common_diff, 9)
  else:
    #get the eighth last element of original diffs.
    eighth_last_diff = mapped_diffs[-8]
    if abs(eighth_last_diff - (most_common_diff / 2)) > threshold:
      #We are missing the 9th ring
      missing_rings[-9] = True
      #generate the 9th ring
      ninth_ring = mapped_radii[-8] + (most_common_diff / 2)
      mapped_radii.append(ninth_ring)
      #prepare for next fill in
      mapped_radii, mapped_diffs = reorder(mapped_radii)  
    
  #the tenth ring would also have half the most common difference, between the 9th(sub) and 10th ring
  
  #get the ninth last element of original diffs.
  if len(mapped_diffs) < 9:
    #We are missing the 10th ring onwards
    mapped_radii, mapped_diffs, missing_rings = fill_from(missing_rings, mapped_radii, most_common_diff, 10)
  else:
    ninth_last_diff = mapped_diffs[-9]
    if abs(ninth_last_diff - (most_common_diff / 2)) > threshold:
      #We are missing the 10th ring
      missing_rings[-10] = True
      #generate the 10th ring
      tenth_ring = mapped_radii[-9] + (most_common_diff / 2)
      mapped_radii.append(tenth_ring)
      #prepare for next fill in
      mapped_radii, mapped_diffs = reorder(mapped_radii)
    
  #the 11th and 12 ring would have the most common difference
  
  #get the tenth last element of original diffs.
  if len(mapped_diffs) < 10:
    #We are missing the 11th ring
    mapped_radii, mapped_diffs, missing_rings = fill_from(missing_rings, mapped_radii, most_common_diff, 11)
  else: 
    tenth_last_diff = mapped_diffs[-10]
    if tenth_last_diff != most_common_diff:
      #We are missing the 11th ring
      missing_rings[-11] = True
      #generate the 11th ring
      eleventh_ring = mapped_radii[-10] + most_common_diff
      mapped_radii.append(eleventh_ring)
      #prepare for next fill in
      mapped_radii, mapped_diffs = reorder(mapped_radii)
    
  #get the eleventh last element of original diffs. This might not exist
  if len(mapped_diffs) < 11:
    #We are missing the 12th ring
    mapped_radii, mapped_diffs, missing_rings = fill_from(missing_rings, mapped_radii, most_common_diff, 12)
  
  print("Missing rings: ", missing_rings)
  return mapped_radii, mapped_diffs

def get_map_to_ideal(originalPath, idealPathImg, idealPathTxt, show=False, verbose=False):
  original = cv2.imread(originalPath, cv2.IMREAD_GRAYSCALE)
  ideal = cv2.imread(idealPathImg, cv2.IMREAD_GRAYSCALE)
  resized_o = cv2.resize(original, ideal.shape)
  _, thresh_o = cv2.threshold(resized_o, 120, 255, cv2.THRESH_BINARY)
  _, thresh_i = cv2.threshold(ideal, 120, 255, cv2.THRESH_BINARY)
  contours_o, _ = cv2.findContours(thresh_o, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  
  ##########################################Ideal##########################################
  #Attributes
  radii_i = []
  ideal_centre = () 
  score_rings_i = 0
  diffs_rings_i = [] #capture the differences between the radii
  ellipses_i = []
  centre_i = ()
  
  if show and verbose:
    print("Ideal Rings")
  
  with open(idealPathTxt, 'r') as file:
    lines = file.readlines()
  for line in lines:
    line = line.strip()  
    # Convert the string to a tuple and add it to the list
    ellipse = eval(line)
    ((cx, cy), (major_axis, minor_axis), angle) = ellipse
    radius = int((major_axis + minor_axis)//2)
    radii_i.append(radius)
    ellipses_i.append(ellipse)
  centre_i = (cx, cy)
  score_rings_i = len(ellipses_i)
  #reverse for consistency
  ellipses_i.reverse()
  radii_i.reverse()
  #Calculate the differences between the radii
  for i in range(1, len(radii_i)):
    diffs_rings_i.append(radii_i[i-1] - radii_i[i])
  
  #Print the res
  if show and verbose:
    for ellipse in ellipses_i:
      print(ellipse) 
    print("Ideal Centre: ", centre_i)
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
  
  if show and verbose:
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
    if show and verbose:
      print(ellipse)
    mapped_ellipse = (centre_i, (radius, radius), 0)
    mapped_ellipses.append(mapped_ellipse)
    score_rings_o += 1
    totcx_o += cx
    totcy_o += cy
  original_centre = (totcx_o//score_rings_o, totcy_o//score_rings_o)
  if show and verbose:
    print("Original Centre: ", original_centre)
    print("Score Rings: ", score_rings_o)
    print()
  
  ##########################################Mapping##########################################
  diffs_rings_o = [] #capture the differences between the radii
  #Calculate diffs
  diffs_rings_o = calculate_diffs(radii_o)
  if show and verbose:
    print("Mapped Rings")
  if show:
    for ellipses in mapped_ellipses:
      cv2.ellipse(mapped, ellipses, colour, thickness, cv2.LINE_8)
      if verbose:
        print(ellipses)
  if show and verbose:
    print("Mapped Centre: ", centre_i)
    print("Mapped Radii: ", radii_o)
    print("Filtered Distance between Rings: ", diffs_rings_o)
    print("Score Rings: ", score_rings_o)
  
  ##########################################Fill In##########################################
  if show:
    filled_in = np.zeros(ideal.shape, np.uint8)
  filled_radii, filled_diffs = fill_in_missing(radii_i, radii_o, diffs_rings_o)
  if show:
    for rad in filled_radii:
      ellipse = (centre_i, (rad, rad), 0)
      cv2.ellipse(filled_in, ellipse, colour, thickness, cv2.LINE_8)
    if verbose:
      print("Filled In Rings ", filled_radii)
      print("Filled In diffs ", filled_diffs)
  
  ##########################################Display##########################################
  if show:
    cv2.imshow("Original", thresh_o)
    cv2.imshow("Ideal", thresh_i)
    cv2.imshow("Mapped", mapped)
    cv2.imshow("Filled In", filled_in)
    cv2.waitKey(0)
    cv2.destroyAllWindows()  
  
  return filled_radii, filled_diffs
  
def main():
  # original = cv2.imread("black_score.jpg", cv2.IMREAD_GRAYSCALE)
  # ideal = cv2.imread("ideal_map_ellipse.jpg", cv2.IMREAD_GRAYSCALE)
  # if len(sys.argv) == 4:
  #   originalPath, idealPathImg, idealPathTxt = sys.argv[1], sys.argv[2], sys.argv[3]
  # else:
  #   originalPath = input("Enter the original image file: ")
  #   idealPathImg = input("Enter the ideal image file: ")
  #   idealPathTxt = input("Enter the ideal text file: ")
  originalPath = "black_score.jpg"
  idealPathImg = "ideal_map_ellipse.jpg"
  idealPathTxt = "ideal_ellipses.txt"
  map_fill_radii, map_fill_diffs = get_map_to_ideal(originalPath, idealPathImg, idealPathTxt, show=True, verbose=True)
    


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
diffs_rings_o = calculate_diffs(radii_o)
print("Mapped Rings")
for ellipses in mapped_ellipses:
  cv2.ellipse(mapped, ellipses, colour, thickness, cv2.LINE_8)
  print(ellipses)
print("Mapped Centre: ", ideal_centre)
print("Mapped Radii: ", radii_o)
print("Filtered Distance between Rings: ", diffs_rings_o)
print("Score Rings: ", score_rings_o)


##########################################Fill In##########################################
filled_in = np.zeros(ideal.shape, np.uint8)
filled_radii, filled_diffs = fill_in_missing(radii_i, radii_o, diffs_rings_o)
for rad in filled_radii:
  ellipse = (ideal_centre, (rad, rad), 0)
  cv2.ellipse(filled_in, ellipse, colour, thickness, cv2.LINE_8)

  
print("Filled In Rings ", filled_radii)
print("Filled In diffs ", filled_diffs)


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