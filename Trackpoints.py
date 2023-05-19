import cv2
import numpy as np
from matplotlib import pyplot as plt

# Find Reference point
# Find størrelsesforhold mellem pixel og A3 papir 297 x 420 mm
# Find Size of paper in pixels / mm.
# Converter billede til grayscale
# Lav ROI så vi kun ser på papiret
# Lav edgedetection på ROI - Sobel / Canny edge detection for isolation af streg
# Binary Image, Euclidian Transform, Skeletonize for single edge.
# Find hjørner på stregen
# Iterpolate stregen og dan x antal punkter

img = cv2.imread('Papir.jpg')

#binary = np.float32(binary)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#gray = cv2.threshold(img, 150,255,cv2.THRESH_BINARY)
gray = np.float32(gray)
dst = cv2.cornerHarris(gray, 10, 3, 0.04)
ret, dst = cv2.threshold(dst,0.1*dst.max(),255,0)
dst=np.uint8(dst)
ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,100,0.001)
corners = cv2.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)

points=[]

for i in range(1,len(corners)):
    print(corners[i])
    print(len(corners))
    print("hej")
img[dst>0.1*dst.max()]=[0,0,255]

x1 = corners[1]
y1 = corners[2]
x2 = corners[3]
y2 = corners[4]
print('x1',x1[1])
img1 = img[int(x1[0]):int(x2[0]),int(y1[1]):int(y2[1])]
#img_crop = np.array()
#img_crop = [y1:y1+y2, x1:x1+x2]


print('x2',x2)
print('y2',y2)

#cv2.imshow("crop", img_crop)
#dst = cv2.cornerHarris(binary, 2, 3, 0.04)

#dst=cv2.dilate(dst,None)
#img[dst>0.01*dst.max()]=[0,0,255]

cv2.imshow('papir', img1)
cv2.waitKey(0)
#def TrajectoryGenerationPoints(image)
    #Load Image
    #img = cv2.imread('OriginalImage', image)


    #return points




