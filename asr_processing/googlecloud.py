from utils.drive_utils import read_folder_and_process, read_file_in_memory, authenticate_drive
import pandas as pd
from google.cloud import speech
from google.oauth2 import service_account

client_file = "C:/Users/dlee3/OneDrive - Olin College of Engineering/PInT/stuttered-speech-asr/credentials2.json"
credentials = service_account.Credentials.from_service_account_file(client_file)
client = speech.SpeechClient(credentials=credentials)
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
    sample_rate_hertz=16000,
    language_code="en-US",
)

predicted_transcriptions = []

def transcribe_wav_file(data, file_name):
    result = ''
    audio = speech.RecognitionAudio(content=data.read())
    response = client.recognize(request={"config": config, "audio": audio})
    print("res", response)
    for result_string in response.results:
        result += result_string.alternatives[0].transcript

    predicted_transcriptions.append({ # Append the result to the predicted_transcriptions list
        'file_name': file_name,
        'prediction': result.lower()
    })
    print(result[:10], f'\nsaving transcriptions of', file_name)
    return None  # No need to return anything since we are not saving individual files

# transcribe_wav_file(None, None)
def save_transcriptions_to_csv(audio_csv_file_name):
    df = pd.DataFrame(predicted_transcriptions)
    df.to_csv(audio_csv_file_name)


# input_folder_id = '1AdEu1i1kkuQIRBCEC6MqlpGSk0EGHUy-' # LibriSpeech train-clean-100
# # output_file_path = '/home/ec2-user/stuttered-speech-asr/librispeech_result/googlecloud_librispeech.csv'
# output_file_path = 'C:/Users/dlee3/OneDrive - Olin College of Engineering/PInT/stuttered-speech-asr/librispeech_result/googlecloud_librispeech.csv'

input_folder_id = '1m7DixM5FBed81Ivvt4jaRmBtDDP5bTAF' #'1LW2FqGlbWVTFgQCMp3sfFa0KsNFEd6tM' # LibriStutter
# output_file_path = '/home/ec2-user/stuttered-speech-asr/libristutter_result/googlecloud_libristutter.csv'
output_file_path = 'C:/Users/dlee3/OneDrive - Olin College of Engineering/PInT/stuttered-speech-asr/libristutter_result/googlecloud_libristutter.csv'

read_folder_and_process(input_folder_id, transcribe_wav_file, '')
save_transcriptions_to_csv(output_file_path)