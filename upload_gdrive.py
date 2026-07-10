import google.auth
import google.auth.transport.requests
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

creds, project = google.auth.default()
print(f"Credentials: {type(creds).__name__}")
print(f"Valid: {creds.valid} | Scopes: {creds.scopes}")

if not creds.valid:
    creds.refresh(google.auth.transport.requests.Request())

service = build('drive', 'v3', credentials=creds)

local_path = r'C:\Users\irfan\rakyathub\spain-belgium-analysis.py'
print(f"File exists: {os.path.exists(local_path)}")
print(f"File size: {os.path.getsize(local_path)} bytes")

file_metadata = {'name': 'spain-belgium-analysis.py'}
media = MediaFileUpload(local_path, mimetype='text/x-python', resumable=True)

uploaded = service.files().create(
    body=file_metadata,
    media_body=media,
    fields='id,name,webViewLink,size'
).execute()

print(f"\n✅ Upload successful!")
print(f"   ID: {uploaded['id']}")
print(f"   Name: {uploaded['name']}")
print(f"   Size: {uploaded.get('size')} bytes")
print(f"   Link: {uploaded.get('webViewLink', 'N/A')}")
