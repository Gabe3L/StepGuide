import cv2
import pytesseract
from PIL import  Image

# Open the default webcam (0 = default camera)
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Continuously read frames
while True:
    ret, frame = cap.read()  # Read a frame from the webcam
    cv2.flip(frame, 1)
    if not ret:
        print("Failed to grab frame.")
        break

    cv2.imshow('Webcam Feed', frame)  # Show the frame in a window

    # Exit loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
