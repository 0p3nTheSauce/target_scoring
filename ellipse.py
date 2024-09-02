import cv2
import numpy as np

# Create a blank image
image = np.zeros((400, 400, 3), dtype=np.uint8)

# Define the center of the ellipse
center = (200, 200)

# Define the axes lengths (major and minor axes)
axes = (75, 50)

# Define the angle of rotation
angle = 90

# Define the start and end angle of the ellipse arc
startAngle = 0
endAngle = 360

# Define the color (BGR format)
color = (0, 255, 0)  # Green

# Define the thickness of the ellipse outline
thickness = 2

# Draw the ellipse
cv2.ellipse(image, center, axes, angle, startAngle, endAngle, color, thickness)

# Display the image
cv2.imshow("Ellipse", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
