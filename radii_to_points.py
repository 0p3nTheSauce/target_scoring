import numpy as np
import cv2

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

import numpy as np

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
        cv2.circle(image, (x, y), radius=1, color=point_color, thickness=-1)  # Radius 1 pixel

    return image

def ex():
  # Example usage:
  ideal_center = (350, 350)
  ideal_radii = [688, 616, 544, 508, 472, 400, 328, 256, 184, 112, 42, 22]

  original_center = (259.0, 234.0)
  original_radii = [411, 387, 329, 270, 212, 153, 95, 22]

  # Generate points for both sets of circles
  ideal_points = generate_circle_points(ideal_center, ideal_radii)
  original_points = generate_circle_points(original_center, original_radii)

  # Check the shapes of the generated points
  print("Ideal Points Shape:", ideal_points.shape)
  print("Original Points Shape:", original_points.shape)
  return ideal_points, original_points

def main():
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
  