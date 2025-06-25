import cv2
from hands.hands import HandTracking

################################################################

if __name__ == "__main__":
    try:
        hands = HandTracking()
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise RuntimeError("Failed to open camera.")
    
        while True:
            ret, frame = cap.read()
            if not ret:
                raise RuntimeError("Failed to capture frame from camera.")
            
            frame = hands.process_frame(frame)

            cv2.imshow('Hand Tracking', frame)
            if cv2.waitKey(5) & 0xFF == 27:
                break
        cap.release()
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"Error: {e}")