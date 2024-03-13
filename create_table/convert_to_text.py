import speech_recognition as sr

def audio_to_text(file_path):
    recognizer = sr.Recognizer()

    # Load audio file
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)  # Read the entire audio file

        try:
            # Recognize speech using Google Speech Recognition
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Google Speech Recognition could not understand the audio"
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"

if __name__ == "__main__":
    audio_file = "C:\\Users\\ChanMengKwan\\Downloads\\yes3.wav"  # Provide the path to your audio file
    recognized_text = audio_to_text(audio_file)
    print("Recognized Text:")
    print(recognized_text)
