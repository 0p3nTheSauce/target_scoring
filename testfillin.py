filled_in = np.zeros(ideal.shape, np.uint8)
missing = np.zeros(ideal.shape, np.uint8)
radii_m = []
with open('test_missing/missingr12_ellipses.txt', 'r') as file:
  lines = file.readlines()
ellipses_m = []
for line in lines:
  line = line.strip()  
  # Convert the string to a tuple and add it to the list
  ellipse = eval(line)
  cv2.ellipse(missing, ellipse, colour, thickness, cv2.LINE_8)
  ((cx, cy), (major_axis, minor_axis), angle) = ellipse
  radius = int((major_axis + minor_axis)//2)
  radii_m.append(radius)
  ellipses_m.append(ellipse)
#reverse for consistency
ellipses_m.reverse()
radii_m.reverse()
#Calculate the differences between the radii
diffs_rings_m = []
for i in range(1, len(radii_m)):
  diffs_rings_m.append(radii_m[i-1] - radii_m[i])
  
filled_radii_m, filled_diffs_m = fill_in_missing(radii_i, diffs_rings_i, radii_m, diffs_rings_m)

cv2.imshow("Missing", missing)
cv2.imshow("Filled In", filled_in)