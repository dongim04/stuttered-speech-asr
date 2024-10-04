from utils.drive_utils import read_folder_and_process
import pandas as pd
import os
### STEP1: IMPORT LIBRARIES
from google.cloud import speech
import io

# Instantiates a client from google cloud
client = speech.SpeechClient()

### STEP2: DEFINE MODEL
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Ensure this matches your file format
    sample_rate_hertz=8000, 
    language_code="en-US",  # Language of the audio
)

predicted_transcriptions = []

def transcribe_wav_file(data, file_name):
    result = ''
    audio = speech.RecognitionAudio(content=data.read())
    response = client.recognize(config=config, audio=audio)
    for resultString in response.results:
        result += resultString.alternatives[0].transcript

    print('res:', result)

    predicted_transcriptions.append({
        'file_name': file_name,
        'prediction': result.lower()
    })
    
    return None

def save_transcriptions_to_csv(audio_csv_file_name):
    df = pd.DataFrame(predicted_transcriptions)
    df.to_csv(audio_csv_file_name)


# input_folder_id = '1AdEu1i1kkuQIRBCEC6MqlpGSk0EGHUy-' # LibriSpeech train-clean-100
# # output_file_path = '/home/ec2-user/stuttered-speech-asr/librispeech_result/googlecloud_librispeech.csv'
# output_file_path = 'C:/Users/dlee3/OneDrive - Olin College of Engineering/PInT/stuttered-speech-asr/librispeech_result/googlecloud_librispeech.csv'

input_folder_id = '1LW2FqGlbWVTFgQCMp3sfFa0KsNFEd6tM' # LibriStutter
# output_file_path = '/home/ec2-user/stuttered-speech-asr/libristutter_result/googlecloud_libristutter.csv'
output_file_path = 'C:/Users/dlee3/OneDrive - Olin College of Engineering/PInT/stuttered-speech-asr/libristutter_result/googlecloud_libristutter.csv'

read_folder_and_process(input_folder_id, transcribe_wav_file, '')
save_transcriptions_to_csv(output_file_path)