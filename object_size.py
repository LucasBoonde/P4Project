#Importing the necessary packages
from imutils import perspective
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2

#Defining midpoint of object
def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

# Construct some arguments parse and parse arguments - Seems like a good habit for when other people use the code
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True, help="path to the input image")
#ap.add_argument("-w", "--width", type=float, required=True, help="width of the known object size (in milimeters)")
#args = vars(ap.parse_args())

#Load the image, convert it to grayscale, and blur ir slightly
#image = cv2.imread(args["image"])
image = cv2.imread('paper.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
gray = cv2.GaussianBlur(gray, (15, 15), 0)
cv2.imshow('image', image)
cv2.waitKey(0)

#Perform edge detection, then perform morphology to close gabs between object edges
edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

#Find contours in the edge map
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

#sort the contours from left to right and initate the pixels per metric callibration variable
(cnts, _) = contours.sort_contours(cnts)
pixelsPerMetric = None

#Loop over the contours individually
for c in cnts:
    #If the contour is not sufficiently large, then it is ignored
    if cv2.contourArea(c) < 100:
        continue

    #Compute the rotated bounding box of the contour
    orig = image.copy()
    box = cv2.minAreaRect(c)
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box, dtype="int")

    """Order the points in the contour so that they appear in the following order:
     top-left, top-right, bottom-right, bottom-left, and then draw an outline around it"""
    box = perspective.order_points(box)
    cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

    #Loop over the original points and draw them
    for (x, y) in box:
        cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

    """ Unpack the ordered bounding box, then compute the 
    midpoint between the top-left and the top-right coordinates, 
    followed by the midpoint between the bottom-left and bottom-right
    """
    (tl, tr, br, bl) = box
    (tltrX, tltrY) = midpoint(tl, tr)
    (blbrX, blbrY) = midpoint(bl, br)
    # compute the midpoint between the top-left and top-right points,
    # followed by the midpoint between the top-righ and bottom-right
    (tlblX, tlblY) = midpoint(tl, bl)
    (trbrX, trbrY) = midpoint(tr, br)
    # draw the midpoints on the image
    cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
    cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
    cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
    cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

    #Draw the lines between the midpoint
    cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)), (255, 0, 255), 2)
    cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)), (255, 0, 255), 2)

    #Compute the euclidian distance between the midpoints
    dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
    dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

    """If the Pixels Per Metric hasn't been initialized, then compute it as the ration of pixels to supply the metric (in mm)"""

    if pixelsPerMetric is None:
        pixelsPerMetric = dB / 297#args["width"]

    #Compute the sixe of the object
    dimA = dA / pixelsPerMetric
    dimB = dB / pixelsPerMetric

    # Draw the object size on the image
    cv2.putText(orig, "{:.1f}mm".format(dimA),
                (int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
                0.65, (255, 255, 255), 2)

    #Show the output Image
    cv2.imshow("Image", orig)
    cv2.waitKey(0)



