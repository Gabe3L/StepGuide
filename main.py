import os
import time
from queue import Queue, Empty
from typing import Dict, Optional, Callable
from threading import Event

import cv2
from cv2.typing import MatLike

from ocr.ocr import OCR
from tts.tts import TextToSpeech
from stt.stt import SpeechToText
from hands.hands import HandTracker
from language.language import Language
from video.processor import VideoProcessor
from thread_manager import ThreadManager

from logs.logging_setup import setup_logger

###############################################################


class CommandScheduler:
    def __init__(self) -> None:
        file_name = os.path.splitext(os.path.basename(__file__))[0]
        self.logger = setup_logger(file_name)

        self.ocr = OCR()
        self.tts = TextToSpeech()
        self.stt = SpeechToText()
        self.language = Language()
        self.hand_tracker = HandTracker()
        self.object_detection = VideoProcessor()

        self.frame_queue = Queue(maxsize=1)
        self.ocr_raw_queue = Queue(maxsize=3)
        self.detection_raw_queue = Queue(maxsize=3)
        self.humanization_queue = Queue(maxsize=3)
        self.speech_queue = Queue(maxsize=3)

        self.workers: Dict[str, Callable] = {
            "frame_capture": self.frame_capture,
            "ocr": self.ocr_handler,
            "tts": self.tts_handler,
            "stt": self.stt_handler,
            "humanizer": self.humanizer_handler,
            "object_detection": self.object_detection_handler
        }
        self.cap = cv2.VideoCapture(0)

    def hand_handler(self, stop_event: Event) -> None:
        while not stop_event.is_set():
            try:
                frame = self.frame_queue.get(timeout=0.5)
                if frame is not None:
                    self.hand_tracker.process_frame(frame)
            except Exception as e:
                print(f"Error: {e}")

    def ocr_handler(self, stop_event: Event) -> None:
        while not stop_event.is_set():
            try:
                frame = self.frame_queue.get(timeout=0.5)
                if frame is not None:
                    text = self.ocr.read(frame)
                    if text:
                        self.ocr_raw_queue.put(text)
            except Empty:
                pass
            except Exception as e:
                self.logger.error(f'An error occured with ocr processing: {e}')

    def humanizer_handler(self, stop_event: Event) -> None:
        while not stop_event.is_set():
            try:
                try:
                    class_id, bbox = self.detection_raw_queue.get_nowait()
                    description = self.language.process_object(
                        class_id, bbox, self.speech_queue)
                    if description:
                        self.humanization_queue.put(description)
                except Empty:
                    pass

                try:
                    text = self.ocr_raw_queue.get_nowait()
                    description = self.language.process_ocr(
                        text, self.speech_queue)
                    if description:
                        self.humanization_queue.put(description)
                except Empty:
                    pass

                try:
                    human_text = self.humanization_queue.get_nowait()
                    self.speech_queue.put(human_text)
                except Empty:
                    pass

                time.sleep(0.01)
            except Exception as e:
                self.logger.error(f"Error in humanizer: {e}")

    def stt_handler(self, stop_event: Event) -> None:
        while not stop_event.is_set():
            try:
                text = self.stt.process_audio()
                if text:
                    if "laptop" in text.lower():
                        self.laptop_mode = True
                        self.tts.speak("Navigating to your laptop.")
            except Empty:
                pass
            except Exception as e:
                self.logger.error(f'An error occured with stt processing: {e}')

    def tts_handler(self, stop_event: Event) -> None:
        while not stop_event.is_set():
            try:
                text = self.speech_queue.get(timeout=0.5)

                if text:
                    self.logger.info(f"Speaking text: {text}")
                    self.tts.speak(text)
            except Empty:
                pass
            except Exception as e:
                self.logger.error(f'An error occured with tts processing: {e}')

    def object_detection_handler(self, stop_event: Event) -> None:
        while not stop_event.is_set():
            try:
                frame = self.frame_queue.get(timeout=0.5)
                if frame is not None:
                    self.object_detection.process_frame(frame)
            except Empty:
                pass
            except Exception as e:
                self.logger.error(
                    f'An error occured with object detection handling processing: {e}')

    def frame_capture(self, stop_event: Event) -> None:
        while not stop_event.is_set():
            frame = self.get_frame()
            if frame is not None:
                if self.frame_queue.qsize() < 2:
                    self.frame_queue.put(frame)
            time.sleep(0.01)

    def get_frame(self) -> Optional[MatLike]:
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def mainloop(self) -> None:
        stop_event = Event()
        thread_manager = ThreadManager(self.workers, self.logger)
        thread_manager.start_all_threads(stop_event)

        self.logger.info("System running. Press Ctrl+C to stop.")
        try:
            while not stop_event.is_set():
                time.sleep(0.01)
        except KeyboardInterrupt:
            self.logger.info("Shutdown signal received.")
            stop_event.set()
        except Exception as e:
            self.logger.error(f"Unhandled exception in main loop: {e}")
            stop_event.set()

        thread_manager.close_all_threads()

###############################################################


if __name__ == '__main__':
    cs = CommandScheduler()
    cs.mainloop()
