import whisper
import torch
import soundfile as sf
import numpy as np
import librosa

def speech_to_text(audio_data):
    try:
        # Check device availability
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")
        # Load whisper model
        model = whisper.load_model("base", device=device)
        # Read audio data from io.BytesIO object
        audio, sample_rate = sf.read(audio_data)
        # Resample to 16kHz if necessary
        if sample_rate != 16000:
            audio = librosa.resample(audio, orig_sr=sample_rate, target_sr=16000)
            sample_rate = 16000
        # Ensure audio is mono
        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)
        # Transcribe audio
        result = model.transcribe(audio, language="en")
        return result["text"]
    except Exception as e:
        print(f"Whisper Error: {str(e)}")
        raise