import speech_recognition as spr
from googletrans import Translator

import requests
from PIL import Image
from io import BytesIO


recog1 = spr.Recognizer()


mc = spr.Microphone()


translator = Translator()

def recognize_speech():
    with mc as source:
        print("Speak something...")
        print("Otherwise speak EXIT to end the program")
        recog1.adjust_for_ambient_noise(source, duration=0.2)
        audio = recog1.listen(source)
        
        try:
            text = recog1.recognize_google(audio)
            return text.lower()
        except spr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
            return ""
        except spr.RequestError:
            print("Sorry, could not request results. Check your internet connection.")
            return ""

def translate_to_english(text):
    translated_text = translator.translate(text, src='auto', dest='en').text
    return translated_text

def generator(prompt, save_path="./", authorization_token="ENTER YOUR HUGGING FACE TOKEN"):
    if authorization_token !=None and len(prompt)>=5:
        API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
        b = requests.post(API_URL,
                        headers = {"Authorization": f"Bearer {authorization_token}"},
                        json={"inputs":str(prompt)})

        i = Image.open(BytesIO(b.content))
        i.save(f"{save_path}"+"image.png")

def main():
    while True:
        user_input = recognize_speech()
        
        if user_input == "exit":
            print("Exiting the program...")
            break
        
        print("You said (in English):", user_input)
        
        translated_text = translate_to_english(user_input)
        print("Translated to English:", translated_text)

        generator(translated_text)

        continue



if __name__ == "__main__":
    main()
