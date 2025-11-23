import speech_recognition as sr
import pyttsx3

class VoiceInterface:
    def __init__(self):
        self.r = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 175)
        self.r.pause_threshold = 2.5  
        self.r.energy_threshold = 300     

    def listen(self, max_seconds=80):
        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source, duration=0.8)
            print("Listening... (up to", max_seconds, "seconds)")
            audio = self.r.listen(source, phrase_time_limit=max_seconds)

        try:
            text = self.r.recognize_google(audio)
        except Exception as e:
            print("STT error:", e)
            text = ""
        return text

    def speak(self, text: str):
        if not text:
            return
        self.engine.say(text)
        self.engine.runAndWait()
