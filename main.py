from tts.tts import TextToSpeech
from video.processor import VideoProcessor

from typing import Dict

###############################################################

class CommandScheduler:
    def __init__(self) -> None:
        pass

    def mainloop(self) -> None:
        ...

###############################################################

if __name__ == '__main__':
    cs = CommandScheduler()
    cs.mainloop()