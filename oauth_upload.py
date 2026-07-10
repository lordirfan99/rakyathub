import os, json, socket, sys
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Try to read credentials from common locations
cred_paths = [
    r'C:\Users\irfan\credentials.json',
    r'C:\Users\irfan\.credentials\client_secret.json',
    r'C:\Users\irfan\.config\google\credentials.json',
]

creds = None
cred_file = None
for p in cred_paths:
    if os.path.exists(p):
        cred_file = p
        print(f"Found credentials: {p}")
        break

if not cred_file:
    # Check env
    env_creds = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if env_creds and os.path.exists(env_creds):
        cred_file = env_creds
        print(f"Found credentials from env: {env_creds}")

if not cred_file:
    print("No credentials file found.")
    print("Please save your Google OAuth client credentials to one of:")
    for p in cred_paths:
        print(f"  {p}")
    sys.exit(1)

# Start local server to get token
flow = InstalledAppFlow.from_client_secrets_file(cred_file, SCOPES)
creds = flow.run_local_server(port=8080, open_browser=False)

# Upload
service = build('drive', 'v3', credentials=creds)
local_path = r'C:\Users\irfan\rakyathub\spain-belgium-analysis.py'
media = MediaFileUpload(local_path, mimetype='text/x-python', resumable=True)
uploaded = service.files().create(
    body={'name': 'spain-belgium-analysis.py'},
    media_body=media,
    fields='id,name,webViewLink,size'
).execute()

print(f"✅ Uploaded!")
print(f"   ID: {uploaded['id']}")
print(f"   Name: {uploaded['name']}")
print(f"   Link: {uploaded.get('webViewLink', 'N/A')}")
