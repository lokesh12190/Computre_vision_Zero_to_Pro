import numpy as np
import cv2

def get_limits(bgr_color, h_tol=10, s_min=100, v_min=100):
    """
    bgr_color: (B, G, R) tuple/list, e.g. (0, 255, 0)
    returns: (lower, upper) as np.array([H,S,V], dtype=np.uint8)
    """
    c = np.uint8([[bgr_color]])  # shape (1,1,3)
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)  # BGR -> HSV [web:17]

    h = int(hsvC[0, 0, 0])  # Hue in OpenCV HSV is in [0, 179] [web:22]

    lower = np.array([max(h - h_tol, 0),   s_min, v_min], dtype=np.uint8)
    upper = np.array([min(h + h_tol, 179), 255,   255],  dtype=np.uint8)

    return lower, upper
