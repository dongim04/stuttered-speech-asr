from utils.drive_utils import read_folder_and_modify
import pandas as pd
import os
from whisper import load_model
import librosa


model = load_model("base")
transcriptions = []

def transcribe_wav_file(data, file_name):
    with open('temp.wav', 'wb') as f:
        f.write(data.read())
    input_audio, _ = librosa.load('temp.wav', sr=16000)
    out = model.transcribe(input_audio)      
    result = out['text']
    
    transcriptions.append({
        'file_name': file_name,
        'prediction': result.lower()
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
