import cv2
import numpy as np
from score_lines import sort_ellipses

def ideal(img):
  # Define the center of the ellipse
  center = (247, 254)
  color2 = (0, 255, 0)  # Green
  # Define the thickness of the ellipse outline
  thickness = 1
  radius1 = 10
  cv2.circle(img, center, radius1, color2, thickness, cv2.LINE_8)
  radius2 = 22
  cv2.circle(img, center, radius2, color2, thickness, cv2.LINE_8)
  radius3 = 56
  r = 2
  # cv2.circle(gray, center, radius3, color2, thickness, cv2.LINE_8)
  for i in range(9):
    cv2.circle(img, center, radius3, color2, thickness, cv2.LINE_8)
    r += 1
    radius3 += 36
    if r == 7:
      cv2.circle(img, center, radius3+18, color2, thickness, cv2.LINE_8)

  # Display the image
  cv2.imshow("Ideal", img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

def ideal_centred(img, x, y):
  centre = (x // 2, y // 2)
  color = (255, 0, 0) #Blue
  thickness = 1
  
  radius1 = 10
  cv2.circle(img, centre, radius1, color, thickness, cv2.LINE_8)
  radius2 = 22
  cv2.circle(img, centre, radius2, color, thickness, cv2.LINE_8)
  radius3 = 56
  r = 2
  # cv2.circle(gray, center, radius3, color2, thickness, cv2.LINE_8)
  for i in range(9):
    cv2.circle(img, centre, radius3, color, thickness, cv2.LINE_8)
    r += 1
    radius3 += 36
    if r == 7:
      cv2.circle(img, centre, radius3+18, color, thickness, cv2.LINE_8)
  cv2.imwrite("ideal_map_circle.jpg", img)

def ideal_centred_circles(title="Ideal rings", show=False,
                         verbose=False, x=700, y=700, img=None,
                         write=False, include_inner=True):
  if img is None:
    img = np.zeros((x, y), dtype=np.uint8)
  radii = []
  centre = (round(x/2), round(y/2))
  color = 255 #White
  thickness = 1
  #First ring
  radius1 = 10
  radii.append(radius1)
  cv2.circle(img, centre, radius1, color, thickness, cv2.LINE_8)
  #Second ring
  radius2 = 22
  radii.append(radius2)
  cv2.circle(img, centre, radius2, color, thickness, cv2.LINE_8)
  #Third ring onwards
  radius3 = 56
  r = 2
  for i in range(9):
    cv2.circle(img, centre, radius3, color, thickness, cv2.LINE_8)
    radii.append(radius3)
    r += 1
    radius3 += 36
    if r == 7 and include_inner:
      cv2.circle(img, centre, radius3+18, color, thickness, cv2.LINE_8)
      radii.append(radius3+18)
  radii.sort()
  if verbose:
    print("Ideal rings")
    for radius in radii:
      print(radius)
    print('Centre: ', centre)
    print('Score rings: ', len(radii))
  if write:
    cv2.imwrite("ideal_map_circle.jpg", img)
  if show:
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
  return radii, centre, img

def ideal_ellipses(img):
  center = (247, 254)
  color = (0, 255, 0)  # Green
  thickness = 1
  radius1 = 22
  ellipse = (center, (radius1, radius1), 0)
  cv2.ellipse(img, ellipse, color, thickness, cv2.LINE_8)
  radius2 = 42
  ellipse = (center, (radius2, radius2), 0)
  cv2.ellipse(img, ellipse, color, thickness, cv2.LINE_8)
  radius3 = 112
  r = 2
  for i in range(9):
    ellipse = (center, (radius3, radius3), 0)
    cv2.ellipse(img, ellipse, color, thickness, cv2.LINE_8)
    r += 1
    radius3 += 72
    if r == 7:
      ellipse = (center, (radius3+36, radius3+36), 0)
      cv2.ellipse(img, ellipse, color, thickness, cv2.LINE_8)
  cv2.imshow("Ideal", img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
 
def ideal_centred_ellipses(title="Ideal rings", show=False,
                           verbose=False, x=700, y=700, img=None,
                           write=False):
  if img is None:
    img = np.zeros((x, y), dtype=np.uint8)
  ellipses = []
  centre = (x // 2, y // 2)
  color = 255 #White
  thickness = 1
  #First ring
  radius1 = 22
  ellipse = (centre, (radius1, radius1), 0)
  ellipses.append(ellipse)
  cv2.ellipse(img, ellipse, color, thickness, cv2.LINE_8)
  #Second ring
  radius2 = 42
  ellipse = (centre, (radius2, radius2), 0)
  ellipses.append(ellipse)
  cv2.ellipse(img, ellipse, color, thickness, cv2.LINE_8)
  #Third ring onwards
  radius3 = 112
  r = 2
  if verbose:
    print("Ideal rings")
  for i in range(9):
    ellipse = (centre, (radius3, radius3), 0)
    ellipses.append(ellipse)
    cv2.ellipse(img, ellipse, color, thickness, cv2.LINE_8)
    r += 1
    radius3 += 72
    if r == 7:
      #The 4-3 inner ring
      ellipse = (centre, (radius3+36, radius3+36), 0)
      if verbose:
        print(ellipse)
      ellipses.append(ellipse)
      cv2.ellipse(img, ellipse, color, thickness, cv2.LINE_8)
  ellipses = sort_ellipses(ellipses)
  if verbose:
    for ellipse in ellipses:
      print(ellipse)
    print('Centre: ', centre)
    print('Score rings: ', len(ellipses))
  if write:
    cv2.imwrite("ideal_map_ellipse.jpg", img)
  if show:
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
  return ellipses, centre, img

def missing(img, x, y):
  ellipses = []
  centre = (x // 2, y // 2)
  color = (0, 255, 0) #Blue ish green
  thickness = 1
  #First ring
  radius1 = 22
  ellipse = (centre, (radius1, radius1), 0)
  ellipses.append(ellipse)
  cv2.ellipse(img, ellipse, color, thickness, cv2.LINE_8)
  #Second ring
  radius2 = 42
  ellipse = (centre, (radius2, radius2), 0)
  ellipses.append(ellipse)
  cv2.ellipse(img, ellipse, color, thickness, cv2.LINE_8)
  #Third ring onwards
  radius3 = 112
  r = 2
  for i in range(9):
    if i != 8:#skip twelvth ring
      ellipse = (centre, (radius3, radius3), 0)
      ellipses.append(ellipse)
      cv2.ellipse(img, ellipse, color, thickness, cv2.LINE_8)
    r += 1
    radius3 += 72
    if r == 7:
      #The 4-3 inner ring (technically the 9th ring)
      ellipse = (centre, (radius3+36, radius3+36), 0)
      ellipses.append(ellipse)
      cv2.ellipse(img, ellipse, color, thickness, cv2.LINE_8)
  cv2.imwrite("test_missing/missing_r12.jpg", img)
  ellipses.sort()
  return ellipses
  
def main():
  x, y = 700, 700

  # Create a blank image
  # image = np.zeros((x, y, 3), dtype=np.uint8)

  # background = cv2.imread("ideal.jpg", 1)

  # resized = cv2.resize(background,(500,500))
  # gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

  #ideal(gray)
  #ideal_centred(image, x, y)

  #ideal_ellipses(gray)
  # ellipses = ideal_centred_ellipse(image, x, y)
  # with open("ideal_ellipses.txt", "w") as f:
  #   for ellipse in ellipses:
  #     f.write(str(ellipse) + "\n")
  ellipses, img = ideal_centred_ellipses(show=True, verbose=True)
  for ellipse in ellipses:
    print(ellipse)

