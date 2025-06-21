import os
import time
import logging
import numpy as np

logging.getLogger("torch.distributed.elastic.multiprocessing.redirects").setLevel(
    logging.ERROR
)

import torch
from TTS.api import TTS
import sounddevice as sd

from logs.logging_setup import setup_logger

################################################################


class TextToSpeech:
    def __init__(self):
        file_name = os.path.splitext(os.path.basename(__file__))[0]
        self.logger = setup_logger(file_name)
        self.logger.info("TTS Logger is setup!")

        device = "cuda" if torch.cuda.is_available() else "cpu"

        self.tts = TTS(
            model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=True
        ).to(device)

    def speak(self, text):
        try:
            if not text.strip().endswith((".", "?", "!")):
                text += "."

            waveform_list = self.tts.tts(text)
            waveform = np.array(waveform_list, dtype=np.float32)
            sample_rate = 22050

            self.play_audio(waveform, sample_rate)
        except Exception as e:
            self.logger.error(f"Speech synthesis failed: {e}")

    def play_audio(self, waveform, sample_rate):
        try:
            sd.play(waveform, samplerate=sample_rate)
            sd.wait()
        except Exception as e:
            self.logger.error(f"Audio playback failed: {e}")


################################################################


if __name__ == "__main__":
    text_to_speech = TextToSpeech()
    text_to_speech.speak("The step guide service has initialized!")
