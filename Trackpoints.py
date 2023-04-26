import cv2
# Find Reference point

# Find størrelsesforhold mellem pixel og A3 papir 297 x 420 mm

# Find Size of paper in pixels / mm.

# Converter billede til grayscale

# Lav ROI så vi kun ser på papiret

# Lav edgedetection på ROI - Sobel / Canny edge detection for isolation af streg

# Binary Image, Euclidian Transform, Skeletonize for single edge.

# Find hjørner på stregen

# Iterpolate stregen og dan x antal punkter


def TrajectoryGenerationPoints(image):
    #Load Image
    img = cv2.imread('OriginalImage', image)








    return points





