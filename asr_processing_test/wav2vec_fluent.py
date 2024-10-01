### STEP1: IMPORT LIBRARIES
import librosa
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
import os

### STEP2: DEFINE MODEL
tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

### STEP3: SAVE TRANSCRIPTION OUTPUT (STRING TYPE)
folder_path = '270782'

my_dict = {}

for filename in os.listdir(folder_path) :
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path) and file_path.endswith(".flac"):


        input_audio, _ = librosa.load(file_path, sr=16000)
        input_values = tokenizer(input_audio, return_tensors="pt").input_values
        result = tokenizer.batch_decode(torch.argmax(model(input_values).logits, dim=-1))[0]
        my_dict[filename] = result

print(my_dict)