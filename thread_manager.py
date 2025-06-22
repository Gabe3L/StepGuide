from typing import Dict, Callable, Optional
from threading import Event, Thread
from queue import Queue

class ThreadManager:
    def __init__(self, worker_funcs: Dict[str, Callable], logger) -> None:
        self.logger = logger
        self.worker_funcs = worker_funcs
        self.threads: Dict[str, Thread] = {}
        self.stop_event: Optional[Event] = None

    def start_all_threads(self, stop_event: Event, speech_queue) -> None:
        self.stop_event = stop_event
        for name in self.worker_funcs.keys():
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