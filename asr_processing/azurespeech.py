from utils.drive_utils import read_folder_and_process
import pandas as pd
import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer
from azure.cognitiveservices.speech.audio import AudioConfig
import io
import azure.cognitiveservices.speech as speechsdk

predicted_transcriptions = []
'''
def transcribe_wav_file(data, file_name):
    temp_file_path = 'temp.wav'
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)
        print(file_name, "pre-removed!")
    with open(temp_file_path, 'wb') as f:
        f.write(data.read())

    speech_config = SpeechConfig(subscription="5f393d5cc2c14b5e81c879e4e0ff8ba6", region="eastus", speech_recognition_language="en-US")
    audio_config = AudioConfig(filename=temp_file_path)
    print(111)
    speech_recognizer = SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    print(222)
    output = speech_recognizer.recognize_once()
    result = output.text

    predicted_transcriptions.append({
        'file_name': file_name,
        'prediction': result.lower()
    })
    print(file_name, result)
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)
        print(file_name, "removed!")
    return None
'''

def transcribe_wav_file(audio_bytes, file_name):

    speech_key = "3e808c6496e5437bb27d9e03e35fea28"
    service_region = "eastus"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Configure audio input from the BytesIO object
    # You need to specify the audio format (e.g., 16kHz, mono, PCM, etc.)
    audio_format = speechsdk.audio.AudioStreamFormat(samples_per_second=16000, bits_per_sample=16, channels=1)

    class ByteStream(speechsdk.audio.PullAudioInputStreamCallback):
        def __init__(self, byte_stream):
            super().__init__()
            self.byte_stream = byte_stream

        def read(self, buffer):
            size = len(buffer)
            data = self.byte_stream.read(size)
            buffer[:len(data)] = data
            return len(data)

        def close(self):
            self.byte_stream.close()

    audio_stream = speechsdk.audio.PullAudioInputStream(stream_format=audio_format, pull_stream_callback=ByteStream(audio_bytes))
    audio_input = speechsdk.audio.AudioConfig(stream=audio_stream)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
    print("Recognizing...")
    result = speech_recognizer.recognize_once()
    print(result)

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
    return None


def save_transcriptions_to_csv(audio_csv_file_name):
    df = pd.DataFrame(predicted_transcriptions)
    df.to_csv(audio_csv_file_name)
    
input_folder_id = '1AdEu1i1kkuQIRBCEC6MqlpGSk0EGHUy-' # LibriSpeech train-clean-100
# output_file_path = '/home/ec2-user/stuttered-speech-asr/librispeech_result/azure_librispeech.csv'
output_file_path = 'C:/Users/dlee3/OneDrive - Olin College of Engineering/PInT/stuttered-speech-asr/librispeech_result/azure_librispeech.csv'

# input_folder_id = '1LW2FqGlbWVTFgQCMp3sfFa0KsNFEd6tM' # LibriStutter
# # output_file_path = '/home/ec2-user/stuttered-speech-asr/libristutter_result/azure_libristutter.csv'
# output_file_path = 'C:/Users/dlee3/OneDrive - Olin College of Engineering/PInT/stuttered-speech-asr/libristutter_result/azure_libristutter.csv'

read_folder_and_process(input_folder_id, transcribe_wav_file, '')
save_transcriptions_to_csv(output_file_path)