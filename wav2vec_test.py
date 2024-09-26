from utils.drive_utils import modify_and_upload_all_files, authenticate_drive, upload_file_to_drive
import io
import pandas as pd
import os

import librosa
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer

tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

# Create a list to store transcription results
transcriptions = []

# Custom modification function to transcribe wav files and store the result
def transcribe_wav_file(data, file_name):
    # Write the audio data into a temporary file in memory
    with open('temp.wav', 'wb') as f:
        f.write(data.read())

    # Use Wav2vec to transcribe the audio file
    input_audio, _ = librosa.load('temp.wav', sr=16000)
    input_values = tokenizer(input_audio, return_tensors="pt").input_values
    result = tokenizer.batch_decode(torch.argmax(model(input_values).logits, dim=-1))[0]


    # Append the result to the transcriptions list
    transcriptions.append({
        'file_name': file_name,
        'prediction': result
    })
    
    if os.path.exists('temp.wav'):
        os.remove('temp.wav')

    return None  # No need to return anything since we are not saving individual files

# After processing all files, save the accumulated results to a CSV file
def save_transcriptions_to_csv(output_folder_id, csv_file_name):
    # Convert the list of transcriptions to a DataFrame
    df = pd.DataFrame(transcriptions)

    # Save the DataFrame to a CSV in memory
    csv_data = io.StringIO()
    df.to_csv(csv_data, index=False)

    # Upload the CSV file to Google Drive
    service = authenticate_drive()
    upload_file_to_drive(service, output_folder_id, csv_file_name, io.BytesIO(csv_data.getvalue().encode('utf-8')))

# Input and output folder IDs from Google Drive
input_folder_id = '1GwqjWYJlE62IBSWnfkhVt34VHNSrZlmY'  # Folder containing wav files
output_folder_id = '15YGGTlUt-QH47axrESTlzNWCeb0EaJKL'  # Folder to save the transcription CSV

# Process all wav files in the input folder, accumulate the transcriptions in a list
modify_and_upload_all_files(input_folder_id, output_folder_id, transcribe_wav_file, file_extension='.wav')

# Save the accumulated transcriptions to a single CSV file in the output folder
save_transcriptions_to_csv(output_folder_id, 'transcriptions.csv')
