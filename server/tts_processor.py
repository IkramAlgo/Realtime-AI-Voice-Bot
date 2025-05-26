import pyttsx3
import base64

def text_to_speech(text):
    try:
        engine = pyttsx3.init()
        temp_file = "temp_audio.mp3"
        engine.save_to_file(text, temp_file)
        engine.runAndWait()
        with open(temp_file, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except Exception as e:
        print(f"TTS Error: {str(e)}")
        raise