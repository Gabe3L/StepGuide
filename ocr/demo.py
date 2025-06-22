import cv2
from ocr.ocr import OCR

if __name__ == "__main__":
    try:
        ocr = OCR()
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise RuntimeError("Failed to open camera.")
    
        while True:
            ret, frame = cap.read()

            if not ret:
                raise RuntimeError("Failed to capture frame from camera.")
            
            results = ocr.read(frame)
            if results:
                print(f'\n\n{results}')
    except Exception as e:
        print(f"Error: {e}")