from utils.drive_utils import read_folder_and_process
import pandas as pd
import os
from whisper import load_model
import librosa


model = load_model("base")
predicted_transcriptions = []

def transcribe_wav_file(data, file_name):
    with open('temp.wav', 'wb') as f:
        f.write(data.read())
    input_audio, _ = librosa.load('temp.wav', sr=16000)
    out = model.transcribe(input_audio)      
    result = out['text']
    
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
# # output_file_path = '/home/ec2-user/stuttered-speech-asr/librispeech_result/wav2vec_librispeech.csv'
# output_file_path = 'C:/Users/dlee3/OneDrive - Olin College of Engineering/PInT/stuttered-speech-asr/librispeech_result/wav2vec_librispeech.csv'

input_folder_id = '1LW2FqGlbWVTFgQCMp3sfFa0KsNFEd6tM' # LibriStutter
# output_file_path = '/home/ec2-user/stuttered-speech-asr/libristutter_result/wav2vec_libristutter.csv'
output_file_path = 'C:/Users/dlee3/OneDrive - Olin College of Engineering/PInT/stuttered-speech-asr/libristutter_result/wav2vec_libristutter.csv'

read_folder_and_process(input_folder_id, transcribe_wav_file, '')
save_transcriptions_to_csv(output_file_path)