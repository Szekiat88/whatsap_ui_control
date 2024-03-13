import speech_recognition as sr
import os

os.environ.get('AIzaSyBkLnAH2_VdwQDkf_gobRNRhe8eFdRMGl8') 

def audio_to_text(file_path):
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)  # Read the entire audio file
        
        try:
            text = recognizer.recognize_google(audio_data, language='en-US', key='AIzaSyBkLnAH2_VdwQDkf_gobRNRhe8eFdRMGl8')  # Specify Mandarin language
            # text = recognizer.recognize_google_cloud(audio_data, language='zh-CN')  # Specify Mandarin language
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
