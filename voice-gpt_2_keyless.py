##First and foremost, please ensure you have the required libraries installed. You can do this via pip:
##```bashpip install openai pydub speechrecognition sounddevice
##``` (we also need homebrew for ffmpeg, which pydub relies on for audio processing. You can install it with `brew install ffmpeg` on macOS).
#Then we import the necessary libraries and set up our OpenAI client. Make sure to replace the API key with your actual key.

import os
import io
import wave
import sounddevice as sd
from openai import OpenAI
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr

#Be sure to add credit to your openai key and setup your own key.
client = OpenAI(api_key="YOUR_OPENAI_KEY")

#we use the `ask_gpt` function to send a prompt and an instruction to the GPT model. 
# The instruction helps guide the model's response, while the prompt is the user's input that we want a response to. 
#The function returns the content of the response or an error message if something goes wrong.
#The function defines roles for the system and user, which helps the model understand the context of the conversation.
#The system role is used to provide instructions or context to the model, while the user role is used for the actual input from the user.
def ask_gpt(prompt, instruction):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": instruction},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error connecting to GPT: {e}"


#The `record_wav` function uses the `sounddevice` library to record audio from the microphone. 
#It records for a specified duration and saves the audio as a WAV file. The audio is recorded in int16 format for compatibility with the wave module. 
#Files are saved with a sample rate of 16000 Hz, which is a common sample rate for speech recognition tasks. duration is set to 5 seconds by default, but you can adjust it as needed.
def record_wav(filename="input.wav", duration=5, samplerate=16000):
    print("\nListening...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype="int16")
    sd.wait()
    
    #This saves the recorded audio to a WAV file using the wave module. It sets the number of channels, sample width, and frame rate according to the specifications used during recording.
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(audio.tobytes())

#the `transcribe_audio` function uses the `speech_recognition` library to transcribe the recorded audio. It loads the audio file and attempts to recognize the speech using Google's Web Speech API.
#If the audio is not clear or if there is an issue with the API, it handles exceptions and returns None, allowing the main loop to continue without prompting GPT with an error message.
#the try-except blocks handle specific exceptions related to speech recognition, such as `UnknownValueError` when the audio cannot be understood and `RequestError` when there is an issue with the API.
def transcribe_audio(filename="input.wav"):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return None # Return None so we don't prompt GPT with an error
    except sr.RequestError:
        print("API Unavailable")
        return None

#the speak_text function uses the OpenAI API to convert text to speech. It sends a request to the TTS model with the specified voice and input text. The response is streamed into a buffer, which is then processed using pydub to play the audio.
#The function also includes error handling to catch any issues that may arise during the text-to-speech conversion process, printing an error message if something goes wrong.  
#we use the `AudioSegment` class from pydub to read the audio data from the buffer and play it using the `play` function. The audio is expected to be in MP3 format, as specified in the `from_file` method.
#The `model` parameter specifies the TTS model to use, and the `voice` parameter specifies the voice to use for the speech synthesis. 
# You can customize these parameters based on your preferences and the available options in the OpenAI API.
#try except block is used to catch any exceptions that may occur during the text-to-speech conversion process, ensuring that the program does not crash and provides feedback on what went wrong.
def speak_text(text):
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text
        )
        # Stream the response content into a buffer
        audio_data = io.BytesIO(response.content)
        audio = AudioSegment.from_file(audio_data, format="mp3")
        play(audio)
    except Exception as e:
        print(f"Speech Error: {e}")

#This is the setup for the main loop of the program. It prompts the user to specify the role of the assistant, which is used to provide context to the GPT model. 
# The loop continuously listens for user input, transcribes it, and generates a response from GPT, which is then spoken back to the user. The loop can be exited by saying "exit", "quit", or "stop".
user_role = input("What should the assistant's role be? \n> ").strip()
dev_instruction = f"You are a helpful assistant. Role: {user_role}. Be concise."

#the print statement indicates that the system is ready to receive voice input. It also informs the user that they can say "exit" or "quit" to stop the program.
print("System Ready! Say 'exit' or 'quit' to stop.")

#this loop continuously records audio, transcribes it, and interacts with the GPT model. It checks for specific exit commands to break the loop and allows for a seamless voice interaction experience.
#the system in its current state doesn't have a continous memory, meaning it cant remember previous interactions.
#This is a design choice to keep the number of used tokens low  and save on costs.

while True:
    record_wav(duration=4) # Shorter duration for snappier feel
    text = transcribe_audio()
    
    if text:
        print(f"You: {text}")
        
        if text.lower() in {"quit", "exit", "stop"}:
            speak_text("Goodbye!")
            break
            
        response_text = ask_gpt(text, dev_instruction)
        print(f"AI: {response_text}")
        speak_text(response_text)
    else:
        print("...") # Silence handling


#the following code sets up the speech recognizer and microphone. It adjusts for ambient noise to improve the accuracy of speech recognition, allowing the system to better hear the wake word or user input over background noise.
recognizer = sr.Recognizer()
microphone = sr.Microphone()

with microphone as source:
    # This helps the AI hear the wake word over background noise
    recognizer.adjust_for_ambient_noise(source, duration=1) 

#and we contiously listen for user input, allowing the system to respond in real-time to voice commands and interactions.
print("Listening for user input...")