import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import urllib.request
import os

# Download the model file if it doesn't exist
model_path = 'blaze_face_short_range.tflite'
if not os.path.exists(model_path):
    print("Downloading face detection model...")
    url = 'https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite'
    urllib.request.urlretrieve(url, model_path)
    print("Model downloaded successfully!")

# Create FaceDetector
base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.FaceDetectorOptions(base_options=base_options)
detector = vision.FaceDetector.create_from_options(options)

# Open webcam (0 is default camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cannot access webcam")
    exit()

print("Webcam started! Press 'q' to quit, 'b' to toggle blur, 's' to save screenshot")

# Blur mode toggle
blur_mode = True

while True:
    # Read frame from webcam
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Cannot read frame")
        break
    
    # Create a copy for blurred version
    frame_blurred = frame.copy()
    
    # Convert to RGB for MediaPipe
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
    
    # Detect faces
    detection_result = detector.detect(mp_image)
    
    # Process each detected face
    if detection_result.detections:
        for detection in detection_result.detections:
            bbox = detection.bounding_box
            x1 = int(bbox.origin_x)
            y1 = int(bbox.origin_y)
            x2 = int(bbox.origin_x + bbox.width)
            y2 = int(bbox.origin_y + bbox.height)
            
            # Make sure coordinates are within frame boundaries
            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(frame.shape[1], x2)
            y2 = min(frame.shape[0], y2)
            
            # Draw bounding box on original frame
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Apply blur to the blurred version
            face_region = frame_blurred[y1:y2, x1:x2]
            
            if face_region.size > 0:  # Check if region is valid
                blurred_face = cv2.GaussianBlur(face_region, (99, 99), 30)
                frame_blurred[y1:y2, x1:x2] = blurred_face
    
    # Display the selected mode
    if blur_mode:
        cv2.imshow("Webcam - Face Anonymizer (Blurred)", frame_blurred)
    else:
        cv2.imshow("Webcam - Face Anonymizer (Original)", frame)
    
    # Handle keyboard input
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('q'):
        # Quit
        print("Exiting...")
        break
    elif key == ord('b'):
        # Toggle blur mode
        blur_mode = not blur_mode
        mode_text = "BLURRED" if blur_mode else "ORIGINAL"
        print(f"Switched to {mode_text} mode")
    elif key == ord('s'):
        # Save screenshot
        if blur_mode:
            cv2.imwrite("screenshot_blurred.jpg", frame_blurred)
            print("Saved screenshot_blurred.jpg")
        else:
            cv2.imwrite("screenshot_original.jpg", frame)
            print("Saved screenshot_original.jpg")

# Release resources
cap.release()
cv2.destroyAllWindows()
print("Webcam closed!")