import cv2
import numpy as np
import math

cap = cv2.VideoCapture(0) #"cd2.mp4"
hata = 0

while True:
    try:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (640, 480))
        #frame = cv2.flip(frame, 0)
        #frame = cv2.rotate(frame, cv2.cv2.ROTATE_90_CLOCKWISE)

        # roi
        x1, y1 = (128, 240)
        roi1 = frame[240 - (y1 // 2):240 + (y1 // 2), 320 - (x1 // 2):320 + (x1 // 2)]  # [y,x]

        # renk maskeleme
        hsv = cv2.cvtColor(roi1, cv2.COLOR_BGR2HSV)

        lower_black = np.array([0, 0, 0], np.uint8)
        upper_black = np.array([180, 255, 80], np.uint8)

        mask = cv2.inRange(hsv, lower_black, upper_black)

        # moments
        M1 = cv2.moments(mask)

        if M1["m00"] == 0:
            M1["m00"] = 1

        mx1 = int(M1["m10"] / M1["m00"])
        my1 = int(M1["m01"] / M1["m00"])

        # new roi
        x2, y2 = (128, my1)
        roi2 = mask[0:y2, 0:x2]  # [y,x]

        # moments2
        M2 = cv2.moments(roi2)

        if M2["m00"] == 0:
            M2["m00"] = 1

        mx2 = int(M2["m10"] / M2["m00"])
        my2 = int(M2["m01"] / M2["m00"])

        #print(mx1,my1,mx2,my2)

        #cizgi ciz
        cv2.line(mask, (mx1,my1), (mx2,my2), (0,0,255), 2)
        cv2.circle(mask, (mx2,my2), 10, (0,0,0), -1)
        cv2.circle(mask, (mx2,my2), 5, (255,255, 255), -1)
        cv2.circle(mask, (mx1,my1), 10, (0,0,0), -1)
        cv2.circle(mask, (mx1,my1), 5, (255,255, 255), -1)

        # tuval
        img = mask
        canvas = np.zeros((480, 640), np.uint8) + 127
        ax, ay = (640 - img.shape[1]) // 2, (480 - img.shape[0]) // 2
        canvas[ay:img.shape[0] + ay, ax:ax + img.shape[1]] = img

        #cizgi acisi
        if mx1<mx2: #sağa yatık
            alfa = math.atan(abs(my1 - my2) / abs(mx2 - mx1))
            alfa = alfa * 57.2957795
            Degree = alfa
            print("<---")
        if mx2<mx1: #sola yatık
            beta = math.atan(abs(my1 - my2) / abs(mx1 - mx2))
            beta = beta * 57.2957795
            Degree = 180-beta
            print("--->")
        else:
            print("||")


        #print(mx1,my1,mx2,my2)
        print(int(Degree))
        #Sum_White = np.sum(img == 255)
        #print(Sum_White)


        #uçuş prosedürü
            #1 beyaz görmüyorsan sağa veya sola yat, beyaz görmeye çalış
            #2 yönünü beyaz çizginin doğrultusuna çevir
            #3 biraz ilerle ve başa sar

    except:
        hata = hata+1
        print("Hata Sayaci :",hata)

    cv2.imshow("Pencere0", frame)
    cv2.imshow("Pencere1", canvas)
    cv2.waitKey(30)

cap.release()
cv2.destroyAllWindows()