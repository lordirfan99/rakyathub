"""Upload file to Google Drive using PyDrive2 with local OAuth."""
import json
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os

# Try to use existing OAuth credentials if available
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Opens browser for auth, but since we're headless, uses a local server

drive = GoogleDrive(gauth)

local_path = r'C:\Users\irfan\rakyathub\spain-belgium-analysis.py'
file_name = 'spain-belgium-analysis.py'

f = drive.CreateFile({'title': file_name})
f.SetContentFile(local_path)
f.Upload()

print(f"✅ Uploaded to Google Drive!")
print(f"   Title: {f['title']}")
print(f"   ID: {f['id']}")
print(f"   MIME: {f['mimeType']}")

# Try to get the web link
try:
    f.FetchMetadata(fields='webViewLink')
    print(f"   Link: {f.get('webViewLink', 'N/A')}")
except:
    pass
