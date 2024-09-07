import numpy as np
import cv2
#local imports
from bullet_holes import get_bullet_holes
from score_lines import get_score_lines
from map_to_ideal import get_map_to_ideal, fill_in_missing, subtract_rings
from lines_to_points import ellipses_to_points, circles_to_points, get_ellipses, visualise_all

def transform(source_points, destination_points, bullet_holes, verbose=False):
  H, status = cv2.findHomography(source_points, destination_points)
  transformed_points = cv2.perspectiveTransform(bullet_holes, H)
  if verbose:
    print("Homography matrix:")
    print(H)
    print()
    print("Transformed points:", transformed_points)
  return transformed_points
  
def main():
  #TODO: Make consistent all the way through
  print("Getting bullet holes")
  imgPath = "TargetPhotos/20141018_155743.jpg"
  imgFile = cv2.imread(imgPath, 1)
  bullet_holes = get_bullet_holes(imgFile, show=True, verbose=True)
  print()
  
  print("Getting score lines")
  score_lines, centre_o = get_score_lines(imgFile, show=True, verbose=True, write=True)
  print()
  
  print("Mapping score lines")
  originalPathTxt = "original_ellipses.txt"
  idealPathTxt = "ideal_ellipses.txt"
  idealPathImg = "ideal_map_ellipse.jpg"
  originalPathImg = "black_score.jpg"
  idealImg = cv2.imread(idealPathImg, cv2.IMREAD_GRAYSCALE)
  originalImgRings = cv2.imread(originalPathImg, cv2.IMREAD_GRAYSCALE)
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
  for radius in mapped_radii:
    ellipse = (centre_i, (radius, radius), 0)
    cv2.ellipse(black, ellipse, colour, thickness, cv2.LINE_8)
  cv2.imshow("Mapped final", black)
  cv2.waitKey(0)
  
  print("Mapping bullet holes") 
  #Original points
  original_ellipses = get_ellipses(originalPathTxt)
  original_points = ellipses_to_points(original_ellipses)
  #Mapped points
  mapped_points = circles_to_points(centre_i, mapped_radii)
  #Bullet points
  bullet_points = ellipses_to_points(bullet_holes, numpoints=20)
  #Bullet holes plus score rings
  bullets_plus_rings = bullet_points + original_points
  #Display
  visualise_all(original_points, title="Original")
  visualise_all(mapped_points, title="Mapped") #TODO: mapped too big
  visualise_all(bullet_points, title="Bullet holes")
  visualise_all(bullets_plus_rings, title="Bullet holes plus rings")
  #Transform
  mapped_bullet_holes = transform(original_points, mapped_points, bullet_points, verbose=True)
  #Display
  visualise_all(mapped_bullet_holes, title="Mapped bullet holes")
  mapped_bullets_plus_rings = mapped_bullet_holes + mapped_points
  visualise_all(mapped_bullets_plus_rings, title="Mapped bullet holes plus rings")

if __name__ == "__main__":
  main()