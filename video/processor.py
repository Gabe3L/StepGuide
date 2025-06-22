import numpy as np
from numpy.typing import NDArray
from typing import Optional, Tuple

import cv2
from cv2.typing import MatLike

from video.detector import YOLODetector
from video.display import VideoDisplay

###############################################################

ROTATE_IMAGE: bool = False
FLIP_IMAGE_HORIZONTALLY: bool = True
FLIP_IMAGE_VERTICALLY: bool = False

###############################################################


class VideoProcessor:
    def __init__(self) -> None:
        self.model = YOLODetector()

    def transform_frame(self, frame: MatLike) -> MatLike:
        if ROTATE_IMAGE:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        if FLIP_IMAGE_HORIZONTALLY:
            frame = cv2.flip(frame, 1)
        if FLIP_IMAGE_VERTICALLY:
            frame = cv2.flip(frame, 0)

        return frame

    def process_video_feed(self, frame: MatLike) -> bool:
        if frame is None:
            return False

        frame = self.transform_frame(frame)

        boxes, confidences, labels = self.model.detect(frame)

        for i, box in enumerate(boxes):
            if confidences[i] > 0.4:
                frame = VideoDisplay.annotate_frame(frame, box)

        cv2.imshow("Detections", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            return False

        return True