import cv2
import numpy as np

# Load the images
ideal_img = cv2.imread('ideal_map.jpg', cv2.IMREAD_GRAYSCALE)
distorted_img = cv2.imread('black_score.jpg', cv2.IMREAD_GRAYSCALE)

# Initialize the ORB detector
orb = cv2.ORB_create()

# Detect keypoints and descriptors
keypoints1, descriptors1 = orb.detectAndCompute(ideal_img, None)
keypoints2, descriptors2 = orb.detectAndCompute(distorted_img, None)

# Match descriptors using Brute-Force Matcher with Hamming distance
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(descriptors1, descriptors2)

# Sort matches by distance (lower distance is better)
matches = sorted(matches, key=lambda x: x.distance)

# Draw the top matches (optional)
match_img = cv2.drawMatches(ideal_img, keypoints1, distorted_img, keypoints2, matches[:20], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

# Find the points corresponding to the best matches
pts1 = np.float32([keypoints1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
pts2 = np.float32([keypoints2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

# Compute the homography matrix
H, mask = cv2.findHomography(pts2, pts1, cv2.RANSAC)

# Warp the distorted image to align with the ideal image
aligned_img = cv2.warpPerspective(distorted_img, H, (ideal_img.shape[1], ideal_img.shape[0]))

# Show results
cv2.imshow("Aligned Image", aligned_img)
cv2.imshow("Match Image", match_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
