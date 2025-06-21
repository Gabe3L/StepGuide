import cv2
import asyncio
import numpy as np
from numpy.typing import NDArray
from typing import Optional, List, Tuple, Sequence

from video.detector import YOLODetector
from video.display import VideoDisplay

###############################################################

ROTATE_IMAGE: bool = False
FLIP_IMAGE_HORIZONTALLY: bool = False
FLIP_IMAGE_VERTICALLY: bool = False

###############################################################

class VideoProcessor:
    def __init__(self) -> None:
        self.model = YOLODetector()

    def transform_frame(self, frame: np.ndarray) -> np.ndarray:
        if ROTATE_IMAGE:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        if FLIP_IMAGE_HORIZONTALLY:
            frame = cv2.flip(frame, 1)
        if FLIP_IMAGE_VERTICALLY:
            frame = cv2.flip(frame, 0)

        return frame

    def most_confident_box(self, boxes: NDArray[np.int32], confidences: NDArray[np.float32], class_ids: NDArray[np.int32]) -> Optional[Tuple[np.ndarray, int]]:
        if not confidences:
            return None

        max_index = np.argmax(confidences)
        box = boxes[max_index]
        label = class_ids[max_index]

        return box, label
    
    def get_video_feed(self) -> Optional[cv2.VideoCapture]:
        return cv2.VideoCapture(0)

    def process_video_feed(self, cap: cv2.VideoCapture):
        ret, frame = cap.read()
        if not ret:
            return False

        frame = self.transform_frame(frame)

        boxes, confidences, labels = self.model.detect(frame)

        for i, box in enumerate(boxes):
            if confidences[i] > 0.4:
                frame = VideoDisplay.annotate_frame(frame, box)

        cv2.imshow("Detections", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return False
        
        return True

###############################################################

if __name__ == "__main__":
    vp = VideoProcessor()
    cap = vp.get_video_feed()
    if cap is not None and cap.isOpened():
        while True:
            if not vp.process_video_feed(cap):
                break

    if cap:
        cap.release()
    cv2.destroyAllWindows()