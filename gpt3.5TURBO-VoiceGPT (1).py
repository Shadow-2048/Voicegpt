import openai
import pyttsx3
import speech_recognition as sr
import pyaudio
import time
import pygame

openai.api_key = "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"

engine = pyttsx3.init()
pygame.mixer.init()

api_endpoint = "https://api.openai.com/v1/chat/completions"

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print('Skipping Unknown error')

def generate_response(prompt):
    messages = [{'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': prompt}]
                
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages,
    max_tokens=1000,
    n=1,
    temperature=0.3,
)   
    return response['choices'][0]['message']['content']


def speak_text(text, rate=180):
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()


def main():
    while True:
        print("Say 'Activate' to ask your question")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "activate":
                    
                    pygame.mixer.music.load("ding.wav")
                    pygame.mixer.music.play()

                    filename = "input.wav"
                    print("say your question")
                    with sr.Microphone()as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())


                            text = transcribe_audio_to_text(filename)
                            if text:
                                print(f"You said: {text}")


                                response = generate_response(text)
                                print(f"GPT-3 Says: {response}")


                                speak_text(response)
            except Exception as e:
                print("An error occured: {}".format(e))

if __name__ == "__main__":
    main()