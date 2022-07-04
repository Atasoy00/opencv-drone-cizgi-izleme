import numpy as np
import cv2


img = cv2.imread("turn_left.png")
Picx = 640
Picy = 480
img = cv2.resize(img,(Picx,Picy))
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_red1 = np.array([0, 50, 50], np.uint8)
upper_red1 = np.array([10, 255, 255], np.uint8)
mask1 = cv2.inRange(hsv, lower_red1, upper_red1)

lower_red2 = np.array([170, 50, 50],np.uint8)
upper_red2 = np.array([180, 255, 255],np.uint8)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

mask = mask1 + mask2

contours,h = cv2.findContours(mask,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)

buyuk = 0
worked =0
for cnt in contours:
    approx = cv2.approxPolyDP(cnt, .03 * cv2.arcLength(cnt, True), True)
    if len(approx)>=8:
        worked = 1
        area = cv2.contourArea(cnt)
        (cx, cy), radius = cv2.minEnclosingCircle(cnt)
        circleArea = radius * radius * np.pi
        if circleArea > buyuk:
            buyuk = circleArea
            tutucu = cnt
    else:
        if worked == 0:
            areas = [cv2.contourArea(c) for c in contours]
            max_index = np.argmax(areas)
            tutucu = contours[max_index]

yeni_mask = np.zeros((Picy,Picx), dtype=np.uint8)
cv2.drawContours(yeni_mask, [tutucu], 0, (255,255,255), -1)

x,y,w,h = cv2.boundingRect(tutucu)
cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)


cv2.imshow('img',img)
cv2.imshow('canvas',yeni_mask)
cv2.waitKey(0)
cv2.destroyAllWindows()

