import cv2 
import numpy as np
from collections import Counter
import sys
#Local imports
from ideal_scoreboard import ideal_centred_ellipses
from score_lines import get_score_lines


def normalise_diffs(diffs_rings):
  #There should be max 4 different differences between the radii
  thresh = 4
  made_change = False
  #the difference between the 2nd and 3rd ring tends to be 
  #very similar to the most common difference, which can lead to
  #uncontrolled recursion, hence len(diff_rings) - 3
  for i in range(len(diffs_rings)-3): 
    frst = diffs_rings[i]
    scnd = diffs_rings[i+1]
    diff = abs(frst - scnd)
    
    if 0 < diff and diff <= thresh:
      made_change = True
      average = round((diffs_rings[i]+ diffs_rings[i+1])/2)
      diffs_rings[i] = average
      diffs_rings[i+1] = average
  if made_change:
    return normalise_diffs(diffs_rings)
  return diffs_rings

def calculate_diffs(radii, normalise=True):
  diffs = []
  for i in range(1, len(radii)):
    diffs.append(radii[i-1] - radii[i])
  if normalise:
    diffs = normalise_diffs(diffs)
  return diffs

def reorder(radii):
  #prepare for next fill in 
  radii.sort()
  radii.reverse()
  #calculate diffs
  diffs = calculate_diffs(radii)
  return radii, diffs

def fill_from(missing_rings, radii, most_common_diff, from_ring):
  half_most_common_diff = round(most_common_diff / 2)
  sixth_ring = 0
  seventh_ring = 0
  eighth_ring = 0
  ninth_ring = 0
  tenth_ring = 0
  eleventh_ring = 0
  twelfth_ring = 0
  from_added = from_ring - 6 #added starts from the 6th ring
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
      sixth_ring = radii[-6] 
    seventh_ring = sixth_ring + most_common_diff
    from_ring += 1
  if from_ring == 8:
    #we are missing the 8th ring onwards
    missing_rings[-8] = True
    #generate the 8th ring
    if seventh_ring == 0:
      seventh_ring = radii[-7] 
    eighth_ring = seventh_ring + most_common_diff
    from_ring += 1
  if from_ring == 9:
    #We are missing the 9th ring onwards
    missing_rings[-9] = True
    #generate the 9th ring
    if eighth_ring == 0:
      eighth_ring = radii[-8] 
    ninth_ring = eighth_ring + half_most_common_diff
    from_ring += 1
  if from_ring == 10:
    #we are missing the 10th ring onwards
    missing_rings[-10] = True
    #generate the 10th ring
    if ninth_ring == 0:
      ninth_ring = radii[-9] 
    tenth_ring = ninth_ring + half_most_common_diff
    from_ring += 1
  if from_ring == 11:
    #We are missing the 11th ring onwards
    missing_rings[-11] = True
    #generate the 11th ring
    if tenth_ring == 0:
      tenth_ring = radii[-10] 
    eleventh_ring = tenth_ring + most_common_diff
    from_ring += 1
  if from_ring == 12:
    #We are missing the 12th ring
    missing_rings[-12] = True
    #generate the 12th ring
    if eleventh_ring == 0:
      eleventh_ring = radii[-11] 
    twelfth_ring = eleventh_ring + most_common_diff
  added_rings = [sixth_ring, seventh_ring, eighth_ring, ninth_ring, tenth_ring, eleventh_ring, twelfth_ring]
  radii.extend(added_rings[from_added:])
  radii, diffs = reorder(radii)
  return radii, diffs, missing_rings

  
