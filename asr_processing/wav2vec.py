from utils.drive_utils import read_folder_and_process
import pandas as pd
import os
### STEP1: IMPORT LIBRARIES
import librosa
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer

### STEP2: DEFINE MODEL
tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

predicted_transcriptions = []

def transcribe_wav_file(data, file_name):
    with open('temp.wav', 'wb') as f: # Write the audio data into a temporary file in memory
        f.write(data.read())

    ### STEP3: SAVE TRANSCRIPTION OUTPUT (STRING TYPE) | file_path = 'temp.wav'
    input_audio, _ = librosa.load('temp.wav', sr=16000)
    input_values = tokenizer(input_audio, return_tensors="pt").input_values 
    result = tokenizer.batch_decode(torch.argmax(model(input_values).logits, dim=-1))[0] # Use Wav2vec to transcribe the audio file

    predicted_transcriptions.append({ # Append the result to the predicted_transcriptions list
        'file_name': file_name,
        'prediction': result.lower()
    })
    print('saving transcriptions of', file_name)
    if os.path.exists('temp.wav'):
        os.remove('temp.wav')
    return None  # No need to return anything since we are not saving individual files

def save_transcriptions_to_csv(audio_csv_file_name):
    df = pd.DataFrame(predicted_transcriptions)
    df.to_csv(audio_csv_file_name)

# input_folder_id = '1AdEu1i1kkuQIRBCEC6MqlpGSk0EGHUy-' # LibriSpeech train-clean-100
# # output_text_file_path = '/home/ec2-user/stuttered-speech-asr/librispeech_result/gt_librispeech.csv'
# # output_file_path = '/home/ec2-user/stuttered-speech-asr/librispeech_result/wav2vec_librispeech.csv'
# output_text_file_path = 'C:/Users/dlee3/OneDrive - Olin College of Engineering/PInT/stuttered-speech-asr/librispeech_result/gt_librispeech.csv'
# output_file_path = 'C:/Users/dlee3/OneDrive - Olin College of Engineering/PInT/stuttered-speech-asr/librispeech_result/wav2vec_librispeech.csv'

input_folder_id = '1LW2FqGlbWVTFgQCMp3sfFa0KsNFEd6tM' # LibriStutter
# output_text_file_path = '/home/ec2-user/stuttered-speech-asr/libristutter_result/gt_libristutter.csv'
# output_file_path = '/home/ec2-user/stuttered-speech-asr/libristutter_result/wav2vec_libristutter.csv'
output_text_file_path = 'C:/Users/dlee3/OneDrive - Olin College of Engineering/PInT/stuttered-speech-asr/libristutter_result/gt_libristutter.csv'
output_file_path = 'C:/Users/dlee3/OneDrive - Olin College of Engineering/PInT/stuttered-speech-asr/libristutter_result/wav2vec_libristutter.csv'

read_folder_and_process(input_folder_id, transcribe_wav_file, output_text_file_path)
save_transcriptions_to_csv(output_file_path)