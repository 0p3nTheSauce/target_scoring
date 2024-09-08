import numpy as np
import cv2
#local imports
from bullet_holes import get_bullet_holes
from score_lines import get_score_lines
from ideal_scoreboard import ideal_centred_ellipses, ideal_centred_circles
from map_to_ideal import get_map_to_ideal, fill_in_missing, subtract_rings
from lines_to_points import ellipses_to_points, circles_to_ellipses, visualise_points, transform

def seperate_points(points, num_points=100):
  n = points.shape[0] // num_points
  if points.shape[0] % 100 != 0:
    raise ValueError("The array cannot be evenly split into parts of shape (100, 2).")
  split_points = np.split(points, n)
  return split_points

def score_single(bullet_pnts):
  ideal_radii, centre_i, _ = ideal_centred_ellipses(show=True, verbose=True)

def score(bullet_pnts):
  split_points = seperate_points(bullet_pnts)
  
  

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

	print("Mapping score lines")
	#Premapping
	ideal_attributes, premapped_attributes = get_map_to_ideal(
		score_elps_o, centre_o, ideal_elps, centre_i, show=True, verbose=True)
	radii_i, diffs_rings_i, centre_i = ideal_attributes
	radii_m, diffs_rings_m, centre_m = premapped_attributes
	# print()
	print("Filling in missing rings")
  #Fill in 
	showOriginal = None
	shape = (700, 700)
	displayVars = (showOriginal, shape, centre_i)
	map_fill_radii, map_fill_diffs, missing_rings = fill_in_missing(
		radii_i, radii_m, diffs_rings_m, displayVars)
	if map_fill_radii is None:
		print("No mapping possible")
		return
	#Finish the mapping 
	displayVars = (shape, centre_i)
	mapped_radii = subtract_rings(map_fill_radii, missing_rings, displayVars)
	
	#Convert ellipses to points
	#Original points
	score_elps_o_pnts = ellipses_to_points(score_elps_o)
	#Ideal points
	ideal_elps_pnts = ellipses_to_points(ideal_elps)
	#Mapped points
	score_elps_m = circles_to_ellipses(centre_m, mapped_radii)
	score_elps_m_pnts = ellipses_to_points(score_elps_m)
	#Bullet points
	bullet_elps_o_pnts = ellipses_to_points(bullet_elps_o)
	#Bullet points plus score rings
	blt_scr_o_pnts = np.vstack((bullet_elps_o_pnts, score_elps_o_pnts))
	#Display	
	visualise_points(score_elps_o_pnts,
                  title="Original score rings", show=True)
	visualise_points(score_elps_m_pnts,
                  title="Mapped score rings", show=True)
	visualise_points(bullet_elps_o_pnts,
                  title="Original bullet holes", show=True)
	visualise_points(blt_scr_o_pnts,
                  title="Original score rings plus bullet holes", show=True)
	visualise_points(ideal_elps_pnts,
									title="Ideal score rings", show=True)
	
 #Transform
	bullet_elps_m_pnts = transform(score_elps_o_pnts, score_elps_m_pnts, bullet_elps_o_pnts, verbose=True)
	blt_scr_i_pnts = np.vstack((ideal_elps_pnts, bullet_elps_m_pnts))
	visualise_points(bullet_elps_m_pnts,
                  title="Mapped bullet holes", show=True)
	visualise_points(blt_scr_i_pnts,
                  title="Mapped bullet holes plus ideal score rings",
                  show=True, rotate_angle=270)
 
	# split_points = seperate_points(bullet_elps_m_pnts)
	# for index, points in enumerate(split_points):
	# 	visualise_points(points, title=f"Bullet hole: {index}", show=True)
	score_single(bullet_elps_m_pnts)
	#TODO: Calculate scores
 
	
if __name__ == "__main__":
	main()