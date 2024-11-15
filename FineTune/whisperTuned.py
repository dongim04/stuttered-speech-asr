import pandas as pd
import os
import librosa
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
import torch

# model = load_model("base")
predicted_transcriptions = []

# Load model directly
processor = AutoProcessor.from_pretrained("dongim04/whisper-base-en")
model = AutoModelForSpeechSeq2Seq.from_pretrained("dongim04/whisper-base-en")

# def transcribe_wav_file(data, file_name):
#     with open('temp.wav', 'wb') as f:
#         f.write(data.read())
#     input_audio, _ = librosa.load('temp.wav', sr=16000)
#     out = model.transcribe(input_audio)      
#     result = out['text']
    
#     predicted_transcriptions.append({
#         'file_name': file_name,
#         'prediction': result.lower()
#     })
#     if os.path.exists('temp.wav'):
#         os.remove('temp.wav')
#     return None

# def save_transcriptions_to_csv(audio_csv_file_name):
#     df = pd.DataFrame(predicted_transcriptions)
#     df.to_csv(audio_csv_file_name)
    
#input_folder_id = '1AdEu1i1kkuQIRBCEC6MqlpGSk0EGHUy-' # LibriSpeech train-clean-100
# # output_file_path = '/home/ec2-user/stuttered-speech-asr/librispeech_result/whisper_librispeech.csv'
#output_file_path = 'C:/Users/dlee3/OneDrive - Olin College of Engineering/PInT/stuttered-speech-asr/librispeech_result/whisper_librispeech.csv'


# read_folder_and_process(input_folder_id, transcribe_wav_file, '')
# save_transcriptions_to_csv(output_file_path)


# Load the processor
# processor = AutoProcessor.from_pretrained("dongim04/whisper-base-en")



# Print the transcription
print("Transcription:", transcription)



def tokenizeDirectory():
    # Walk through the directory and print each file with its full path
    for dirpath, dirnames, filenames in os.walk('/path/to/directory'):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)

            # Load the audio file (e.g., 'audio.flac') with librosa
            audio, sr = librosa.load(full_path, sr=16000)  # sr=16000 to match model requirements

            # Tokenize the audio
            inputs = processor(audio, sampling_rate=sr, return_tensors="pt")

            # Print the tokenized input
            print(inputs)

            # Perform inference to get the model's predicted output
            with torch.no_grad():
                generated_ids = model.generate(inputs["input_features"])

            # Decode the generated IDs to text
            transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            print(full_path)
            new_row = pd.DataFrame({'Filename': {filename}, 'TunedTranscription': {transcription}})
            df = df.append(new_row, ignore_index=True)


df = pd.DataFrame({'Filename':[],'TunedTranscription':'' })

df.to_csv('data.csv', index=False)
