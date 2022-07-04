import cv2
import numpy as np

img = cv2.imread("dnm222.png")
img = cv2.resize(img,(640,480))
blurred = cv2.pyrMeanShiftFiltering(img, 3, 3)
kernel = np.ones((2,2),np.uint8)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_red1 = np.array([0, 50, 50], np.uint8)
upper_red1 = np.array([10, 255, 255], np.uint8)
mask1 = cv2.inRange(hsv, lower_red1, upper_red1)

lower_red2 = np.array([170, 50, 50],np.uint8)
upper_red2 = np.array([180, 255, 255],np.uint8)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

mask = mask1 + mask2

dilation = cv2.dilate(mask,kernel,iterations = 1)

closing = cv2.morphologyEx(dilation, cv2.MORPH_GRADIENT, kernel)
closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)

#Getting the edge of morphology
edge = cv2.Canny(closing, 175, 175)
contours,hierarchy = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Find the index of the largest contour
areas = [cv2.contourArea(c) for c in contours]
max_index = np.argmax(areas)
cnt=contours[max_index]

x,y,w,h = cv2.boundingRect(cnt)
cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)


cv2.imshow('threshold', img)
cv2.imshow('edge', edge)

cv2.waitKey(0)
cv2.destroyAllWindows()