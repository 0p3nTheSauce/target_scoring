import cv2
import numpy as np

def transform(source_points, destination_points, bullet_holes,
              verbose=False):
  
  if verbose:
    print("Source Points Shape:", source_points.shape)
    print("Destination Points Shape:", destination_points.shape)
    print("Bullet Holes Shape:", bullet_holes.shape)
    print()
  #reshape for find homography
  source_points = np.array(source_points, dtype='float32').reshape(-1, 1, 2)
  destination_points = np.array(destination_points, dtype='float32').reshape(-1, 1, 2)
  bullet_holes = np.array(bullet_holes, dtype='float32').reshape(-1, 1, 2)
  
  if verbose:
    print("Source Points Shape:", source_points.shape)
    print("Destination Points Shape:", destination_points.shape)
    print("Bullet Holes Shape:", bullet_holes.shape)
  
  H, status = cv2.findHomography(source_points, destination_points)
  transformed_points = cv2.perspectiveTransform(bullet_holes, H)
  
  if verbose:
    print("Homography matrix:")
    print(H)
    print()
  
  
  #Return to original shape
  transformed_points = transformed_points.reshape(-1, 2)

  return transformed_points

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

  return np.vstack((x, y)).T

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
  ellipse_points = np.empty((0, 2), dtype=np.float64)
  for ellipse in ellipse_array:
    points = get_ellipse_points(ellipse, numpoints)
    ellipse_points = np.vstack((ellipse_points, points))
  return ellipse_points

def circles_to_points(centre, radii, numpoints=100):
    # Start with an empty NumPy array
    circle_points = np.empty((0, 2), dtype=np.float64)

    # Loop through each radius and add the points to the array
    for radius in radii:
        points = get_circle_points(centre, radius, numpoints)
        circle_points = np.vstack((circle_points, points))

    return circle_points

def circles_to_ellipses(centre, radii):
  ellipses = []
  for radius in radii:
    ellipse = (centre, (radius, radius), 0)
    ellipses.append(ellipse)
  return ellipses

def visualise_points(points, title="Points", show=False, shape=(700,700),
                     image=None, point_color=255, rotate_angle=0):
  if image is None:
    image = np.zeros(shape, dtype=np.uint8)
  for (x, y) in points:
    x, y = int(x), int(y)
    cv2.circle(image, (x, y), radius=1, color=point_color, thickness=-1)
  if rotate_angle != 0:
    center = (shape[0] // 2, shape[1] // 2)
    scale = 1.0
    rotation_matrix = cv2.getRotationMatrix2D(center, rotate_angle, scale)
    image = cv2.warpAffine(image, rotation_matrix, shape)
  if show:
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
  return image

def main():
  print("Original")
  path = "experimentation/ellipses/original_ellipses.txt"
  ellipses = get_ellipses(path)
  for ellipse in ellipses:
    print(ellipse)
  print()
  
  print("Ideal")
  ideal_map = np.zeros((700, 700), dtype=np.uint8)
  # path = "ideal_ellipses.txt"
  path = "experimentation/ellipses/mapped_ellipses.txt"
  centre, radii = get_circles(path)
  for radius in radii:
    print(centre, radius)
    cv2.circle(ideal_map, centre, radius, color=255, thickness=1)
  print()
  
  a_bullet = ((268.5964050292969, 257.7123107910156), (12.312881469726562, 17.09013557434082), 103.4205093383789)
  a_bullet2 = ((280.8199768066406, 224.81353759765625), (16.182527542114258, 20.5277042388916), 20.32695770263672)
  a_bullet3 = ((252.96786499023438, 222.6781463623047), (14.28591537475586, 20.636219024658203), 8.740201950073242)
  a_bullet_points1 = get_ellipse_points(a_bullet, 100)
  a_bullet_points2 = get_ellipse_points(a_bullet2, 100)
  a_bullet_points3 = get_ellipse_points(a_bullet3, 100)
  a_bullet_points = np.vstack((a_bullet_points1, a_bullet_points2, a_bullet_points3))
  
  
  ellipse_points = ellipses_to_points(ellipses)  
  circle_points = circles_to_points(centre, radii)
  original_image = np.zeros((700, 700), dtype=np.uint8)
  ideal_image = original_image.copy()
  bullet_image = original_image.copy()
  original_bullet = original_image.copy()
  mapped_bullet_image = original_image.copy()
  ideal_bullet = original_image.copy()
  
  print()
  mapped_bullet_points = transform(ellipse_points, circle_points, a_bullet_points)
  
  original_image = visualise_points(original_image, ellipse_points)
  ideal_image = visualise_points(ideal_image, circle_points)
  bullet_image = visualise_points(bullet_image, a_bullet_points)
  mapped_bullet_image = visualise_points(mapped_bullet_image, mapped_bullet_points)
  
  original_bullet = visualise_points(original_image, a_bullet_points)
  ideal_bullet = visualise_points(ideal_image, mapped_bullet_points)
  
  cv2.imshow("Original points", original_image)
  cv2.imshow("Ideal points", ideal_image)
  cv2.imshow("Bullet points", bullet_image)
  cv2.imshow("Mapped bullet points", mapped_bullet_image)
  
  cv2.imshow("Original bullet", original_bullet)
  
  center = (350, 350)
  angle = 270
  scale = 1.0
  # Compute the rotation matrix
  rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)

# Apply the rotation
  rotated_image = cv2.warpAffine(ideal_bullet, rotation_matrix, (700, 700))
  
  cv2.imshow("Ideal bullet", rotated_image)
  
  
  cv2.imshow("Ideal map", ideal_map)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

if __name__ == "__main__":
  main()