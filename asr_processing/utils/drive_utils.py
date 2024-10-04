import os
import pickle
import io
import pandas as pd
import csv
from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload #, MediaIoBaseUpload

# Set the scope to allow access to Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']

# Authenticate and build the Google Drive API service
def authenticate_drive():
    creds = None

    if os.path.exists('token.pickle'):
       with open('token.pickle', 'rb') as token:
           creds = pickle.load(token)
    if not creds or not creds.valid:
       if creds and creds.expired and creds.refresh_token:
           creds.refresh(Request())
       else:
           flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
           creds = flow.run_local_server(port=0)
       with open('token.pickle', 'wb') as token:
           pickle.dump(creds, token)

    # flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES) # Load credentials from credentials.json
    # creds = flow.run_console() #  URL to paste into browser on local machine

    service = build('drive', 'v3', credentials=creds)
    return service

# Returns a list of all files and folders within a given Google Drive folder.
def list_files_in_folder(service, folder_id):
    query = f"'{folder_id}' in parents and trashed = false"
    results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    return results.get('files', [])


# Recursive function to traverse folders and return paths of all audio files
def find_audio_files_in_folder(service, folder_id, audio_file_list=None, text_file_list=None):
    """Recursively find all .flac files within a Google Drive folder and its subfolders."""
    if audio_file_list is None:
        audio_file_list = []
        text_file_list = []

    # List all files and folders in the current folder
    items = list_files_in_folder(service, folder_id)

    for item in items:
        item_id = item['id']
        item_name = item['name']
        mime_type = item['mimeType']

        # Check if it's a folder (mimeType for Google Drive folders)
        if mime_type == 'application/vnd.google-apps.folder':
            # Recursively search this folder
            # print(f"Entering folder: {item_name}")
            find_audio_files_in_folder(service, item_id, audio_file_list, text_file_list)
        elif item_name.endswith('.flac'):
            # It's a .flac file, add to the list
            # print(f"Found audio file: {item_name}")
            audio_file_list.append({
                'file_id': item_id,
                'file_name': item_name
            })
        elif item_name.endswith('.txt'):
            text_file_list.append({
                'file_id': item_id,
                'file_name': item_name
            })
        elif item_name.endswith('.csv'):
            text_file_list.append({
                'file_id': item_id,
                'file_name': item_name
            })

    return audio_file_list, text_file_list


# Function to read a file (text or binary) from Google Drive into memory
def read_file_in_memory(service, file_id):
    try:
        # Download the file content
        fh = io.BytesIO()
        request = service.files().get_media(fileId=file_id)
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        fh.seek(0)
        return fh
    except Exception as e:
        print(f"Error reading file: {e}")
        raise e

# # Function to upload modified files back to Google Drive
# def upload_file_to_drive(service, output_folder_id, output_file_name, data):
#     # Prepare the file metadata for upload
#     file_metadata = {
#         'name': output_file_name,
#         'parents': [output_folder_id]
#     }

#     # Upload as a new file
#     media = MediaIoBaseUpload(data, mimetype='application/octet-stream')
#     file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
#     print(f"Uploaded file '{output_file_name}' with ID: {file.get('id')}")

# Main function to modify and upload all files from input to output folder
def read_folder_and_process(input_folder_id, modify_func, output_text_file_path):
    service = authenticate_drive()

    # Get all .flac files in the folder and subfolders
    audio_files, text_files = find_audio_files_in_folder(service, input_folder_id)

    if not audio_files:
        print(f"No audio files found in folder '{input_folder_id}'.")

    # Process each audio file
    for audio_file in audio_files:
        file_id = audio_file['file_id']
        file_name = audio_file['file_name']
        try:
            audio_data = read_file_in_memory(service, file_id)
            modify_func(audio_data, file_name)
        except Exception as e:
            print(f"Failed to process file '{file_name}': {e}")

    if not text_files:
        print(f"No text files found in folder '{input_folder_id}'.")

    # Process transcription file
    gt_transcriptions = []
    for text_file in text_files:
        file_id = text_file['file_id']
        file_name = text_file['file_name']
        transcription_words = []
        total_stutter = 0
        try:
            text_data = read_file_in_memory(service, file_id).getvalue().decode('utf-8')
            if file_name.endswith('txt'):
                # Process each line in the text file
                for line in text_data.strip().splitlines():
                    line_split = line.split(' ', 1)
                    if len(line_split) == 2:
                        file_name_in_line = line_split[0]  # File name part
                        transcription_text = line_split[1]  # Transcription text

                        # Append to ground truth transcriptions list
                        gt_transcriptions.append({
                            'file_name': file_name_in_line,
                            'ground_truth': transcription_text.lower()
                        })
            elif file_name.endswith('csv'):
                reader = csv.reader(io.StringIO(text_data), delimiter=',')

                for row in reader:
                    print(row)
                    transcription_word = row[0]
                    stutter_value = int(row[3])
                    transcription_words.append(transcription_word)
                    total_stutter += stutter_value

                gt_transcriptions.append({
                    'file_name': file_name,
                    'gt_transcriptions': ' '.join(transcription_words).lower(),
                    'total_stutter': total_stutter
                })
        except Exception as e:
            print(f"Failed to process file '{file_name}': {e}")
    df_transc = pd.DataFrame(gt_transcriptions)
    df_transc.to_csv(output_text_file_path)