import cv2
from video.processor import VideoProcessor


if __name__ == "__main__":
    vp = VideoProcessor()
    cap = cv2.VideoCapture(0)
    if cap is not None and cap.isOpened():
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if not vp.process_video_feed(frame):
                break

    if cap:
        cap.release()
    cv2.destroyAllWindows()
