from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account
# gcs_uri = "C:\\Users\\ChanMengKwan\\Downloads\\yes.wav"
from google.cloud import speech_v1p1beta1 as speech

#google.api_core.exceptions.InvalidArgument: 400 Request payload size exceeds the limit: 10485760 bytes.
speech_file = "C:\\Users\\ChanMengKwan\\Downloads\\yes6_1.wav"

from google.cloud import speech

import base64

def audio_to_base64(file_path):
    with open(file_path, "rb") as audio_file:
        audio_content = audio_file.read()
        audio_base64 = base64.b64encode(audio_content).decode("utf-8")
    return audio_base64

def speech_to_text(
    config: speech.RecognitionConfig,
    audio: speech.RecognitionAudio,
) -> speech.RecognizeResponse:
    client = speech.SpeechClient()

    # Synchronous speech recognition request
    response = client.recognize(config=config, audio=audio)
    return response


def print_response(response: speech.RecognizeResponse):
    for result in response.results:
        print_result(result)


def print_result(result: speech.SpeechRecognitionResult):
    best_alternative = result.alternatives[0]
    print("-" * 80)
    print(f"language_code: {result.language_code}")
    print(f"transcript:    {best_alternative.transcript}")
    print(f"confidence:    {best_alternative.confidence:.0%}")

config = speech.RecognitionConfig(
    # language_code="zh-CN",
    language_code="en-US",
    model="phone_call",
    enable_automatic_punctuation=True

)

audio_file = speech_file  # Replace with your audio file path
inline_content = audio_to_base64(audio_file)
print("Inline Content:")
print(inline_content)
audio = speech.RecognitionAudio(
    content = inline_content
    # uri="gs://cloud-samples-data/speech/brooklyn_bridge.flac",
)

response = speech_to_text(config, audio)
print_response(response)
    