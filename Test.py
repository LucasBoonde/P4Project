import cv2
import numpy as np
import math

# Load the image
img = cv2.imread('Papir2.jpeg')
cv2.imshow('Original Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply adaptive thresholding to create a binary image
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)

# Apply morphological operations to remove noise and thin lines
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
erosion = cv2.erode(thresh, kernel, iterations=1)
dilation = cv2.dilate(erosion, kernel, iterations=2)

# Find contours in the dilated image
contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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

# A3 diagonal = 514.40 mm
# A3 diagonal in pixels = 387.48677396783495
# Pixels per metric = object width / known width
diagonalMM = 514.40
diagonalPxl = math.sqrt((w-x)**2+(h-y)**2)
PPM = diagonalPxl / diagonalMM

# Crop the image to the bounding box
cropped_image = img[y:y+h, x:x+w]

# Display the cropped image
cv2.imshow('Cropped Image', cropped_image)
cv2.waitKey(0)

# --- EDGE DETECTION INSIDE PAPER ---

# Convert the cropped image to grayscale
gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

# Apply a threshold to create a binary image
ret, thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY_INV)

# Find the contours in the image
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Find the largest contour
largest_contour = max(contours, key=cv2.contourArea)

# Generate evenly spaced points along the perimeter of the contour using polar coordinates
center, radius = cv2.minEnclosingCircle(largest_contour)
n_points = 50
values = np.arange(0, 2*math.pi, 2*math.pi/n_points)
points = [tuple(map(int, cv2.polarToCart(radius, angle, center))) for angle in values]
print('points',points)
#points = [tuple(map(int, point)) for point in cv2.polarToCart(radius, angle, center, True)]


# Make the points relative to the reference point (in this case, the top-left corner of the cropped image)
ref_point = (x, y)
points = [(point[0] - ref_point[0], point[1] - ref_point[1]) for point in points]

# Display the image with the contour and points
cv2.drawContours(img, [largest_contour], 0, (0, 255, 0), 2)
for point in points:
    cv2.circle(img, point, 3, (0, 0, 255), -1)
cv2.imshow('Contour and Points', img)
cv2.waitKey(0)
cv2.destroyAllWindows()


# Define the reference point (in this case, the top-left corner of the image)
ref_point = x #The top left side of the paper

# Make the points relative to the reference point
points = [(point[0] - ref_point[0], point[1] - ref_point[1]) for point in points]


# Print the relative points
print(points)