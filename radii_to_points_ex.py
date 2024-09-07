import numpy as np
import cv2
import math

def generate_circle_points(center, radii, num_points=20):
	"""
	Generate points on the circumference of circles.
	
	Parameters:
	- center: (x, y) tuple representing the center of the circles.
	- radii: List of radii of the circles.
	- num_points: Number of points to generate on each circle's circumference.
	
	Returns:
	- points: List of generated points on all circles.
	"""
	cx, cy = center
	angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)  # Generate angles in radians

	points = []
	for r in radii:
		# Calculate points on the circumference for each radius
		x = cx + r * np.cos(angles)
		y = cy + r * np.sin(angles)
		circle_points = np.stack((x, y), axis=-1)  # Combine x and y into (x, y) points
		points.extend(circle_points)
	
	return np.array(points, dtype=np.float32)

def generate_circle_points2(centre, radius, num_points=20):
    cx, cy = centre
    angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    x = cx + radius * np.cos(angles)
    y = cy + radius * np.sin(angles)
    return np.stack((x, y), axis=-1)

def generate_ellipse_points(cx, cy, a, b, theta, num_points=100):
    """
    Generate points around the circumference of an ellipse.

    Args:
        cx (float): x-coordinate of the center.
        cy (float): y-coordinate of the center.
        a (float): Length of the semi-major axis.
        b (float): Length of the semi-minor axis.
        theta (float): Angle of rotation in radians.
        num_points (int): Number of points to generate along the circumference.

    Returns:
        numpy.ndarray: Array of (x, y) points along the ellipse.
    """
    t = np.linspace(0, 2 * np.pi, num_points)
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)

    x = cx + a * np.cos(t) * cos_theta - b * np.sin(t) * sin_theta
    y = cy + a * np.cos(t) * sin_theta + b * np.sin(t) * cos_theta

    return np.vstack((x, y)).T

def circpnts():
	r = 5  #radius
	n = 20 #points to generate
	circlePoints = [
	(r * math.cos(theta), r * math.sin(theta))
	for theta in (math.pi*2 * i/n for i in range(n))
	]
	circlePoints = np.array(circlePoints, dtype=np.uint8)
	cv2.imshow("Circle Points", circlePoints)
	cv2.waitKey(0)

def ellpnts():
	r1 = 5
	r2 = 10
	n = 20 #points to generate
	ellipsePoints = [
		(r1 * math.cos(theta), r2 * math.sin(theta))
		for theta in (math.pi*2 * i/n for i in range(n))
	]
	ellipsePoints = np.array(ellipsePoints, dtype=np.uint8)
	cv2.imshow("Ellipse Points", ellipsePoints)
	cv2.waitKey(0)


def visualize_points(points, image_size=(700, 700), point_color=(255, 255, 255)):
	"""
	Visualize points by marking them on a black background.
	
	Parameters:
	- points: Array of (x, y) coordinates of the points to mark.
	- image_size: Tuple defining the size of the output image (width, height).
	- point_color: Color of the points in BGR format. (255, 255, 255) is white.
	
	Returns:
	- image: Image with points marked.
	"""
	# Create a black image
	image = np.zeros((image_size[1], image_size[0], 3), dtype=np.uint8)
	
	# Mark each point
	for (x, y) in points:
		# Convert to integer coordinates for OpenCV
		x, y = int(x), int(y)
		# Draw a small circle or point at each coordinate
		#cv2.circle(image, (x, y), radius=1, color=point_color, thickness=-1)  # Radius 1 pixel
		image[y, x] = point_color
 
	return image




def test3():
	# Given ellipse parameters
	ellipse = ((260.67889404296875, 230.03924560546875), (329.0604248046875, 446.8589172363281), 89.81938171386719)

	# Extract parameters and convert them
	(cx, cy), (a, b), theta = ellipse
	a /= 2  # Convert to semi-major axis length
	b /= 2  # Convert to semi-minor axis length
	theta = np.radians(theta)  # Convert angle to radians

	# Generate points on the ellipse
	ellipse_points = generate_ellipse_points(cx, cy, a, b, theta)

	# Create a blank image
	image_size = (700, 700)
	image = np.zeros(image_size, dtype=np.uint8)

	# Plot the generated points on the image
	for x, y in ellipse_points.astype(int):
		if 0 <= x < image_size[1] and 0 <= y < image_size[0]:
			image[y, x] = 255  # Mark the point as white

	# Draw the ellipse with OpenCV for comparison
	cv2_image = np.zeros(image_size, dtype=np.uint8)
	cv2.ellipse(cv2_image, ellipse, 255, 1)

	# Combine both images for side-by-side comparison
	combined_image = np.hstack((image, cv2_image))

	# Show the images using OpenCV
	cv2.imshow('Generated Points vs OpenCV Ellipse', combined_image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def test4():
    centre = (250, 250)
    radius = 200
    black = np.zeros((500, 500), dtype=np.uint8)
    cv2.circle(black, centre, radius, 255, 1)
    cv2.imshow("Circle", black)
    cv2.waitKey(0)
    cpnts = generate_circle_points2(centre, radius)
    cv2.imshow("Points", visualize_points(cpnts,(500, 500)))
    cv2.waitKey(0)

def main():
  test4()	
  
  quit()	
  ideal_points, original_points = ex()
  ideal_image = visualize_points(ideal_points)
  original_image = visualize_points(original_points)
  # Parameters for the ellipse
  cx, cy = 350, 350  # Center of the ellipse
  a, b = 200, 100    # Semi-major and semi-minor axes lengths
  theta = np.radians(30)  # Rotation angle in degrees, converted to radians

  # Generate points on the ellipse
  ellipse_points = generate_ellipse_points(cx, cy, a, b, theta)
  ellipse_image = visualize_points(ellipse_points)
  cv2.imshow("Ideal Points", ideal_image)
  cv2.imshow("Original Points", original_image)
  cv2.imshow("Ellipse Points", ellipse_image)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

  # Now, you can use these points to find the homography
  #H, _ = cv2.findHomography(original_points, ideal_points, cv2.RANSAC)

if __name__ == "__main__":
  main()
  