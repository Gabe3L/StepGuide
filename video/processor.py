from ultralytics import YOLO
import cv2

class VideoProcessor:
    def __init__(self) -> None:
        pass

    def process_video(self):
        model = YOLO("yolo11n.pt", task='detect')

        cap = cv2.VideoCapture(0)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            results = model(frame)

            annotated_frame = results[0].plot()

            cv2.imshow("YOLO Detection", annotated_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    vp = VideoProcessor()
    vp.process_video()