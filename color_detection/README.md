# Real-time Yellow Color Detection (OpenCV)

This project captures webcam video, converts frames to HSV, thresholds for **yellow**, and displays the original frame, mask, and the masked result.

## Files
- `main.py` — Webcam loop + HSV masking and display.
- `utils.py` — Helper function `get_limits(bgr_color, h_tol=10, s_min=100, v_min=100)` that returns HSV lower/upper bounds.

- <img width="1920" height="1080" alt="Screenshot 2026-02-09 232111" src="https://github.com/user-attachments/assets/099765ea-ea30-4d9f-958f-81e6ba198bfb" />


## Requirements
- Python 3.x
- OpenCV (`cv2`)
- NumPy

Install:
```bash
pip install opencv-python numpy
