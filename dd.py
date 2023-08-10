import os
import requests
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Fungsi untuk mengunduh file dari URL
def download_file(url, save_path):
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

# Fungsi untuk mengunggah file ke Google Drive
def upload_to_google_drive(file_path, drive_folder_id=None):
    SCOPES = ['https://www.googleapis.com/auth/drive.file']

    creds = ServiceAccountCredentials.from_service_account_file('service-account-key.json', scopes=SCOPES)
    creds.refresh(Request())

    service = build('drive', 'v3', credentials=creds)

    file_name = os.path.basename(file_path)
    metadata = {'name': file_name}
    if drive_folder_id:
        metadata['parents'] = [drive_folder_id]

    media = service.files().create(body=metadata, media_body=file_path).execute()
    print(f'File "{file_name}" berhasil diunggah ke Google Drive dengan ID: {media["id"]}')

if __name__ == '__main__':
    url = input("Masukkan URL file yang akan diunduh: ")

    file_name = os.path.basename(url)
    download_path = os.path.join(os.getcwd(), file_name)
    download_file(url, download_path)

    folder_id = '1x1PFmqLvC7wzt3Eqbs5rtr6QhyidKb1p'
    upload_to_google_drive(download_path, drive_folder_id=folder_id)
