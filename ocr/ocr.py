import os
import cv2
import warnings

warnings.filterwarnings(
    "ignore", message="Using CPU. Note: This module is much faster with a GPU."
)

import easyocr

from logs.logging_setup import setup_logger

########################################################################################


class OCR:
    def __init__(self):
        file_name = os.path.splitext(os.path.basename(__file__))[0]
        self.logger = setup_logger(file_name)
        self.lang = ["en"]
        try:
            self.reader = easyocr.Reader(self.lang, gpu=True)
        except Exception as e:
            self.reader = easyocr.Reader(self.lang, gpu=False)
        self.logger.info("Loaded model")

    def read(self, frame):
        text = self.perform_ocr(frame)
        if text:
            self.logger.info(f'OCR Reads: {text.strip()}')
            return text.strip()

    def perform_ocr(self, frame):
        results = self.reader.readtext(frame)
        return "\n".join([text for _, text, conf in results if float(conf) > 0.4])