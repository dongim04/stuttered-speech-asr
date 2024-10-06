import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig
import csv

subscription_key = "" #Enter your custom subscription_key here
location = "eastus"
endpoint = "https://eastus.api.cognitive.microsoft.com/" # Enter your model's endpoint here
wav_base_path = "C:\\202425\\pint\\LibriStutter Audio-20240930T230826Z-001\\LibriStutter Audio\\"

config = SpeechConfig(subscription=subscription_key, region=location)
config.endpoint_id = endpoint
speech_config = SpeechConfig(subscription=subscription_key, region=location, speech_recognition_language="en-US")

predictions = []
file_names = []

for root, _, files in os.walk(wav_base_path):
    for file_name in files:
        if file_name.endswith(".flac"):
            temp = []
            audio_file_path = os.path.join(root, file_name)
            print(file_name)
            audio_config = AudioConfig(filename=audio_file_path)
            speech_recognizer = SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

            result = speech_recognizer.recognize_once()
            if result.text:
                transcribed_text = result.text
                predictions.append(transcribed_text)
                file_names.append(file_name)
                temp = [file_name, transcribed_text]
                # opening the csv file in 'w+' mode
                with open('test1.csv', mode='a', newline='') as file:
                    writer = csv.writer(file) 
                    writer.writerow(temp)
            else:
                print("Speech Recognition failed for file:", audio_file_path)
                temp = [file_name]
                with open('fail1.csv', mode='a', newline='') as file:
                    writer = csv.writer(file) 
                    writer.writerow(temp)
            
            
print(file_names)
print(predictions)
