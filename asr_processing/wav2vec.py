from utils.drive_utils import read_folder_and_modify
import pandas as pd
import os
### STEP1: IMPORT LIBRARIES
import librosa
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer

### STEP2: DEFINE MODEL
tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

transcriptions = []

def transcribe_wav_file(data, file_name):
    with open('temp.wav', 'wb') as f: # Write the audio data into a temporary file in memory
        f.write(data.read())

    ### STEP3: SAVE TRANSCRIPTION OUTPUT (STRING TYPE) | file_path = 'temp.wav'
    input_audio, _ = librosa.load('temp.wav', sr=16000)
    input_values = tokenizer(input_audio, return_tensors="pt").input_values 
    result = tokenizer.batch_decode(torch.argmax(model(input_values).logits, dim=-1))[0] # Use Wav2vec to transcribe the audio file

    transcriptions.append({ # Append the result to the transcriptions list
        'file_name': file_name,
        'prediction': result.lower()
    })
    if os.path.exists('temp.wav'):
        os.remove('temp.wav')
    return None  # No need to return anything since we are not saving individual files

def save_transcriptions_to_csv(csv_file_name):
    df = pd.DataFrame(transcriptions)
    df.to_csv(csv_file_name)

input_folder_id = '1GwqjWYJlE62IBSWnfkhVt34VHNSrZlmY' # Input folder ID from Google Drive
read_folder_and_modify(input_folder_id, transcribe_wav_file, file_extension='.wav')
save_transcriptions_to_csv('/home/ec2-user/stuttered-speech-asr/predicted_transcriptions/wav2vec_transcr.csv')