def fill_in_missing(ideal_radii, original_radii, original_diffs,
                    displayVars=None):
  #TODO: Try with multiple missing rings
  #TODO: Maybe mess around with filling from only 3 or 4 rings
  #TODO: Given the ad hoc mapping, it may be more efficient to simply work out the most common difference
  # and fill the rest of the rings based on that. But that would put all the work i've done on this mess
  # of a function to waste, and it may not fill the rings as nicely in all cases. And given the power of
  # modern processors we are not exactly crying over a tiny bit of inefficiency
  #Fill in the missing rings
  if len(ideal_radii) == len(original_radii):
    return original_radii, original_diffs
  elif len(original_radii) < 4: 
    #This function could work with 3 if the first 3 rings are captured,
    #but better to be on the conservative side. Even 4 rings may not work
    #in all cases
    print("Not enough rings to reliably fill in")
    return None, None
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
  half_most_common_diff = round(most_common_diff / 2)
  #First handle the first two rings
  
  #Get last element of original diffs ,should be smallest
  first_diff = original_diffs[-1]
  smallest = min(original_diffs)
  if first_diff != smallest: 
    #the smallest and second smallest ring should be smaller than the most common difference
    smlst_av_ring = original_radii[-1] #smallest available ring
    # scnd_smlst_av_ring = original_radii[-2] #second smallest available ring
    if smlst_av_ring < most_common_diff:
      #We are either missing the smallest ring or the second smallest ring
      #The smallest ring should be less than half the most common difference (between 3rd and 8th rings)
      #(Additionally if we are missing the second ring then scnd_smlst_ring < most_common_diff == False) 
      if smlst_av_ring < half_most_common_diff:
        #generate the second smallest ring
        missing_rings[-2] = True
        smlst_ring = smlst_av_ring
        scnd_smlst_ring = round((smlst_ring / 22 ) * 42) #rough estimate
        mapped_radii.append(scnd_smlst_ring)
      else:
        #generate the smallest ring
        missing_rings[-1] = True
        scnd_smlst_ring = smlst_av_ring
        smlst_ring = round((scnd_smlst_ring / 42) * 22)
        mapped_radii.append(smlst_ring)
    else:
      #We are missing the first two rings 
      #generate the first two rings
      missing_rings[-1] = True
      missing_rings[-2] = True
      smlst_ring = round((most_common_diff / 72) * 22) #rough estimate
      scnd_smlst_ring = round((smlst_ring / 22 ) * 42)
      mapped_radii.extend([scnd_smlst_ring, smlst_ring]) 
    #Prepare for next fill in
    mapped_radii, mapped_diffs = reorder(mapped_radii)
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
    
  #the ninth ring is the sub ring, and has roughly half the most common difference,
  # between the 8th and 9th ring
  if len(mapped_diffs) < 8:
    #We are missing the 9th ring onwards
    mapped_radii, mapped_diffs, missing_rings = fill_from(missing_rings, mapped_radii, most_common_diff, 9)
  else:
    #get the eighth last element of original diffs.
    eighth_last_diff = mapped_diffs[-8]
    if abs(eighth_last_diff - half_most_common_diff) > threshold:
      #We are missing the 9th ring
      missing_rings[-9] = True
      #generate the 9th ring
      ninth_ring = mapped_radii[-8] + half_most_common_diff
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
    if abs(ninth_last_diff - half_most_common_diff) > threshold:
      #We are missing the 10th ring
      missing_rings[-10] = True
      #generate the 10th ring
      tenth_ring = mapped_radii[-9] + half_most_common_diff
      mapped_radii.append(tenth_ring)
      #prepare for next fill in
      mapped_radii, mapped_diffs = reorder(mapped_radii)
  
  #Add hoc correction of the distances between the subrings
  if mapped_diffs[-9] != mapped_diffs[-8] != half_most_common_diff:
    missing_copy = missing_rings.copy()
    mapped_radii, mapped_diffs, missing_rings = fill_from(missing_rings, mapped_radii[-8:], most_common_diff, 9)
    missing_rings = missing_copy.copy() #because the 9th ring wasnt missing, 
    # we were just correcting it
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
  
  #Ad hoc correction of distances between the 1st 2nd and 3rd rings
  ideal_first_diff = round((most_common_diff / 72) * 22)
  ideal_second_diff = round((most_common_diff / 72) * 70)
  if mapped_diffs[-2] != ideal_second_diff:
    mapped_radii[-2] = mapped_radii[-3] - ideal_second_diff
    mapped_radii[-1] = mapped_radii[-2] - ideal_first_diff
    mapped_diffs[-2] = ideal_second_diff
    mapped_diffs[-1] = ideal_first_diff
  if mapped_diffs[-1] != ideal_first_diff:
    mapped_radii[-1] = mapped_radii[-2] - ideal_first_diff
    mapped_diffs[-1] = ideal_first_diff
  
  if displayVars is not None:
    originalImg, shape, centre_i = displayVars
    if originalImg is None:
      showOriginal = False
    else:
      showOriginal = True
    print("Filling in missing rings")
    print()
    print("Missing rings: ", missing_rings)
    print("Filled in rings: ", mapped_radii)
    print("Filled in diffs: ", mapped_diffs)
    filled_in = np.zeros(shape, np.uint8)
    colour = (255, 0, 0)
    thickness = 1
    for rad in mapped_radii:
      ellipse = (centre_i, (rad, rad), 0)
      cv2.ellipse(filled_in, ellipse, colour, thickness, cv2.LINE_8)
    if showOriginal:
      cv2.imshow("Before filling in rings", originalImg)
    cv2.imshow("After filling in rings", filled_in)
    cv2.waitKey(0)
    # cv2.destroyAllWindows()
  
  
  return mapped_radii, mapped_diffs, missing_rings

