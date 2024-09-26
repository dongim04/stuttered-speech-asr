import os
import pickle
import io
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload

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

    service = build('drive', 'v3', credentials=creds)
    return service

# Function to list all files in a Google Drive folder
def list_files_in_folder(service, folder_id):
    query = f"'{folder_id}' in parents"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    return results.get('files', [])

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

# Function to upload modified files back to Google Drive
def upload_file_to_drive(service, output_folder_id, output_file_name, data):
    # Prepare the file metadata for upload
    file_metadata = {
        'name': output_file_name,
        'parents': [output_folder_id]
    }

    # Upload as a new file
    media = MediaIoBaseUpload(data, mimetype='application/octet-stream')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"Uploaded file '{output_file_name}' with ID: {file.get('id')}")

# Main function to modify and upload all files from input to output folder
def modify_and_upload_all_files(input_folder_id, output_folder_id, modify_func, file_extension):
    service = authenticate_drive()

    # List all files in the input folder
    files = list_files_in_folder(service, input_folder_id)

    if not files:
        print(f"No files found in folder '{input_folder_id}'.")
        return

    # Process each file in the folder
    for file in files:
        file_id = file['id']
        file_name = file['name']

        try:
            # Check the file extension
            if not file_name.lower().endswith(file_extension):
                print(f"Skipping file with unsupported extension: {file_name}")
                continue

            # Read the file into memory
            data = read_file_in_memory(service, file_id)

            # Call the modify_func and pass both data and file_name
            modify_func(data, file_name)

        except Exception as e:
            continue
