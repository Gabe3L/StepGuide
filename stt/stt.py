import os
import torch
import whisper
import numpy as np
from typing import Optional, Dict, cast

from logs.logging_setup import setup_logger
from speech_recognition import Recognizer, Microphone, UnknownValueError, AudioData

################################################################

class SpeechToText():
    def __init__(self) -> None:
        file_name = os.path.splitext(os.path.basename(__file__))[0]
        self.logger = setup_logger(file_name)

        self.recording = Recognizer()

        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = whisper.load_model("base").to(device)

    def process_audio(self) -> Optional[str]:
        try:
            request = self.get_request()
            if request:
                self.logger.info(f"Whisper Heard: {request}")
                return request
        except UnknownValueError:
            self.logger.error("Audio could not be understood.")
        except Exception as e:
            self.logger.error(f"Error in processing audio: {e}")
        
        return None

    def get_request(self) -> Optional[str]:
        try:
            audio_data = self.capture_audio()
            if audio_data is not None:
                result = self.transcribe_audio(audio_data)
                if result:
                    return result
        except Exception as e:
            self.logger.error(f"Error while getting request: {e}")
        
        return None

    def capture_audio(self) -> Optional[np.ndarray]:
        try:
            with Microphone(sample_rate=16000) as mic:
                self.recording.adjust_for_ambient_noise(mic, duration=1)
                audio = self.recording.listen(mic)

            audio = cast(AudioData, audio)
            audio_data = np.frombuffer(audio.get_wav_data(), dtype=np.int16)
            audio_data = audio_data.astype(np.float32) / 32768.0
            return audio_data
        except Exception as e:
            self.logger.error(f"Error capturing audio: {e}")
            return None

    def transcribe_audio(self, audio_data: np.ndarray) -> Optional[str]:
        try:
            result = cast(Dict[str, str], self.model.transcribe(audio_data))
            text = result["text"].lower()
            
            if text.strip():
                return self.clean_transcription(text)
            else:
                self.logger.warning("Empty transcription result.")
                return None
        except Exception as e:
            self.logger.error(f"Error transcribing audio: {e}")
            return None
        
    def clean_transcription(self, text: str) -> str:
        unwanted_words = ["um", "uh", "urm"]
        for word in unwanted_words:
            text = text.replace(word, "")
        return text.strip()