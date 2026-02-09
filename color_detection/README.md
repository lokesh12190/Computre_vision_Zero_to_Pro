# Real-time Yellow Color Detection (OpenCV)

This project captures webcam video, converts frames to HSV, thresholds for **yellow**, and displays the original frame, mask, and the masked result.

## Files
- `main.py` — Webcam loop + HSV masking and display.
- `utils.py` — Helper function `get_limits(bgr_color, h_tol=10, s_min=100, v_min=100)` that returns HSV lower/upper bounds.

## Requirements
- Python 3.x
- OpenCV (`cv2`)
- NumPy

Install:
```bash
pip install opencv-python numpy
