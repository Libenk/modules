import pyttsx3

def text_to_speech(text):
    # Initialize the TTS engine
    engine = pyttsx3.init()
    
    # Set properties (optional)
    # Set rate (speed of speech)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 50)  # Reduce speed for clarity
    
    # Set voice
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Select male or female voice
    
    # Speak the text
    engine.say(text)
    engine.runAndWait()

# Test the function
if __name__ == "__main__":
    user_input = input("Enter text to convert to speech: ")
    text_to_speech(user_input)