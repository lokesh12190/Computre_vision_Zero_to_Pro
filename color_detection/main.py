import cv2
from utils import get_limits  

cap = cv2.VideoCapture(0)

# yellow in BGR (OpenCV uses BGR order)
yellow_bgr = (0, 255, 255)
lower, upper = get_limits(yellow_bgr)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    cv2.imshow("yellow", result)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

