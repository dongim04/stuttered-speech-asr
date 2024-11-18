from utils.drive_utils import read_folder_and_process, read_file_in_memory, authenticate_drive
import pandas as pd
from google.cloud import speech
from google.oauth2 import service_account
import os

client_file = "C:/Users/dlee3/OneDrive - Olin College of Engineering/PInT/stuttered-speech-asr/credentials2.json"
credentials = service_account.Credentials.from_service_account_file(client_file)
client = speech.SpeechClient(credentials=credentials)


predicted_transcriptions = []

folder_path = 'C:/Users/dlee3/OneDrive - Olin College of Engineering/PInT/stuttered-speech-asr/asr_processing/209'

for filename in os.listdir(folder_path):
    result = ''
    file_path = f'{folder_path}/{filename}'
    with open(file_path, "rb") as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # PCM format in 32-bit floating point audio
        sample_rate_hertz=22050,  # Sample rate from the file (22050 Hz)
        language_code="en-US",  # Language of the audio (you can change this)
        audio_channel_count=1,  # Mono channel
    )
    response = client.recognize(config=config, audio=audio)
    # print("res", response)
    for result_string in response.results:
        result += result_string.alternatives[0].transcript

    predicted_transcriptions.append({ # Append the result to the predicted_transcriptions list
        'file_name': filename,
        'prediction': result.lower()
    })
    print(result, f'\nsaving transcriptions of', filename)


# output_file_path = '/home/ec2-user/stuttered-speech-asr/libristutter_result/googlecloud_libristutter.csv'
output_file_path = 'C:/Users/dlee3/OneDrive - Olin College of Engineering/PInT/stuttered-speech-asr/libristutter_result/googlecloud_libristutter.csv'

df = pd.DataFrame(predicted_transcriptions)
df.to_csv(output_file_path, mode='a', index=True, header=False)