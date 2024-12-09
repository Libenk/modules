from pydantic import BaseModel
from fastapi import FastAPI, HTTPException ,UploadFile
from fastapi.responses import StreamingResponse
from io import BytesIO
import tempfile
import audio_to_text as converteraudio
from gtts import gTTS
import speech_recognition as sr
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import shutil
import os
import speech_recognition as sr
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
# Create the FastAPI app
app = FastAPI()
recognizer = sr.Recognizer()
# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow only localhost:3000
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Pydantic model to handle input data for text-to-speech conversion
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
    
    # Return the mp3 file in memory as BytesIO
    mp3_file.seek(0)  # Reset the BytesIO stream position
    return mp3_file

@app.post("/text-to-audio/")
async def text_to_audio(input: TextInput):
    """
    Endpoint to convert text to speech and return the audio as MP3 for download.
    :param input: Input data (text and voice).
    :return: MP3 file to be downloaded and played by the client.
    """
    print(f"Received text: {input.text}, voice: {input.voice}")  # Debug: Log received data
    try:
        # Generate the MP3 audio file
        
        audio_file = text_to_speech2(input.text, input.voice)
        
        # Return the MP3 file with a Content-Disposition header to trigger a download
        return StreamingResponse(
            audio_file,
            media_type="audio/mp3",
            headers={"Content-Disposition": "attachment; filename=output.mp3"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint to convert MP3 to text
@app.post("/audio-to-text/")
async def audio_to_text(file: UploadFile = File(...)):
    
    
    try:
        # Save the uploaded MP3 file temporarily
        file_location = f"./temp_{file.filename}"
        print(file_location)
        wav_file = converteraudio.convert_audio_to_wav(file_location)
        text = converteraudio.audio_to_text(wav_file)
        print("Transcription:", text)
        return JSONResponse(content={"transcription": text})        
    except sr.RequestError:
        return JSONResponse(content={"error": "Could not request results from Google Speech Recognition service."}, status_code=500)
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)