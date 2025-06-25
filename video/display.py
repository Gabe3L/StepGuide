import cv2
import numpy as np

###############################################################

class VideoDisplay:
    @staticmethod
    def show_frame(window_name: str, frame: np.ndarray) -> None:
        """Displays the frame in a window."""
        cv2.imshow(window_name, frame)

    @staticmethod
    def annotate_frame(frame: np.ndarray, box: np.ndarray) -> np.ndarray:
        """Annotate the frame with bounding boxes and labels."""
        return cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 0, 0), 2)

    @staticmethod
    def insert_text_onto_frame(frame: np.ndarray, message: str, row: int) -> np.ndarray:
        """Annotate the frame with text"""
        if message:
            cv2.putText(frame, message, (10, (30 + (row * 50))),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
        
        return frame