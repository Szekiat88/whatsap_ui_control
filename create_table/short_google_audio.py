import argparse

from google.cloud import speech
from google.cloud.speech_v2.types import cloud_speech


def transcribe_file(speech_file: str) -> speech.RecognizeResponse:
    """Transcribe the given audio file."""
    client = speech.SpeechClient()

    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=48000,
        # language_code="zh-CN",
        language_code="en-US",
        model="phone_call",
        enable_automatic_punctuation= True,

    )

    # response = client.recognize(config=config, audio=audio)
    response = client.long_running_recognize(config=config, audio=audio)


    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(f"Transcript: {result.alternatives[0].transcript}")

    return response

print(transcribe_file("C:\\Users\\ChanMengKwan\\Downloads\\yes1.wav"))
