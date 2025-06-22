import os
import time
from queue import Queue, Empty
from typing import Dict, Optional, Callable
from threading import Thread, Event

import cv2
from cv2.typing import MatLike

from ocr.ocr import OCR
from tts.tts import TextToSpeech
from video.processor import VideoProcessor

from logs.logging_setup import setup_logger

###############################################################

class CommandScheduler:
    def __init__(self) -> None:
        file_name = os.path.splitext(os.path.basename(__file__))[0]
        self.logger = setup_logger(file_name)
        self.ocr = OCR()
        self.object_detection = VideoProcessor()
        self.tts = TextToSpeech()
        self.workers: Dict[str, Callable] = {
            "ocr": self.ocr_handler,
            "tts": self.speech_handler,
            "object_detection": self.object_detection_handler
        }
        self.cap = cv2.VideoCapture(0)

    def ocr_handler(self, stop_event: Event, speech_queue: Queue) -> None:
        while not stop_event.is_set():
            try:
                request: Optional[str] = self.ocr.read(self.get_frame())
            except Empty:
                pass
            except Exception as e:
                self.logger.error(f'An error occured with audio processing: {e}')

    def speech_handler(self, stop_event: Event, speech_queue: Queue) -> None:
        while not stop_event.is_set():
            try:
                request: Optional[str] = speech_queue.get(timeout=0.5)
                if request:
                    self.tts.speak(request)
            except Empty:
                pass
            except Exception as e:
                self.logger.error(f'An error occured with audio processing: {e}')

    def object_detection_handler(self, stop_event: Event, speech_queue: Queue) -> None:
        while not stop_event.is_set():
            try:
                frame = self.get_frame()
                if frame:
                    self.object_detection.process_video_feed(frame)
            except Empty:
                pass
            except Exception as e:
                self.logger.error(f'An error occured with audio processing: {e}')

    def get_frame(self) -> Optional[MatLike]:
        ret, frame = self.cap.read()
        if ret:
            return None
        return frame

    def mainloop(self) -> None:
        stop_event = Event()
        speech_queue: Queue = Queue()
        thread_manager = ThreadManager(self.workers, self.logger)
        
        thread_manager.start_all_threads(stop_event, speech_queue)

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

class ThreadManager:
    def __init__(self, worker_funcs: Dict[str, Callable], logger) -> None:
        self.logger = logger
        self.worker_funcs = worker_funcs
        self.threads: Dict[str, Thread] = {}
        self.stop_event: Optional[Event] = None

    def start_all_threads(self, stop_event: Event, speech_queue) -> None:
        self.stop_event = stop_event
        for name in ["ocr", "tts", "object_detection"]:
            self.start_thread(name, speech_queue)

    def close_all_threads(self) -> None:
        if self.stop_event:
            self.stop_event.set()

        for name, thread in self.threads.items():
            thread.join()
            self.logger.info(f"Thread '{name}' joined.")
        
        self.threads.clear()
        self.logger.info("All threads stopped.")

    def start_thread(self, name: str, speech_queue: Queue) -> None:
        if name in self.threads and self.threads[name].is_alive():
            self.logger.info(f"Thread '{name}' is already running.")
            return

        if self.stop_event is None:
            self.logger.error("Stop event not initialized.")
            return

        target = self.worker_funcs.get(name)
        if not target:
            self.logger.error(f"No such thread worker defined for: '{name}'")
            return

        thread = Thread(target=target, args=(self.stop_event, speech_queue), name=name)
        thread.start()
        self.threads[name] = thread
        self.logger.info(f"Thread '{name}' started.")

###############################################################

if __name__ == '__main__':
    cs = CommandScheduler()
    cs.mainloop()