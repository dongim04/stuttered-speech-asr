from google.cloud import speech
import io

# Instantiates a client
client = speech.SpeechClient()

# The path to the local audio file to transcribe
file_path = 'asr_processing_test/sample_data.wav'
answer = ""
def transcribe_speech():
    global answer
    # Read the local audio file
    with io.open(file_path, "rb") as audio_file:
        content = audio_file.read()

    # Prepare the RecognitionAudio object
    audio = speech.RecognitionAudio(content=content)

    # Set up the RecognitionConfig
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Ensure this matches your file format
        sample_rate_hertz=8000, 
        language_code="en-US",  # Language of the audio
    )

    # Call the API to transcribe the audio
    response = client.recognize(config=config, audio=audio) #audio and config gets fed into the tokenizer 

    # Process the response and save the transcript to a string
    for result in response.results:
        answer += result.alternatives[0].transcript

# Run the transcription
transcribe_speech()

print(answer)