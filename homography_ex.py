import cv2
import numpy as np

# Example points from the original image (source points)
pts_src = np.array([
    [100, 150],   # Point 1 in the original image
    [200, 50],    # Point 2 in the original image
    [300, 200],   # Point 3 in the original image
    [400, 100]    # Point 4 in the original image
])

# Corresponding points in the final image (destination points)
pts_dst = np.array([
    [80, 130],    # Corresponding Point 1 in the final image
    [210, 60],    # Corresponding Point 2 in the final image
    [330, 220],   # Corresponding Point 3 in the final image
    [430, 120]    # Corresponding Point 4 in the final image
])

# Find the homography matrix
H, status = cv2.findHomography(pts_src, pts_dst)

print("Homography matrix:")
print(H)


# Example: Transform a point using the homography matrix
point = np.array([[100, 150]], dtype='float32')
point = np.array([point])

# Transform the point
transformed_point = cv2.perspectiveTransform(point, H)
print("Transformed point:", transformed_point)
