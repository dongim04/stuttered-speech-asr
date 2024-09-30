# ### STEP 1: IMPORT LIBRARIES
import azure.cognitiveservices.speech as speechsdk
import os

# Set your Azure subscription key and service region
subscription_key = ""
service_region = "eastus"  # Ensure this is correct

# ### STEP 2: SET UP SPEECH CONFIGURATION
speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=service_region)

# ### STEP 3: SPECIFY THE PATH TO YOUR WAV FILE
audio_filename = r"asr_processing_test\sample_data.wav"  # Use a raw string for the path

# Check if the file exists
if not os.path.exists(audio_filename):
    print("File does not exist")
    exit()  # Exit if the file does not exist

# Create an audio configuration from the audio file
audio_input = speechsdk.audio.AudioConfig(filename=audio_filename)

# Create a speech recognizer
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

# Recognize speech from the audio file
try:
    print("Starting speech recognition...")
    result = speech_recognizer.recognize_once()
    
    # Check the result
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        transcribed_text = result.text
        print("Recognized text:", transcribed_text)
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Recognition canceled:", cancellation_details.reason)
        
        # Check for specific cancellation reasons
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("An error occurred during recognition.")
            if cancellation_details.error_details:
                print("Error details:", cancellation_details.error_details)
            else:
                print("No additional error details provided.")
        else:
            print("Cancellation reason:", cancellation_details.reason)

except Exception as e:
    print("An unexpected error occurred during speech recognition:", str(e))
