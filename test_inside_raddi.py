import numpy as np

# Example numpy array of shape (100, 2)
points = np.array([
    [383.96268, 343.33057], [383.7959, 343.7891], [383.601, 344.24063], 
    [383.37885, 344.68338], [383.1303, 345.11557], [382.85635, 345.53546], 
    [382.55814, 345.9413], [382.23685, 346.33154], [381.89377, 346.70456], 
    # ... (remaining points) ...
    [384.10074, 342.86694], [383.96268, 343.33057]
])

# Circle parameters: center (cx, cy) and radius r
cx, cy = 383, 343  # Example center
r = 10  # Example radius

# Calculate the distance of each point from the center (cx, cy)
distances = np.sqrt((points[:, 0] - cx) ** 2 + (points[:, 1] - cy) ** 2)

# Check the shape of distances
print("Shape of distances:", distances.shape)

# Check how many points are inside the circle
points_inside_circle_count = np.sum(distances <= r)

# Check if at least 10 points are inside the circle
if points_inside_circle_count >= 10:
    print("At least 10 points are inside the circle.")
else:
    print("Less than 10 points are inside the circle.")
