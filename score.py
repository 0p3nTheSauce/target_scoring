import numpy as np
import cv2
#local imports
from bullet_holes import get_bullet_holes
from score_lines import get_score_lines
from ideal_scoreboard import ideal_centred_ellipses
from map_to_ideal import get_map_to_ideal, fill_in_missing, subtract_rings
from lines_to_points import ellipses_to_points, circles_to_points, get_ellipses, visualise_points, transform

def main():
	#TODO: Make consistent all the way through
	print("Getting bullet holes")
	imgPath = "TargetPhotos/20141018_155743.jpg"
	imgFile = cv2.imread(imgPath, 1)
	bullet_elps_o = get_bullet_holes(imgFile, title="Bullet holes", 
                                  show=True, verbose=True)
	print()

	print("Getting score lines")
	score_elps_o, centre_o, _ = get_score_lines(imgFile, title="Score rings",
                                          show=True, verbose=True)
	print()
	
	print("Getting ideal score lines")
	ideal_elps, centre_i, _ = ideal_centred_ellipses(show=True, verbose=True)
	print()
	#TODO: continue here ...
	
	print("Mapping score lines")
	quit()
	#Premapping 
	ideal_attributes, premapped_attributes = get_map_to_ideal(
		originalPathTxt, idealPathTxt, idealImg=idealImg, verbose=True)
	radii_i, diffs_rings_i, centre_i = ideal_attributes
	radii_m, diffs_rings_m, centre_m = premapped_attributes
	#Fill in
	showOriginal = False
	displayVars = (originalImgRings, idealImg.shape, centre_i, showOriginal)
	map_fill_radii, map_fill_diffs, missing_rings = fill_in_missing(
		radii_i, radii_m, diffs_rings_m, displayVars)
	print()
	#Finish mapping
	mapped_radii = subtract_rings(map_fill_radii, missing_rings)
	black = np.zeros(idealImg.shape, np.uint8)
	colour = (255, 0, 0)
	thickness = 1
	ellipses = []
	for radius in mapped_radii:
		ellipse = (centre_i, (radius, radius), 0)
		ellipses.append(ellipse)
		cv2.ellipse(black, ellipse, colour, thickness, cv2.LINE_8)
	cv2.imshow("Mapped final", black)
	cv2.waitKey(0)
	with open("mapped_ellipses.txt", "w") as f:
		for ellipse in ellipses:
			f.write(str(ellipse) + "\n")
	print("Mapping bullet holes") 
	#Original points
	original_ellipses = get_ellipses(originalPathTxt)
	original_points = ellipses_to_points(original_ellipses)
	#Mapped points
	mapped_points = circles_to_points(centre_i, mapped_radii)
	#Bullet points
	bullet_points = ellipses_to_points(bullet_holes, numpoints=20)
	#Display 
	original_rings = np.zeros(idealImg.shape, np.uint8)
	mapped_rings = original_rings.copy()
	original_bullets = original_rings.copy()
	original_bullets_rings = original_rings.copy()
	mapped_bullets = original_rings.copy()
	mapped_bullets_rings = original_rings.copy()
	
	original_rings = visualise_points(original_rings, original_points)
	mapped_rings = visualise_points(mapped_rings, mapped_points)
	original_bullets = visualise_points(original_bullets, bullet_points)
	original_bullets_rings = visualise_points(original_rings, bullet_points)
	
	cv2.imshow("Original rings", original_rings)
	cv2.imshow("Mapped rings", mapped_rings)
	cv2.imshow("Original bullets", original_bullets)
	cv2.imshow("Original bullets plus rings", original_bullets_rings)
	cv2.waitKey(0)
	#Transform
	mapped_bullet_points = transform(original_points, mapped_points, bullet_points, verbose=True)
	mapped_bullets = visualise_points(mapped_bullets, mapped_bullet_points)
	mapped_bullets_rings = visualise_points(mapped_rings, mapped_bullet_points)
	cv2.imshow("Mapped bullets", mapped_bullets)
	
	center = (350, 350)
	angle = 270
	scale = 1.0
	# Compute the rotation matrix
	rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)

# Apply the rotation
	rotated_image = cv2.warpAffine(mapped_bullets_rings, rotation_matrix, (700, 700))
	#TODO: Neaten up
	#TODO: Apply mapped bullets to fully mapped rings (not excluding any rings)
	#TODO: Start appplying to other images
	#TODO: Calculate scores 
	
	cv2.imshow("Mapped bullets plus rings", rotated_image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	
	
if __name__ == "__main__":
	main()