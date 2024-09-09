import numpy as np
import math
import cv2
#local imports
from bullet_holes import get_bullet_holes
from score_lines import get_score_lines
from ideal_scoreboard import ideal_centred_ellipses, ideal_centred_circles
from map_to_ideal import get_map_to_ideal, fill_in_missing2, subtract_rings, subtract_ellipses
from lines_to_points import ellipses_to_points, circles_to_ellipses, visualise_points, transform, ellipses_to_points_bullets

def seperate_points(points, num_points):
	n = points.shape[0] // num_points
	if points.shape[0] % num_points != 0:
		raise ValueError(f"The array cannot be evenly split into parts of shape ({num_points}, 2).")
	split_points = np.split(points, n)
	return split_points

def inside_ring(points, centre, radius):
	cx, cy = centre
	threshold = 15
	# Calculate the distance of each point from the center (cx, cy)
	distances = np.sqrt((points[:, 0] - cx) ** 2 + (points[:, 1] - cy) ** 2)
	# Check how many points are inside the circle
	points_inside_circle = np.sum(distances <= radius)
	print("Points inside circle:", points_inside_circle)
	#Check if at least threshold points are inside the circle
	return points_inside_circle >= threshold

# def inside_ring(points, centre, radius):
# 	cx, cy = centre
# 	threshold = 20
# 	inside = []
# 	points_inside_circle = 0
# 	# Calculate the distance of each point from the center (cx, cy)
# 	for point in points:
# 		x, y = point
# 		distance = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
# 		if distance <= radius:
# 			points_inside_circle += 1
# 			inside.append(point)
# 	print("Points inside circle:", points_inside_circle)
# 	return inside, points_inside_circle >= threshold

def score_single(bullet_pnts, ideal_radii, centre_i):
	score = 11
	for radii in ideal_radii:
		if inside_ring(bullet_pnts, centre_i, radii):
			return score
		score -= 1
	return 0

# def score_single(bullet_pnts, ideal_radii, centre_i):
# 	score = 11
# 	for radii in ideal_radii:
# 		inside, points_inside_circle = inside_ring(bullet_pnts, centre_i, radii)
# 		if points_inside_circle:
# 			return score, inside
# 		score -= 1
# 	return 0

def score(bullet_pnts, num_points=200):
	scores = []
	total = 0
	split_points = seperate_points(bullet_pnts, num_points)
	print(len(split_points))
	ideal_radii, centre_i, _ = ideal_centred_circles(include_inner=False)
	for blt_pnts in split_points:
		score = score_single(blt_pnts, ideal_radii, centre_i)
		scores.append(score)
		total += score
	print("Scores:", scores)
	print("Total:", total)
	
# def score(bullet_pnts, num_points=100):
# 	scores = []
# 	points_inside = np.empty((0, 2))
# 	total = 0
# 	split_points = seperate_points(bullet_pnts, num_points)
# 	print(len(split_points))
# 	ideal_radii, centre_i, _ = ideal_centred_circles(include_inner=False)
# 	for blt_pnts in split_points:
# 		score, inside = score_single(blt_pnts, ideal_radii, centre_i)
# 		scores.append(score)
# 		points_inside = np.vstack((points_inside, np.array((inside))))
# 		total += score
# 	print("Scores:", scores)
# 	print("Total:", total)
# 	return points_inside
 

def main():
	#TODO: Make consistent all the way through
	print("Getting bullet holes")
	#imgPath = "TargetPhotos/20141018_155743.jpg"
	imgPath = "TargetPhotos/20140811_192351.jpg"
	
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
	shape = (700, 700)
	missing_rings, corr_radii_o = fill_in_missing2(radii_m, diffs_rings_m)
	print("Missing rings", missing_rings)
	print("Corresponding score rings", corr_radii_o)
	if missing_rings is None:
		print("No mapping possible")
		return
	#Finish the mapping 
	displayVars = (shape, centre_i)
	mapped_radii = subtract_rings(radii_i, missing_rings, displayVars)
	score_elps_o = subtract_ellipses(score_elps_o, corr_radii_o)
	#Convert ellipses to points
	#Original points
	score_elps_o_pnts = ellipses_to_points(score_elps_o)
	#Ideal points
	ideal_elps_pnts = ellipses_to_points(ideal_elps)
	#Mapped points
	score_elps_m = circles_to_ellipses(centre_m, mapped_radii)
	score_elps_m_pnts = ellipses_to_points(score_elps_m)
	#Bullet points
	bullet_elps_o_pnts = ellipses_to_points_bullets(bullet_elps_o)
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
 
	#split_points = seperate_points(bullet_elps_m_pnts)
	# for index, points in enumerate(split_points):
	# 	visualise_points(points, title=f"Bullet hole: {index}", show=True)
	ideal_radii, centre_i, idealImg = ideal_centred_ellipses(show=True)
	visualise_points(bullet_elps_m_pnts,
									title="Mapped bullet holes plus ideal score rings",
									show=True, image=idealImg, rotate_angle=270)	
	
 
	# points_inside = score(bullet_elps_m_pnts)
	# visualise_points(points_inside, title="Points inside", show=True, image=idealImg)
	score(bullet_elps_m_pnts)
 #TODO: Calculate scores
 
	
if __name__ == "__main__":
	main()