# Face Anonymizer 🎭

A Python application that detects and blurs faces in images and real-time webcam feeds using MediaPipe and OpenCV.

## 📋 Table of Contents
- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Keyboard Controls](#keyboard-controls)
- [File Structure](#file-structure)
- [Requirements](#requirements)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)
- [License](#license)

---

## ✨ Features

- **Face Detection**: Automatically detects faces using Google's MediaPipe BlazeFace model
- **Image Processing**: Process static images with face detection and blurring
- **Real-time Webcam**: Live face anonymization through your webcam
- **Dual View**: Compare original and anonymized versions side-by-side
- **Screenshot Capture**: Save anonymized frames with a single keypress
- **Toggle Mode**: Switch between blurred and original view in real-time
- **Automatic Model Download**: First-run automatically downloads the required AI model

---

## 🎬 Demo

### Image Mode (`main.py`)
- Detects faces in a static image
- Shows two windows:
  - **Original**: Image with green bounding boxes around detected faces
  - **Blurred**: Image with faces anonymized using Gaussian blur
- Saves both versions automatically

### Webcam Mode (`main_webcam.py`)
- Real-time face detection and blurring
- Toggle between original and blurred view
- Capture screenshots on demand
- Live processing at 30+ FPS

---

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- Webcam (for `main_webcam.py`)
- Windows/Linux/macOS

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/face-anonymizer.git
cd face-anonymizer
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install opencv-python mediapipe numpy
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

---

## 💻 Usage

### Image Processing Mode

1. **Place your image** in the project directory or update the path in `main.py`:
```python
img_path = r"path/to/your/image.jpg"
```

2. **Run the script**:
```bash
python main.py
```

3. **View results**:
   - Two windows will appear showing original and blurred versions
   - Press any key to close
   - Output images saved as:
     - `original_with_box.jpg`
     - `anonymized_blurred.jpg`

---

### Webcam Mode

1. **Run the script**:
```bash
python main_webcam.py
```

2. **Use keyboard controls** (see below)

3. **Exit**: Press `q` to quit

---

## ⌨️ Keyboard Controls

### Webcam Mode (`main_webcam.py`)

| Key | Action |
|-----|--------|
| `q` | Quit the application |
| `b` | Toggle between **Blurred** and **Original** view |
| `s` | Save screenshot of current view |

---

## 🧠 How It Works

### Face Detection Pipeline
```
Input Image/Frame
       ↓
Convert BGR → RGB
       ↓
MediaPipe Face Detection
       ↓
Extract Bounding Boxes
       ↓
Apply Gaussian Blur to Face Regions
       ↓
Display/Save Results
```

### Key Components

1. **MediaPipe BlazeFace Model**
   - Lightweight face detection model
   - Optimized for mobile and real-time applications
   - Returns bounding box coordinates for each detected face

2. **Gaussian Blur**
   - Kernel size: 99x99 pixels
   - Sigma: 30
   - Applied only to detected face regions

3. **Coordinate System**
```python
(x1, y1) ──────────┐
    │              │
    │    FACE      │  height
    │              │
    └──────────(x2, y2)
         width
```

---

## 📁 File Structure
```
face-anonymizer/
│
├── main.py                          # Image processing script
├── main_webcam.py                   # Webcam real-time script
├── blaze_face_short_range.tflite   # AI model (auto-downloaded)
├── person.jpg                       # Sample input image
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
│
└── output/
    ├── original_with_box.jpg        # Image with bounding boxes
    ├── anonymized_blurred.jpg       # Blurred faces image
    ├── screenshot_original.jpg      # Webcam screenshot (original)
    └── screenshot_blurred.jpg       # Webcam screenshot (blurred)
```

---

## 📦 Requirements

Create a `requirements.txt` file:
```txt
opencv-python>=4.8.0
mediapipe>=0.10.32
numpy>=1.24.0
```

Install all at once:
```bash
pip install -r requirements.txt
```

---

## 🔧 Troubleshooting

### Webcam Not Opening
```python
# Try different camera index in main_webcam.py
cap = cv2.VideoCapture(1)  # Try 0, 1, 2, etc.
```

### Slow Performance
Reduce resolution:
```python
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
```

Or use lighter blur:
```python
blurred_face = cv2.GaussianBlur(face_region, (51, 51), 15)
```

### Model Download Issues
Manually download from:
```
https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite
```
Save as `blaze_face_short_range.tflite` in project directory.

### "No module named 'mediapipe'" Error
```bash
pip uninstall mediapipe
pip install --no-cache-dir mediapipe
```

---

## 🎨 Customization

### Adjust Blur Intensity
```python
# Light blur
blurred_face = cv2.GaussianBlur(face_region, (21, 21), 10)

# Medium blur
blurred_face = cv2.GaussianBlur(face_region, (51, 51), 20)

# Heavy blur (default)
blurred_face = cv2.GaussianBlur(face_region, (99, 99), 30)
```

### Change Bounding Box Color
```python
# Red box
cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

# Blue box
cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
```

### Pixelation Instead of Blur
```python
# Replace blur code with:
h, w = face_region.shape[:2]
temp = cv2.resize(face_region, (w//15, h//15))
pixelated = cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)
img_blurred[y1:y2, x1:x2] = pixelated
```

---

## 🚀 Future Improvements

- [ ] Add pixelation mode
- [ ] Support for video file processing
- [ ] Batch processing for multiple images
- [ ] GUI
