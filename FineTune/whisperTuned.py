import pandas as pd
import os
import librosa
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
import torch

# Load model and processor
processor = AutoProcessor.from_pretrained("dongim04/whisper-base-en")
model = AutoModelForSpeechSeq2Seq.from_pretrained("dongim04/whisper-base-en")

# Initialize an empty list to store the results
transcription_data = []

def tokenizeDirectory():
    # Walk through the directory and process each file
    for dirpath, dirnames, filenames in os.walk('C:/Users/xnishikawa/Downloads/libristutter_audio'):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            
            try:
                # Load the audio file
                audio, sr = librosa.load(full_path, sr=16000)

                # Tokenize the audio
                inputs = processor(audio, sampling_rate=sr, return_tensors="pt")

                # Perform inference
                with torch.no_grad():
                    generated_ids = model.generate(inputs["input_features"])

                # Decode the generated IDs to text
                transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
                
                # Append the result to our list
                transcription_data.append({
                    'Filename': filename,
                    'TunedTranscription': transcription
                })
                
                print(f"Processed: {filename}")
                print(f"Transcription: {transcription}")
                
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

    # Create DataFrame from all collected data at once
    df = pd.DataFrame(transcription_data)
    
    # Save to CSV
    df.to_csv('data.csv', index=False)
    print(f"Saved {len(transcription_data)} transcriptions to data.csv")

if __name__ == "__main__":
    tokenizeDirectory()