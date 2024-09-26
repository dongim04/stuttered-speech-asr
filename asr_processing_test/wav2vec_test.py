### STEP1: IMPORT LIBRARIES
import librosa
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer

### STEP2: DEFINE MODEL
tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

### STEP3: SAVE TRANSCRIPTION OUTPUT (STRING TYPE)
file_path = 'C:/Users/dlee3/OneDrive - Olin College of Engineering/PInT/stuttered-speech-asr/asr_processing_test/sample_data.wav'
input_audio, _ = librosa.load(file_path, sr=16000)
input_values = tokenizer(input_audio, return_tensors="pt").input_values
result = tokenizer.batch_decode(torch.argmax(model(input_values).logits, dim=-1))[0]

print(result)