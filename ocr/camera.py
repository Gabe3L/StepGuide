import cv2
import pytesseract
import time
import sys
import platform
from PIL import Image

def ocr(frame):
    # Convert BGR to RGB for pytesseract
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convert to PIL Image       
    pil_img = Image.fromarray(rgb)

    # Run OCR
    text = pytesseract.image_to_string(pil_img, lang='eng')

    return text

# Print system information for debugging
print(f"OpenCV version: {cv2.__version__}")
print(f"Python version: {sys.version}")
print(f"Operating System: {platform.system()} {platform.release()}")

# Try different camera indices
camera_index = 0  # Start with default camera

# On macOS, try to use a more compatible API
if platform.system() == 'Darwin':  # macOS
    print("Running on macOS, trying compatible camera API...")
    # Try different API backends on macOS
    cap = cv2.VideoCapture(camera_index, cv2.CAP_AVFOUNDATION)
else:
    cap = cv2.VideoCapture(camera_index)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam with index 0.")
    # Try alternative camera indices
    for i in range(1, 3):
        print(f"Trying camera index {i}...")
        if platform.system() == 'Darwin':
            cap = cv2.VideoCapture(i, cv2.CAP_AVFOUNDATION)
        else:
            cap = cv2.VideoCapture(i)
        
        if cap.isOpened():
            print(f"Successfully opened camera with index {i}")
            break
    
    if not cap.isOpened():
        print("Could not open any camera. Exiting.")
        exit()

# Give the camera some time to initialize
print("Initializing camera...")
time.sleep(2)

# Set camera properties for better performance
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Continuously read frames
frame_count = 0
while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    
    if not ret:
        print(f"Failed to grab frame. Attempt: {frame_count + 1}")
        # Try a few more times before giving up
        if frame_count < 5:
            frame_count += 1
            time.sleep(0.5)
            continue
        else:
            print("Multiple failures to grab frame. Exiting.")
            break
    
    # Reset counter on successful frame grab
    frame_count = 0
    
    # Flip the frame horizontally for mirror effect
    # frame = cv2.flip(frame, 1)

    cv2.imshow('Webcam Feed', frame)  # Show the frame in a window

    # Exit loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    print(ocr(frame))



# Release resources
cap.release()
cv2.destroyAllWindows()
