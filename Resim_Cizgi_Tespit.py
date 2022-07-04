import cv2
import numpy as np

frame = cv2.imread("C:\\Users\\ataso\\Desktop\\cd2Frames\\175.png")

frame = cv2.resize(frame,(640,480))
frame = cv2.flip(frame,1)

#roi
x1,y1 = (128,240)
roi1 = frame[240-(y1//2):240+(y1//2), 320-(x1//2):320+(x1//2)] #[y,x]

#renk maskeleme
hsv = cv2.cvtColor(roi1,cv2.COLOR_BGR2HSV)

lower_black = np.array([0,0,0],np.uint8)
upper_black = np.array([180,255,80],np.uint8)

mask = cv2.inRange(hsv,lower_black,upper_black)


#moments
M1 = cv2.moments(mask)

if M1["m00"] == 0:
    M1["m00"] = 1

mx1 = int(M1["m10"]/M1["m00"])
my1 = int(M1["m01"]/M1["m00"])

cv2.circle(mask,(mx1,my1),10,(255,255,255),-1)
cv2.circle(mask,(mx1,my1),4,(0,0,0),-1)

#new roi
x2,y2 = (128,my1)
roi2 = mask[0:y2,0:x2] #[y,x]

'''
#en tepedeki beyaz nokta koordinatı
tepeX,tepeY = (x2//2,0)
for i in range(x2):
    for j in range(y2):
        if roi2[i,j] == 255:
            tepeX,tepeY = (i,j)
            print(tepeX,tepeY)
            break
    break
'''

#moments2
M2 = cv2.moments(roi2)

mx2 = int(M2["m10"]/M2["m00"])
my2 = int(M2["m01"]/M2["m00"])

cv2.circle(mask,(mx2,my2),10,(255,255,255),-1)
cv2.circle(mask,(mx2,my2),4,(0,0,0),-1)


#tuval
img = mask
canvas = np.zeros((480,640),np.uint8)+127
ax,ay = (640 - img.shape[1])//2,(480 - img.shape[0])//2
canvas[ay:img.shape[0]+ay , ax:ax+img.shape[1]] = img

try:
    print("Onurcan")

except:
    print("An exception occurred")

cv2.imshow("Webcam",frame)
cv2.imshow("Webcam0",canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()