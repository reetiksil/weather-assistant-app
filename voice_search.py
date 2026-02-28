import speech_recognition as sr #type: ignore

# Create recognizer object
recognizer = sr.Recognizer()

# Use microphone as source
with sr.Microphone() as source:
    print("Listening... Speak now.")
    
    # Adjust for background noise
    recognizer.adjust_for_ambient_noise(source)
    
    # Capture audio
    audio = recognizer.listen(source)

try:
    # Convert speech to text
    text = recognizer.recognize_google(audio)
    print("You said:", text)

except sr.UnknownValueError:
    print("Sorry, could not understand audio.")

except sr.RequestError:
    print("Could not request results from Google service.")