import cv2
import pytesseract
import time
import sys
import platform
from PIL import Image


class WebcamOCR:
    def __init__(self, camera_index=0, frame_width=640, frame_height=480):
        self.camera_index = camera_index
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.cap = None
        self._print_system_info()

    def _print_system_info(self):
        print(f"OpenCV version: {cv2.__version__}")
        print(f"Python version: {sys.version}")
        print(f"Operating System: {platform.system()} {platform.release()}")

    def _get_camera_backend(self):
        return cv2.CAP_AVFOUNDATION if platform.system() == 'Darwin' else 0

    def initialize_camera(self):
        print("Initializing camera...")
        backend = self._get_camera_backend()
        self.cap = cv2.VideoCapture(self.camera_index, backend)

        if not self.cap.isOpened():
            for i in range(1, 3):
                print(f"Trying camera index {i}...")
                self.cap = cv2.VideoCapture(i, backend)
                if self.cap.isOpened():
                    print(f"Successfully opened camera index {i}")
                    break
            else:
                raise RuntimeError("Could not open any webcam.")

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
        time.sleep(2)  # Let camera warm up

    def capture_loop(self):
        print("Press [SPACE] for OCR. Press [Q] to quit.")
        fail_count = 0

        while True:
            ret, frame = self.cap.read()
            if not ret:
                fail_count += 1
                print(f"Failed to grab frame ({fail_count}/5)")
                if fail_count >= 5:
                    print("Multiple failures. Exiting.")
                    break
                time.sleep(0.5)
                continue

            fail_count = 0
            cv2.imshow('Webcam OCR - Press SPACE', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord(' '):  # SPACE key for OCR
                text = self.perform_ocr(frame)
                print("\n--- OCR Result ---")
                print(text.strip())
                print("------------------")

        self.cleanup()

    def perform_ocr(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb)
        return pytesseract.image_to_string(pil_img, lang='eng')

    def cleanup(self):
        print("Cleaning up resources.")
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    try:
        ocr_app = WebcamOCR()
        ocr_app.initialize_camera()
        ocr_app.capture_loop()
    except Exception as e:
        print(f"Fatal error: {e}")
        if hasattr(ocr_app, 'cleanup'):
            ocr_app.cleanup()
