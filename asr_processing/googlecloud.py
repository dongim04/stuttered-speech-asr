from utils.drive_utils import read_folder_and_modify
import pandas as pd
import os
### STEP1: IMPORT LIBRARIES
from google.cloud import speech
import io

# Instantiates a client from google cloud
client = speech.SpeechClient()

### STEP2: DEFINE MODEL
# What do i put here??

transcriptions = []

def transcribe_wav_file(data, file_name):
    answer = ''
    # Prepare the RecognitionAudio object
    with io.open(temp.wav, "wb") as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)

        # Set up the RecognitionConfig
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Ensure this matches your file format
        sample_rate_hertz=8000, 
        language_code="en-US",  # Language of the audio
    )

    # Call the API to transcribe the audio
    response = client.recognize(config=config, audio=audio)

    # Process the response and save the transcript to answer
    for resultString in response.results:
        answer += resultString.alternatives[0].transcript

    transcriptions.append({
        'file_name': file_name,
        'prediction': answer.lower()
    })
    
    if os.path.exists('temp.wav'):
        os.remove('temp.wav')
    return None

def save_transcriptions_to_csv(csv_file_name):
    df = pd.DataFrame(transcriptions)
    df.to_csv(csv_file_name)
    
input_folder_id = '1GwqjWYJlE62IBSWnfkhVt34VHNSrZlmY'
read_folder_and_modify(input_folder_id, transcribe_wav_file, file_extension='.wav')
save_transcriptions_to_csv('/home/ec2-user/stuttered-speech-asr/predicted_transcriptions/azure_transcr.csv')