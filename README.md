````md
# Voice GPT Assistant

## Overview

Voice GPT Assistant is a Python-based voice interaction program that allows users to speak to an AI assistant and receive spoken responses. The program records audio from the user’s microphone, converts the speech into text, sends the text to an OpenAI GPT model, and then converts the AI’s response back into speech.

At the start of the program, the user can define the assistant’s role. For example, the assistant can act as a coding helper, maths tutor, study assistant, or general chatbot.

## Features

- Records voice input through the microphone
- Converts speech into text using SpeechRecognition
- Sends user prompts to an OpenAI GPT model
- Converts AI responses into spoken audio using OpenAI text-to-speech
- Allows the user to define the assistant’s role
- Supports exit commands such as `exit`, `quit`, and `stop`
- Handles unclear speech without crashing the program

## Technologies Used

- Python
- OpenAI API
- SoundDevice
- SpeechRecognition
- PyDub
- Google Web Speech API
- FFmpeg

## Requirements

Before running the program, make sure Python is installed on your system.

Install the required Python libraries using pip:

```bash
pip install openai pydub speechrecognition sounddevice
````

PyDub also requires FFmpeg for audio processing. On macOS, FFmpeg can be installed using Homebrew:

```bash
brew install ffmpeg
```

## API Key Setup

This project requires an OpenAI API key.

For security reasons, the API key has not been made available in this push.



## How to Run

After installing the required libraries and setting up the API key, run the program with:

```bash
python voice-gpt.py
```

The program will ask:

```text
What should the assistant's role be?
```

You can enter a role such as:

```text
Math tutor
```

or:

```text
Helpful coding assistant
```

The assistant will then begin listening for voice input and responding with spoken audio.

## How It Works

The program is built around four main functions and one main loop.

### ask_gpt(prompt, instruction)

This function sends the user’s transcribed speech to the OpenAI GPT model. The instruction defines the assistant’s role, while the prompt contains what the user said.

### record_wav(filename, duration, samplerate)

This function records audio from the microphone and saves it as a WAV file. The default sample rate is 16000 Hz, which is suitable for speech recognition.

### transcribe_audio(filename)

This function reads the recorded WAV file and converts the speech into text using the SpeechRecognition library and Google’s Web Speech API. If the speech is unclear, the function returns `None` instead of stopping the program.

### speak_text(text)

This function converts the AI’s written response into speech using OpenAI text-to-speech. The audio is processed with PyDub and played back to the user.

### Main Loop

The main loop continuously:

1. Records the user’s voice
2. Converts the voice recording into text
3. Checks whether the user wants to exit
4. Sends the text to GPT
5. Prints the AI response
6. Speaks the AI response aloud

The loop ends when the user says:

```text
exit
quit
stop
```

## Limitations

* The program does not currently remember previous conversations.
* Each message is treated as a separate interaction.
* Speech recognition accuracy depends on microphone quality and background noise.
* Google Web Speech API requires an internet connection.
* OpenAI API usage may cost money depending on the user’s account and usage.
* The program records for a fixed number of seconds instead of automatically detecting when the user has stopped speaking.

## Future Improvements

Possible future improvements include:

* Adding conversation memory
* Adding a wake word
* Improving real-time listening
* Allowing the user to choose different AI voices
* Saving conversation history to a file
* Creating a graphical user interface
* Improving error handling
* Using environment variables by default for safer API key management

## Example Usage

```text
What should the assistant's role be?
> Physics tutor

System Ready! Say 'exit' or 'quit' to stop.

You: Explain Ohm's law
AI: Ohm's law states that voltage is equal to current multiplied by resistance.
```

## Author

Created by: Ege Mestçi

## License

This project is for educational purposes.


