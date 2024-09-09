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

def fill_ideal():
  #I am aware this is weird
	return [688, 616, 544, 508, 472, 400, 328, 256, 184, 112, 42, 22]

def correspond3(original_radii, most_common_diff):
	ideal_mcd = 72
	missing = [True]*12
	map = [round((rad * ideal_mcd) / most_common_diff) for rad in original_radii]
	print("original: ", map)
	ideal_mapped = fill_ideal()
	print("ideal: ", ideal_mapped)
	pos = 0
	corresponding = []
	missing, corresponding = correspond_rec(map, ideal_mapped, most_common_diff, missing, pos, corresponding)
	unmap = [round((rad * most_common_diff) / ideal_mcd) for rad in corresponding]
	return missing, unmap

def correspond_rec(map, ideal_mapped, most_common_diff, missing, pos, corresponding):
	ideal_mcd = 72
	thresh = round(ideal_mcd * 0.25)
	rad = map.pop(0)
	for i, ideal in enumerate(ideal_mapped):
		if abs(rad - ideal) <= thresh:
			print("Original: ", rad, "corresponds to ideal: ", ideal)
			corresponding.append(rad)
			missing[i+pos] = False
			ideal_mapped.pop(i)
			pos += 1
			break
	if len(map) == 0:
		return missing, corresponding
	return correspond_rec(map, ideal_mapped, most_common_diff, missing, pos, corresponding)

def fill_in_missing2(original_radii, original_diffs):

	if len(original_radii) < 4: 
		#This function could work with 3 if the first 3 rings are captured,
		#but better to be on the conservative side. Even 4 rings may not work
		#in all cases
		print("Not enough rings to reliably fill in")
		return None, None
	most_common_diff = Counter(original_diffs).most_common(1)[0][0]
	original_copy = original_radii.copy()
	missing, unmap = correspond3(original_copy, most_common_diff)
	return missing, unmap
	

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
	# radii_o = normalise_radii(radii_o)
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

def subtract_ellipses(ellipses, corresponding_radii):
	mapped = []
	for ellipse in ellipses:
		((cx, cy), (major_axis, minor_axis), angle) = ellipse
		rad = round((major_axis + minor_axis) / 2)
		if rad in corresponding_radii:
			mapped.append(ellipse)
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
	#originalPathImg = "TargetPhotos/20140811_192351.jpg"
	#originalImg = cv2.imread(originalPathImg, 1)
	originalImg = cv2.imread(originalPathImg, cv2.IMREAD_UNCHANGED)
	
	score_elps_o, centre_o, scoreImg = get_score_lines(originalImg
																										 ,show=True, verbose=True)
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
	# map_fill_radii, map_fill_diffs, missing_rings = fill_in_missing(
	# 	radii_i, radii_m, diffs_rings_m, displayVars)
	map_fill_radii = fill_ideal()
	missing_rings, unmap = fill_in_missing2(radii_m, diffs_rings_m)
	if map_fill_radii is not None:
		print("Rings filled successfully")
		
	#finish the mapping
	displayVars = (idealImg.shape, centre_i)
	mapped_radii = subtract_rings(map_fill_radii, missing_rings, displayVars)

	
	
	
if __name__ == '__main__':
	main()