import os
import asyncio
from queue import Queue, Empty
from typing import Dict, Optional
from threading import Thread, Event

from tts.tts import TextToSpeech
from video.processor import VideoProcessor

from logs.logging_setup import setup_logger

###############################################################

class CommandScheduler:
    def __init__(self) -> None:
        file_name = os.path.splitext(os.path.basename(__file__))[0]
        self.logger = setup_logger(file_name)
        self.camera = VideoProcessor()
        self.tts = TextToSpeech()

    async def speech_handler(self, stop_event: Event, speech_queue: Queue) -> None:
        while not stop_event.is_set():
            try:
                request: Optional[str] = speech_queue.get(timeout=0.5)
                if request:
                    self.tts.speak(request)
            except Empty:
                pass
            except Exception as e:
                self.logger.error(f'An error occured with audio processing: {e}')

    async def camera_handler(self, stop_event: Event, speech_queue: Queue) -> None:
        cap = self.camera.get_video_feed()
        if not cap or cap.isOpened():
            return

        while not stop_event.is_set():
            try:
                self.camera.process_video_feed(cap)
            except Empty:
                pass
            except Exception as e:
                self.logger.error(f'An error occured with audio processing: {e}')
                
    def get_worker(self, name: str):
        return {
            "text_to_speech": self.speech_handler,
            "camera": self.camera_handler
        }.get(name, None)
    
    def _run_async_worker(self, coro_func, stop_event: Event, speech_queue: Queue) -> None:
        try:
            asyncio.run(coro_func(stop_event, speech_queue))
        except Exception as e:
            self.logger.error(f'Async worker failed: {e}')

    def mainloop(self) -> None:
        try:
            stop_event = Event()
            speech_queue: Queue = Queue()
            thread_manager = ThreadManager(self)
            def start_thread(name: str, speech_queue: Queue):
                if name in thread_manager.threads and thread_manager.threads[name].is_alive():
                    self.logger.info(f"Thread '{name}' is already running.")
                    return

                if thread_manager.stop_event is None:
                    self.logger.error("Stop event not initialized.")
                    return

                target = self.get_worker(name)
                if not target:
                    self.logger.error(f"No such thread worker defined for: '{name}'")
                    return

                thread = Thread(
                    target=self._run_async_worker,
                    args=(target, stop_event, speech_queue),
                    name=name
                )
                thread.start()
                thread_manager.threads[name] = thread
                self.logger.info(f"Thread '{name}' started.")

            thread_manager.start_thread = start_thread
            thread_manager.start_all_threads(stop_event, speech_queue)

            self.logger.info("System running. Press Ctrl+C to stop.")
            while not stop_event.is_set():
                try:
                    ...
                except KeyboardInterrupt:
                    self.logger.info("Shutdown signal received.")
                    stop_event.set()
                    break
                except Exception as e:
                    self.logger.error(f"Unhandled exception in main loop: {e}")
                    stop_event.set()
                    break

            thread_manager.close_all_threads()

        except Exception as e:
            self.logger.error(f'Exception in mainloop: {e}')       

class ThreadManager:
    def __init__(self, command_scheduler: CommandScheduler) -> None:
        self.command_scheduler = command_scheduler
        self.logger = self.command_scheduler.logger
        self.threads: Dict[str, Thread] = {}
        self.stop_event: Optional[Event] = None

    def start_all_threads(self, stop_event: Event, speech_queue):
        self.stop_event = stop_event
        for name in ["text_to_speech", "camera"]:
            self.start_thread(name, speech_queue)

    def close_all_threads(self):
        if self.stop_event:
            self.stop_event.set()

        for name, thread in self.threads.items():
            thread.join()
            self.logger.info(f"Thread '{name}' joined.")
        
        self.threads.clear()
        self.logger.info("All threads stopped.")

    def start_thread(self, name: str, speech_queue: Queue):
        if name in self.threads and self.threads[name].is_alive():
            self.logger.info(f"Thread '{name}' is already running.")
            return

        if self.stop_event is None:
            self.logger.error("Stop event not initialized.")
            return

        target = self.command_scheduler.get_worker(name)
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