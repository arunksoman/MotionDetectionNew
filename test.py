import cv2

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow("output", frame)
    k = cv2.waitKey(1)
    if k == 27:
        break

cv2.destroyAllWindows()
