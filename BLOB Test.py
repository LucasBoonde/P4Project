import math

import cv2
import numpy as np

# Load the image
img = cv2.imread('Papir2.jpeg')

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

ref = math.sqrt((w-x)^2+(h-y)^2)
print(ref)

# Crop the image to the bounding box
cropped_image = img[y:y+h, x:x+w]

# Display the cropped image
cv2.imshow('Cropped Image', cropped_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
