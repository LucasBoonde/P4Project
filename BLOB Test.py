import math
import matplotlib.pyplot as plt
import cv2
from skimage.morphology import skeletonize
import numpy as np


# Load the image
img = cv2.imread('paperSetup.jpg')
cv2.imshow("img", img)
cv2.waitKey(0)

#Isolate the reference point in the image
# Define lower and upper bounds for blue color in RGB format
lower_blue = np.array([0, 0, 200])
upper_blue = np.array([50, 50, 255])

# Create a mask using the defined bounds
mask = cv2.inRange(img, lower_blue, upper_blue)

# Apply the mask to the original image
blue_objects = cv2.bitwise_and(img, img, mask=mask)

# Convert the isolated blue pixels to binary
gray = cv2.cvtColor(blue_objects, cv2.COLOR_BGR2GRAY)
ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)

# Find contours in the binary image
contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
erosion = cv2.erode(binary, kernel, iterations=1)
dilation = cv2.dilate(erosion, kernel, iterations=2)
# Display the result

# Find the largest contour
largest_contour = None
largest_contour_area = 0
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > largest_contour_area:
        largest_contour = cnt
        largest_contour_area = area

# Draw a red circle at the center of the largest contour
if largest_contour is not None:
    M = cv2.moments(largest_contour)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    #img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.circle(img, (cx, cy), 5, (0, 0, 255), -1)

print(cx)
print(cy)


# Display the result
"""cv2.imshow('Original Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()"""

#--- Crop the image to paper view

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('img', gray)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Apply adaptive thresholding to create a binary image
#thresh = cv2.adaptiveThreshold(gray, 255 ,  cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 41, 21)
ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY, 2)

"""cv2.imshow('Thresh', thresh)
cv2.waitKey(0)"""

# Apply morphological operations to remove noise and thin lines
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
erosion = cv2.erode(thresh, kernel, iterations=1)
dilation = cv2.dilate(erosion, kernel, iterations=2)

# Create a copy of the original image to draw on
img_contours = img.copy()

# Find contours in the dilated image
contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# Draw the contours on the image in green color with thickness 2
cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 2)

# Display the image with contours
"""cv2.imshow('Image with Contours', img_contours)
cv2.waitKey(0)
cv2.destroyAllWindows()"""

# Find the contour with the largest area
max_area = 0
max_contour = None
for contour in contours:
    area = cv2.contourArea(contour)
    if area > max_area:
        max_area = area
        max_contour = contour

# Determine the bounding box of the contour
x, y, w, h = cv2.boundingRect(max_contour)



# plot the image
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

# plot the bounding box
rect = plt.Rectangle((x, y), w, h, fill=False, edgecolor='red', linewidth=2)
plt.gca().add_patch(rect)

# show the plot
plt.show()
#This code will create a plot of the image with a red rectangle around the bounding box of the contour. You can adjust the edgecolor and linewidth arguments to change the appearance of the rectangle.


# A3 diagonal = 514.40 mm
# A3 diagonal in pixels = 387.48677396783495

#Pixels per metric = object width / known width

diagonalMM = 514.40
diagonalPxl = math.sqrt((w-x)**2+(h-y)**2)

PPM = diagonalPxl / diagonalMM

#p = (w-x)**2
"""print('p', p)
print('h',h)
print('x',x)
print('y',y)
print('w',w)
print(diagonalPxl)
print('PPM',PPM)"""

# Crop the image to the bounding box
#cropped_image = img[y:y+h, x:x+w]
cropped_image = img[y:y+h, x:x+w]

# Display the cropped image
"""cv2.imshow('Cropped Image1', cropped_image)
cv2.waitKey(0)"""

# --- EDGE DETECTION INSIDE PAPER ---

img = cropped_image

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply a threshold to create a binary image
ret, thresh = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY_INV)
"""cv2.imshow('Thresh', thresh)
cv2.waitKey(0)"""



# Apply morphological operations to remove noise and thin lines
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
dilation = cv2.dilate(thresh, kernel, iterations=2)
erosion = cv2.erode(dilation, kernel, iterations=1)

#Skeletonize the BLOB
skeleton = skeletonize(erosion)
print('Skeleton DType', skeleton.dtype)
skeleton = skeleton.astype(np.uint8)

# Find the contours in the image
contours, hierarchy = cv2.findContours(skeleton, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Find the largest contour
largest_contour = max(contours, key=cv2.contourArea)

# Get the perimeter of the largest contour
perimeter = cv2.arcLength(largest_contour, True)

# Generate X evenly spaced points along the perimeter of the contour
n_points = 10
points = [tuple(largest_contour[int(i * perimeter / n_points) % len(largest_contour)][0]) for i in range(n_points)]

print(points)
print(len(points))

# Display the image with the contour and points
cv2.drawContours(img, [largest_contour], 0, (0, 255, 0), 2)
for point in points:
    cv2.circle(img, point, 3, (0, 0, 255), -1)
    print('current point', point)
"""cv2.imshow('Contour and Points', img)
cv2.waitKey(0)
cv2.destroyAllWindows()"""

print('Len Point', len(point))

# Define the reference point (in this case, the top-left corner of the image)
ref_point = [cx, cy - 280] #Reference point minus the length in the x and y direction to the actual 0-point


#Length to points in real life
#Pixels per metric = object width / known width

# Make the points relative to the reference point

points = [(math.sqrt(abs(point[0]**2 - ref_point[0]**2)) / PPM,
           math.sqrt(abs(point[1]**2 - ref_point[1]**2)) / PPM)
          for point in points]
#points = [(point[0] - ref_point[0], point[1] - ref_point[1]) for point in points]

# Print the relative points
print('points', points)
print('point[0]', points[0])
print('point[1]', points[1])


cv2.imshow('Contour and Points', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
