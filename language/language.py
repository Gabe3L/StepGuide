from typing import Tuple, List
from queue import Queue

from ocr_to_text import OCR
from object_to_text import ObjectToText

class Language:
    def __init__(self) -> None:
        self.detector = ObjectToText() 
        self.reader = OCR()

    def process_object(self, class_id: str, bbox: List[int], speech_queue: Queue) -> None:
        object_text = self.detector.get_text(class_id, bbox)
        if object_text:
            speech_queue.put(object_text)

    def process_ocr(self, text: str, speech_queue: Queue) -> None:
        ocr_text = self.reader.read(text)
        if ocr_text:
            speech_queue.put(ocr_text)