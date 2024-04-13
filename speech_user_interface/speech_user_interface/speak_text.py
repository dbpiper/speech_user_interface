from gtts import gTTS
import pygame


def speak_text(text):
    # Create an audio file from the text
    tts = gTTS(text, lang="en")
    filename = "temp_audio.mp3"
    tts.save(filename)

    # Initialize pygame mixer
    pygame.mixer.init()

    # Load the sound file
    sound = pygame.mixer.Sound(filename)

    # Play the sound
    sound.play()

    # Keep the script running until the audio has finished playing
    while pygame.mixer.get_busy():
        pygame.time.Clock().tick(10)
