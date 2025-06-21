import cv2
import easyocr
import platform
import sys
import time


class RealTimeEasyOCR:
    def __init__(self):
        self.lang = ['en']
        self.cap = None
        self.reader = easyocr.Reader(self.lang, gpu=False, mps=True)

    def initialize_camera(self):
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            raise RuntimeError("Unable to open webcam.")

        self.cap.set(640, self.frame_width)
        self.cap.set(480, self.frame_height)

    def run(self):
        print("Press [SPACE] to scan. Press [Q] to quit.")
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame.")
                break


            text = self.perform_ocr(frame)
            if text.strip():
                print("\n[ OCR Result ]")
                print(text.strip())
                print("----------------------")
                
            cv2.imshow("Webcam Feed", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cleanup()

    def perform_ocr(self, frame):
        results = self.reader.readtext(frame)
        return "\n".join([text for _, text, conf in results if conf > 0.4])

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
