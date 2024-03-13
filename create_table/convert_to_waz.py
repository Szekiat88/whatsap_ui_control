from pydub import AudioSegment

def convert_ogg_to_wav(ogg_file, wav_file):
    # Load OGG file
    audio = AudioSegment.from_ogg(ogg_file)
    
    # Export as WAV file
    audio.export(wav_file, format="wav")

# Specify the paths to your OGG and WAV files
ogg_file = "C:\\Users\\ChanMengKwan\\Downloads\\yes2.ogg"
wav_file = "C:\\Users\\ChanMengKwan\\Downloads"

# Convert OGG to WAV
convert_ogg_to_wav(ogg_file, wav_file)

# Now you can use the WAV file with SpeechRecognition
