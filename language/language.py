from typing import Tuple

from ocr_to_text import Ocr
from object_to_text import ObjectToText

class Language:
    def __init__(self, q) -> None:
        self.queue = q
        self.detector = ObjectToText() 
        self.reader   = Ocr()

    def process(
        self,
        object_args: Tuple[str, int, int, int, int, float],
        ocr_args: Tuple[str, bool]
    ) -> None:
        """
        Detect object → put text on queue,
        Read OCR → put text on queue.
        Nothing is returned.
        """
        object_text = self.detector.detect(*object_args)
        self.queue.put(object_text)

        ocr_text = self.reader.read(*ocr_args)
        self.queue.put(ocr_text)