def get_map_to_ideal(original_elps, centre_o, ideal_elps, centre_i, 
                      originalImg=None, idealImg=None,show=False,
                      verbose=False, shape=(700, 700)):
  show_ideal = True
  show_original = True
  if idealImg is None:
    show_ideal = False
  if originalImg is None:
    show_original = False
  if verbose:
    print("Mapping")
    print()
  
  ##########################################Ideal##########################################
  #Attributes
  radii_i = []
  diffs_rings_i = [] #capture the differences between the radii
  score_rings_i = 0
  if verbose:
    print("Ideal Rings")
  for ellipse in ideal_elps:
    if verbose:
      print(ellipse)
    ((cx, cy), (major_axis, minor_axis), angle) = ellipse
    radius = round((major_axis + minor_axis)/2)
    radii_i.append(radius)
  score_rings_i = len(radii_i)
  #Calculate the differences between the radii
  diffs_rings_i = calculate_diffs(radii_i, normalise=False)
  #Print the res
  if verbose:
    print("Ideal Centre: ", centre_i)
    print("Ideal Radii: ", radii_i)
    print("Distance between Rings: ", diffs_rings_i)
    print("Score Rings: ", score_rings_i)
    print()

  ##########################################Original##########################################
  #Attributes
  radii_o = []
  diffs_rings_o = []
  score_rings_o = 0
  if verbose:
    print("Original Rings")
  for ellipse in original_elps:
    if verbose:
      print(ellipse)
    ((cx, cy), (major_axis, minor_axis), angle) = ellipse
    radius = round((major_axis + minor_axis)/2)
    radii_o.append(radius)
  score_rings_o = len(radii_o)
  #Calculate the differences between the radii
  diffs_rings_o = calculate_diffs(radii_o, normalise=False)
  if verbose:
    print("Original Centre: ", centre_o)
    print("Original Radii: ", radii_o)
    print("Distance between Rings: ", diffs_rings_o)
    print("Score Rings: ", score_rings_o)
    print()
  
  ##########################################Mapped##########################################
  #Attributes
  mapped_ellipses = []
  diffs_rings_m = [] #capture the differences between the radii
  if show:
    mapped = np.zeros(shape, np.uint8)
    colour = (255, 0, 0)
    thickness = 1
  
  if verbose:
    print("Mapped Rings")
  for radius in radii_o:
    ellipse = (centre_i, (radius, radius), 0)
    if verbose:
      print(ellipse)
    if show:
      cv2.ellipse(mapped, ellipse, colour, thickness, cv2.LINE_8)
    mapped_ellipses.append(ellipse)
  
  #Calculate diffs
  diffs_rings_m = calculate_diffs(radii_o)
  
  #Print the res
  if verbose:
    print("Premapped Centre: ", centre_i)
    print("Premapped Radii: ", radii_o)
    print("Distance between Rings: ", diffs_rings_m)
    print("Score Rings: ", score_rings_o)
    print()
  
  ##########################################Display##########################################
  if show_original:
    cv2.imshow("Original", originalImg)
    cv2.waitKey(0)
  if show_ideal:
    cv2.imshow("Ideal", idealImg)
    cv2.waitKey(0)
  if show:
    cv2.imshow("Premapped", mapped)
    cv2.waitKey(0)
  if show or show_original or show_ideal:
    cv2.destroyAllWindows()
  
  ideal_attributes = (radii_i, diffs_rings_i, centre_i)
  mapped_attributes = (radii_o, diffs_rings_m, centre_i)
  return ideal_attributes, mapped_attributes
  
  


def subtract_rings(radii, missing ,displayVars=None):
  #We want to have the original rings, just mapped to their correct positions
  mapped = []
  for index, bool in enumerate(missing):
    if bool:
      continue
    mapped.append(radii[index])
  if displayVars is not None:
    shape, centre_i = displayVars 
    black = np.zeros(shape, np.uint8)
    colour = (255, 0, 0)
    thickness = 1
    for radius in mapped:
      ellipse = (centre_i, (radius, radius), 0)
      cv2.ellipse(black, ellipse, colour, thickness, cv2.LINE_8)
    cv2.imshow("Mapped final", black)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
  return mapped

def main():
  # original = cv2.imread("black_score.jpg", cv2.IMREAD_GRAYSCALE)
  # ideal = cv2.imread("ideal_map_ellipse.jpg", cv2.IMREAD_GRAYSCALE)
  # if len(sys.argv) == 4:
  #   originalPath, idealPathImg, idealPathTxt = sys.argv[1], sys.argv[2], sys.argv[3]
  # else:
  #   originalPath = input("Enter the original image file: ")
  #   idealPathImg = input("Enter the ideal image file: ")
  #   idealPathTxt = input("Enter the ideal text file: ")
  originalPathImg = "TargetPhotos/20141018_155743.jpg"
  originalImg = cv2.imread(originalPathImg, cv2.IMREAD_UNCHANGED)
  
  score_elps_o, centre_o, scoreImg = get_score_lines(originalImg)
  ideal_elps_i, centre_i, idealImg = ideal_centred_ellipses()
  #Map
  ideal_attributes, mapped_attributes = get_map_to_ideal(
    score_elps_o, centre_o, ideal_elps_i, centre_i, scoreImg, idealImg,
    show=True, verbose=True)
  radii_i, diffs_rings_i, centre_i = ideal_attributes
  radii_m, diffs_rings_m, centre_m = mapped_attributes #these are partially mapped
  #Still not in the exact proportions
  
  #Fill in
  displayVars = (originalImg, idealImg.shape, centre_i)
  map_fill_radii, map_fill_diffs, missing_rings = fill_in_missing(
    radii_i, radii_m, diffs_rings_m, displayVars)
  if map_fill_radii is not None:
    print("Rings filled successfully")
    
  #finish the mapping
  displayVars = (idealImg.shape, centre_i)
  mapped_radii = subtract_rings(map_fill_radii, missing_rings, displayVars)

  
  
  
if __name__ == '__main__':
  main()