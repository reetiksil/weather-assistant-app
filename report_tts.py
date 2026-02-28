import edge_tts # type: ignore
import asyncio
import pygame # type: ignore
import time
import os

VOICE = "en-US-AriaNeural"  # Change voice here if needed

async def generate_speech(text, filename="speech.mp3"):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(filename)

def play_audio(filename="speech.mp3"):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    # Wait until audio finishes playing
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    pygame.mixer.quit()

async def main():
    text = input("Enter text: ").strip()

    if not text:
        print("No text provided.")
        return

    filename = "speech.mp3"

    await generate_speech(text, filename)
    play_audio(filename)

    # Optional: delete file after playing
    if os.path.exists(filename):
        os.remove(filename)

if __name__ == "__main__":
    asyncio.run(main())
    