import pyttsx3
from gtts import gTTS
from io import BytesIO
from pydantic import BaseModel
import tempfile
def text_to_speech(text, voice=1):
    # Initialize the TTS engine
    engine = pyttsx3.init()
    
    # Initialize gTTS with the selected language
    language = 'en'  # English language
    tts = gTTS(text=text, lang=language, slow=False)
    
    # Set properties (optional)
    # Set rate (speed of speech)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 50)  # Reduce speed for clarity
    
    # Set voice
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice].id)  # Select male or female voice
    
    # Speak the text
    engine.say(text)
    engine.runAndWait()
class TextInput(BaseModel):
    text: str
    voice: int = 1  # Default to female voice (1), male voice (0) can be set

def text_to_speech2(text: str, voice: int = 1) -> BytesIO:
    """
    Convert the given text to speech and return an MP3 file in a BytesIO object.
    :param text: The text to convert to speech.
    :param voice: Select the voice (0 for male, 1 for female).
    :return: BytesIO object containing the MP3 audio file.
    """
    language = 'en'  # English language
    tts = gTTS(text=text, lang=language, slow=False)
    print("done")
    # Create a temporary file to save the MP3
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_file_name = tmp_file.name  # Get the temporary file path
        
        # Save the speech to the temporary file
        tts.save(tmp_file_name)
        
        # Read the saved MP3 file into a BytesIO object
        with open(tmp_file_name, 'rb') as f:
            mp3_file = BytesIO(f.read())
    
    # You can safely remove the temporary file now
    # os.remove(tmp_file_name)  # Uncomment if you want to delete the temp file
    print("done")    
    # Return the mp3 file in memory as BytesIO
    mp3_file.seek(0)  # Reset the BytesIO stream position
    return mp3_file
    
# Test the function
if __name__ == "__main__":
    user_input = input("Enter text to convert to speech: ")
    text_to_speech2(user_input)