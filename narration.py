import os
import requests

# import elevenlabs
import openai
from gtts import gTTS


elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")


narration_api = "elevenlabs"  # (or "openai")


def parse(narration):
    data = []
    narrations = []
    lines = narration.split("\n")
    for line in lines:
        if line.startswith("Narrator: "):
            text = line.replace("Narrator: ", "")
            data.append(
                {
                    "type": "text",
                    "content": text.strip('"'),
                }
            )
            narrations.append(text.strip('"'))
        elif line.startswith("["):
            background = line.strip("[]")
            data.append(
                {
                    "type": "image",
                    "description": background,
                }
            )
    return data, narrations


import os
import pyttsx3


def create(data, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    n = 0
    engine = pyttsx3.init()
    for element in data:
        if element["type"] != "text":
            continue

        n += 1
        output_file = os.path.join(output_folder, f"narration_{n}.mp3")

        # Use pyttsx3 for text-to-speech
        engine.save_to_file(element["content"], output_file)
        engine.runAndWait()


"""
# Example usage
data = [{"type": "text", "content": "Hello, how are you iam kumki what is your name"}]
output_folder = "output"
create(data, output_folder)
"""
