from tts.tts import TextToSpeech

if __name__ == "__main__":
    text_to_speech = TextToSpeech()
    print("Speaking")
    text_to_speech.speak("The step guide service has initialized!")
    print("Done Speaking")