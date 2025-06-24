from queue import Queue
from stt.stt import SpeechToText

################################################################

if __name__ == "__main__":
    speech_queue = Queue()
    stt = SpeechToText()
    print("Started.")
    while True:
        result = stt.process_audio()
        if result:
            print(result)