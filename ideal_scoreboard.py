import cv2
import numpy as np

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
  color = (0, 255, 0) #Green
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
  cv2.imwrite("ideal_map.jpg", img)
  
x, y = 700, 700

# Create a blank image
image = np.zeros((x, y, 3), dtype=np.uint8)

background = cv2.imread("ideal.jpg", 1)

resized = cv2.resize(background,(500,500))
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

#ideal(gray)
ideal_centred(image, x, y)