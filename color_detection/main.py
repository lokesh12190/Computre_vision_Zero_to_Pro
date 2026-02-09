import cv2
import numpy as np
from utils import get_limits

cap = cv2.VideoCapture(0)

yellow_bgr = (0, 255, 255)
lower, upper = get_limits(yellow_bgr)

# tweak these if needed
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
min_area = 800

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)

    # clean mask: opening removes small noise, closing fills small holes 
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)

    # find biggest yellow blob and draw bbox [web:107]
    contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]  

    if contours:
        c = max(contours, key=cv2.contourArea)
        if cv2.contourArea(c) > min_area:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    cv2.imshow("yellow", result)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
