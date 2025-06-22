from typing import Tuple
from queue import Queue

from ocr_to_text import OCR
from object_to_text import ObjectToText

class Language:
    def __init__(self, speech_queue: Queue) -> None:
        self.speech_queue = speech_queue
        self.detector = ObjectToText() 
        self.reader = OCR()

    def process(
        self,
        object_args: Tuple[str, int, int, int, int, float],
        ocr_args: Tuple[str, bool]
    ) -> None:
        object_text = self.detector.detect(*object_args)
        if object_text:
            self.speech_queue.put(object_text)

        ocr_text = self.reader.read(*ocr_args)
        if ocr_text:
            self.speech_queue.put(ocr_text)
