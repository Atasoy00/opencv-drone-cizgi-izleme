import cv2

cap = cv2.VideoCapture("cd2.mp4")

i=0

while True:
    i=i+1
    ret, frame = cap.read()
    frame = cv2.resize(frame,(640,480))
    if i%25==0:
        Name1 = "D:\\Frame222\\{i}.png".format(i=i)
        cv2.imwrite(Name1, frame)

    cv2.imshow("Webcam",frame)
    cv2.waitKey(30)

cap.release()
cv2.destroyAllWindows()