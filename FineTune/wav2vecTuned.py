import pandas as pd
import os
import librosa
# Load model directly
from transformers import AutoProcessor, AutoModelForCTC
import torch

processor = AutoProcessor.from_pretrained("dongim04/wav2vec-large-en")
model = AutoModelForCTC.from_pretrained("dongim04/wav2vec-large-en")

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
                
                # audio file is decoded on the fly
                inputs = processor(audio, sampling_rate=sr, return_tensors="pt")
                with torch.no_grad():
                    logits = model(**inputs).logits
                predicted_ids = torch.argmax(logits, dim=-1)

                # Decode the generated IDs to text
                transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
                print("test, ", logits.shape)
                print("predictedID", predicted_ids.shape)

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
    df.to_csv('FineTune/dataWav2Vec.csv', index=False)
    print(f"Saved {len(transcription_data)} transcriptions to dataWav2Vec.csv")

if __name__ == "__main__":
    tokenizeDirectory()