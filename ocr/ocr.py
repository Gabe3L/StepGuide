import os
import cv2
import easyocr

from logs.logging_setup import setup_logger

class OCR:
    def __init__(self):
        file_name = os.path.splitext(os.path.basename(__file__))[0]
        self.logger = setup_logger(file_name)
        self.lang = ['en']
        self.cap: cv2.VideoCapture = cv2.VideoCapture(0)
        self.reader = easyocr.Reader(self.lang, gpu=False)

    def initialize_camera(self):
        if not self.cap.isOpened():
            raise RuntimeError("Unable to open webcam.")

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame.")
                break


            text = self.perform_ocr(frame)
            if text:
                print(text.strip())

        self.cleanup()

    def perform_ocr(self, frame):
        results = self.reader.readtext(frame)
        return "\n".join([text for _, text, conf in results if float(conf) > 0.4])

    def cleanup(self):
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()



if __name__ == "__main__":
    try:
        ocr = OCR()
        ocr.initialize_camera()
        ocr.run()
    except Exception as e:
        print(f"Error: {e}")
