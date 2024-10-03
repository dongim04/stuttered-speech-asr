import librosa
import whisper  

# Load the model  
model = whisper.load_model("base")  

# Load and transcribe audio   
file_path = "sample_data.wav"
input_audio, _ = librosa.load(file_path, sr=16000)
result = model.transcribe(input_audio)  
print(result["text"])  
