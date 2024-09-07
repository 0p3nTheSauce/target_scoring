import cv2
import numpy as np

def get_ellipses(path):
  ellipses = []
  with open(path, "r") as file:
    lines = file.readlines()
  for line in lines:
    line = line.strip()
    ellipse = eval(line)
    ellipses.append(ellipse)
  #ellipses.reverse()
  return ellipses

def get_circles(path):
  radii = []
  totcx = 0
  totcy = 0
  num_rings = 0
  with open(path, "r") as file:
    lines = file.readlines()
  for line in lines:
    line = line.strip()
    ellipse = eval(line)
    ((cx, cy), (major, minor), theta) = ellipse
    totcx += cx
    totcy += cy
    radius = round((major + minor) / 2)
    radii.append(radius)
  num_rings = len(radii)
  centre = (round(totcx / num_rings), round(totcy / num_rings))
  return centre, radii

def get_circle_points(centre, radius, num_points):
  cx, cy = centre
  angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)

  x = cx + radius * np.cos(angles)
  y = cy + radius * np.sin(angles)

  return np.stack((x, y), axis=-1)

def get_ellipse_points(ellipse, num_points):
  ((cx, cy), (major, minor), theta) = ellipse
  major /= 2 # Convert to semi-major axis length
  minor /= 2 # Convert to semi-major axis length
  theta = np.radians(theta)
  t = np.linspace(0, 2 * np.pi, num_points)
  cos_theta = np.cos(theta)
  sin_theta = np.sin(theta)

  x = cx + major * np.cos(t) * cos_theta - minor * np.sin(t) * sin_theta
  y = cy + major * np.cos(t) * sin_theta + minor * np.sin(t) * cos_theta

  return np.vstack((x, y)).T

def ellipses_to_points(ellipse_array, numpoints=100):
  ellipse_points = []
  for ellipse in ellipse_array:
    ellipse_points.append(get_ellipse_points(ellipse, numpoints))
  return np.array(ellipse_points)

def circles_to_points(centre, radii, numpoints=100):
  circle_points = []
  for radius in radii:
    circle_points.append(get_circle_points(centre, radius, numpoints))
  return np.array(circle_points)

def visualise_points(image, points, point_color):
  for (x, y) in points:
    x, y = int(x), int(y)
    cv2.circle(image, (x, y), radius=1, color=point_color, thickness=-1)
  return image
  
def visualise_all(array_points, title="Points", image_size=(700, 700), point_color=255):
  image = np.zeros((image_size[0], image_size[1]), dtype=np.uint8)
  for rings in array_points:
    image = visualise_points(image, rings, point_color)
  cv2.imshow(title, image)
  cv2.waitKey(0)

def main():
  print("Original")
  path = "original_ellipses.txt"
  ellipses = get_ellipses(path)
  for ellipse in ellipses:
    print(ellipse)
  print()
  
  print("Ideal")
  ideal_map = np.zeros((700, 700), dtype=np.uint8)
  path = "ideal_ellipses.txt"
  centre, radii = get_circles(path)
  for radius in radii:
    print(centre, radius)
    cv2.circle(ideal_map, centre, radius, color=255, thickness=1)
  print()
  
  ellipse_points = ellipses_to_points(ellipses)  
  circle_points = circles_to_points(centre, radii)
  visualise_all(ellipse_points, title="Original")
  visualise_all(circle_points, title="Ideal")
  cv2.imshow("Ideal map", ideal_map)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

if __name__ == "__main__":
  main()