import speech_recognition as sr
from pydub import AudioSegment
import text_to_speech as converter
from pydub.utils import mediainfo
import os
AudioSegment.converter = "C:/ffmpeg/bin/ffmpeg.exe"  # Replace with your actual ffmpeg path
AudioSegment.ffprobe = "C:/ffmpeg/bin/ffprobe.exe"  # Replace with your actual ffprobe path

def convert_audio_to_wav(input_file, output_file="converted_audio.wav"):
    """
    Converts an audio file to WAV format using pydub.
    """
    try:
        # Convert to WAV format
        sound = AudioSegment.from_file(input_file)
        sound.export(output_file, format="wav")
        print(f"File converted to {output_file}")
        return output_file
    except Exception as e:
        print(f"Error during audio conversion: {e}")
        return None

def audio_to_text(audio_file):
    """
    Converts audio to text using speech_recognition.
    """
    recognizer = sr.Recognizer()

    try:
        # Load the audio file
        with sr.AudioFile(audio_file) as source:
            print("Listening to the audio...")
            audio_data = recognizer.record(source)
            
        # Recognize speech using Google Web Speech API
        print("Converting audio to text...")
        text = recognizer.recognize_google(audio_data)
        return text

    except sr.UnknownValueError:
        return "Audio was unclear. Could not understand."
    except sr.RequestError as e:
        return f"Could not request results from Google API; {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# Main function
if __name__ == "__main__":
    current_path = os.getcwd()
    print(os.environ["PATH"])
    os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"  # Replace with your actual path
    print(f"Current working directory: {current_path}")
    input_audio_file = "sample.mp3"  # Specify your file name here
    try:
        # Step 1: Convert audio to WAV format (if necessary)
        wav_file = convert_audio_to_wav(input_audio_file)
        
        if not wav_file:
            raise ValueError("Failed to convert audio file.")
        
        # Step 2: Convert WAV audio to text
        transcription = audio_to_text(wav_file)
        print("Transcription:", transcription)
    except Exception as e:
        print(f"Error: {e}")
