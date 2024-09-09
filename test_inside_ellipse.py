import numpy as np
import cv2
def point_in_ellipse(point, ellipse):
    (x, y) = point
    ((cx, cy), (major, minor), theta) = ellipse
    a = major / 2  # Semi-major axis
    b = minor / 2  # Semi-minor axis
    theta = np.radians(theta)

    # Translate point to ellipse center
    translated_x = x - cx
    translated_y = y - cy

    # Rotate point by negative ellipse angle
    cos_theta = np.cos(-theta)
    sin_theta = np.sin(-theta)

    x_rot = translated_x * cos_theta - translated_y * sin_theta
    y_rot = translated_x * sin_theta + translated_y * cos_theta

    # Check if point satisfies the ellipse equation
    inside = (x_rot**2 / a**2) + (y_rot**2 / b**2) <= 1

    return inside

cx = 350
cy = 350
ellipse = ((cx, cy), (15, 10), 0)  # Center at (5,5), major axis 8, minor axis 4, rotation 30 degrees
point = (6, 6)  # Point to check

if point_in_ellipse(point, ellipse):
    print("Point is inside the ellipse.")
else:
    print("Point is outside the ellipse.")
    
black = np.zeros((700, 700), dtype=np.uint8)
cv2.ellipse(black, ellipse, color=255, thickness=1)
tl = (int(cx-7.5), int(cx+7.5))
br = (int(cy+7.5),int( cy-7.5))
cv2.rectangle(black, tl, br, color=255, thickness=1)
cv2.imshow("Ellipse", black)
cv2.waitKey(0)
cv2.destroyAllWindows()