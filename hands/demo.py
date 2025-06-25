import cv2
from hands.hands import HandTracker

################################################################

if __name__ == "__main__":
    try:
        hand_tracker = HandTracker()
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise RuntimeError("Failed to open camera.")
    
        while True:
            ret, frame = cap.read()
            if not ret:
                raise RuntimeError("Failed to capture frame from camera.")
            
            results = hand_tracker.process_frame(frame)
            frame = hand_tracker.annotate_frame(frame, results)

            cv2.imshow('Hand Tracking', frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        cap.release()
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"Error: {e}")