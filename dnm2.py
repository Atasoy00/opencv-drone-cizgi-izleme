import cv2
import numpy as np

cap = cv2.VideoCapture("cd1.mp4")


while True:
    ret,frame = cap.read()
    frame = cv2.resize(frame,(640,480))
    frame = cv2.flip(frame, 0)
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    _,mask2 = cv2.threshold(gray,80,100,cv2.THRESH_BINARY)

    lower_yellow = np.array([0,0,0],np.uint8)
    upper_yellow = np.array([180,255,80],np.uint8)

    mask = cv2.inRange(hsv,lower_yellow,upper_yellow)

    edges = cv2.Canny(mask,20,255)

    lines = cv2.HoughLinesP(image=edges,rho=1,theta=np.pi/180,threshold=20,maxLineGap=50)

    try:
        for line in lines:
            (x1, y1, x2, y2) = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
    except:
        print("An exception occurred")


    cv2.imshow("Webcam",frame)
    cv2.imshow("Webcam0",mask2)
    cv2.waitKey(30)

cap.release()
cv2.destroyAllWindows()