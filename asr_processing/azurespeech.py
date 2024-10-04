from utils.drive_utils import read_folder_and_process
import pandas as pd
import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig

subscription_key = "5f393d5cc2c14b5e81c879e4e0ff8ba6"
location = "eastus"
speech_config = SpeechConfig(subscription=subscription_key, region=location, speech_recognition_language="en-US")


predicted_transcriptions = []

def transcribe_wav_file(data, file_name):
    with open('temp.wav', 'wb') as f:
        f.write(data.read())

    audio_config = AudioConfig(filename='sample_data.wav')
    speech_recognizer = SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    output = speech_recognizer.recognize_once()
    result = output.text

    predicted_transcriptions.append({
        'file_name': file_name,
        'prediction': result.lower()
    })
    if os.path.exists('temp.wav'):
        os.remove('temp.wav')
    return None

def save_transcriptions_to_csv(audio_csv_file_name):
    df = pd.DataFrame(predicted_transcriptions)
    df.to_csv(audio_csv_file_name)
    
# input_folder_id = '1AdEu1i1kkuQIRBCEC6MqlpGSk0EGHUy-' # LibriSpeech train-clean-100
# # output_file_path = '/home/ec2-user/stuttered-speech-asr/librispeech_result/azure_librispeech.csv'
# output_file_path = 'C:/Users/dlee3/OneDrive - Olin College of Engineering/PInT/stuttered-speech-asr/librispeech_result/azure_librispeech.csv'

input_folder_id = '1LW2FqGlbWVTFgQCMp3sfFa0KsNFEd6tM' # LibriStutter
# output_file_path = '/home/ec2-user/stuttered-speech-asr/libristutter_result/azure_libristutter.csv'
output_file_path = 'C:/Users/dlee3/OneDrive - Olin College of Engineering/PInT/stuttered-speech-asr/libristutter_result/azure_libristutter.csv'

read_folder_and_process(input_folder_id, transcribe_wav_file, '')
save_transcriptions_to_csv(output_file_path)