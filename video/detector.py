import os
import numpy as np
from typing import Tuple, List

import torch
from ultralytics import YOLO

from logs.logging_setup import setup_logger

###############################################################

CONFIDENCE_THRESHOLD: float = 0.5

###############################################################

class YOLODetector:
    def __init__(self) -> None:
        file_name = os.path.splitext(os.path.basename(__file__))[0]
        self.logger = setup_logger(file_name)
        self.device: torch.device = torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu')
        self.model: YOLO = YOLO("video/weights/yolo11n.onnx", task='detect')
        self.logger.info("Loaded CV model.")

    def detect(self, frame: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        with torch.no_grad():
            results = self.model.predict(frame)[0]
        return self.extract_detections(results)

    def extract_detections(self, results) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        boxes: List[List[int]] = []
        confidences: List[float] = []
        class_ids: List[int] = []

        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
            confidence: float = float(box.conf[0])

            if confidence >= CONFIDENCE_THRESHOLD:
                boxes.append([x1, y1, x2, y2])
                confidences.append(confidence)
                class_ids.append(int(box.cls[0]))

        return np.array(boxes), np.array(confidences), np.array(class_ids)