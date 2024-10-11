import speech_recognition as sr
import subprocess
import os

def convert_to_wav(input_file_path: str, output_file_path: str):
    command = [
        "ffmpeg", "-i", input_file_path, output_file_path
    ]
    subprocess.run(command, check=True)

def process_audio(audio_file_path: str):
    wav_file_path = f"{audio_file_path}.wav"
    
    convert_to_wav(audio_file_path, wav_file_path)

    recognizer = sr.Recognizer()

    with sr.AudioFile(wav_file_path) as source:
        audio = recognizer.record(source) 
    text = recognizer.recognize_google(audio, language="uk-UA")

    os.remove(wav_file_path)

    return text
    


