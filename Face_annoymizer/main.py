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

img_path = r"C:\Users\lokes\Desktop\computer vision\projects\Face_annoymizer\person.jpg"
img = cv2.imread(img_path)
if img is None:
    raise FileNotFoundError(f"Could not read image: {img_path}")

# Create a copy for the blurred version
img_blurred = img.copy()

# Create FaceDetector
base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.FaceDetectorOptions(base_options=base_options)
detector = vision.FaceDetector.create_from_options(options)

# Convert to MediaPipe Image format
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)

# Detect faces
detection_result = detector.detect(mp_image)

# Process each detected face
if detection_result.detections:              # If faces found
    for detection in detection_result.detections:  # For each face
        bbox = detection.bounding_box        # Get its box info
        
        # Calculate the 4 corners of the rectangle:
        x1 = int(bbox.origin_x)              # Left edge
        y1 = int(bbox.origin_y)              # Top edge
        x2 = int(bbox.origin_x + bbox.width)  # Right edge
        y2 = int(bbox.origin_y + bbox.height) # Bottom edge
        
        # Now we have: (x1, y1) = top-left, (x2, y2) = bottom-right
        # We can use these to draw or blur!
        
        # Make sure coordinates are within image boundaries
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(img.shape[1], x2)
        y2 = min(img.shape[0], y2)
        
        # Draw bounding box on original image
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # Extract the face region from blurred copy
        face_region = img_blurred[y1:y2, x1:x2]
        
        # Apply Gaussian blur to the face region
        blurred_face = cv2.GaussianBlur(face_region, (99, 99), 30)
        
        # Replace the original face region with the blurred version
        img_blurred[y1:y2, x1:x2] = blurred_face

# Display both windows
cv2.imshow("Original with Bounding Box", img)
cv2.imshow("Anonymized (Blurred)", img_blurred)

print("Press any key to close the windows...")
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save both results
cv2.imwrite("original_with_box.jpg", img)
cv2.imwrite("anonymized_blurred.jpg", img_blurred)
print("Saved both images!")