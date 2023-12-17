import base64
import json
import re
import sys
import os.path

from google.oauth2.service_account import Credentials
from national_membership_list import process_national_membership_list
from googleapiclient.discovery import build

from dotenv import load_dotenv
load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/drive"]
GOOGLE_ACCOUNT_CREDENTIALS = base64.b64decode(os.getenv("GOOGLE_ACCOUNT_CREDENTIAL_BASE64"))
INCOMING_FOLDER_ID = os.getenv("INCOMING_FOLDER_ID")

FILE_HANDLERS = (
    (
        r"^\d{4}-\d{2}-\d{2} National Membership List.csv$",
        process_national_membership_list,
    ),
)

def main(argv):
    service_account_info = json.loads(GOOGLE_ACCOUNT_CREDENTIALS)
    credentials = Credentials.from_service_account_info(service_account_info)

    print("Initializing ingest-drive-files")
    print("Google account credential account:", credentials.service_account_email)
    print("Incoming folder ID:", INCOMING_FOLDER_ID)

    drive = build('drive', 'v3', credentials=credentials)

    results = drive.files().list(
        q=f"'{INCOMING_FOLDER_ID}' in parents",
        fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Processing files')
        for item in items:
            handler_found = False
            for (regex, handler) in FILE_HANDLERS:
                if re.compile(regex).match(item['name']):
                    handler_found = True
                    print(f"{item['name']}: {handler.__name__}")

                    file = drive.files().get_media(fileId=item['id']).execute()
                    result = handler(file)

                    if result.get('move_to_directory'):
                        drive.files().update(
                            fileId=item['id'],
                            addParents=result['move_to_directory'],
                            removeParents=INCOMING_FOLDER_ID,
                        ).execute()

                    print(f"Handler completed with status {result['status']}.")
                    break
            if not handler_found:
                print(f"{item['name']}: No handler found.")
            print()


if __name__ == "__main__":
    main(sys.argv[1:])
