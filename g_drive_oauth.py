
import os
import tomllib

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

class GoogleDriveService:
    def __init__(self):
        self._SCOPES=['https://www.googleapis.com/auth/drive']

        _base_path = os.path.dirname(__file__)
        _secrets_path=os.path.join(_base_path+"/.streamlit/", 'secrets.toml')
        
        secrets = tomllib.load(_secrets_path)  
        self._credentials_dict = secrets["google_drive_API_service_account"]  # Già un dizionario valido

    def build(self):
        creds = ServiceAccountCredentials.from_json_keyfile_dict(self._credentials_dict, self._SCOPES)
        service = build('drive', 'v3', credentials=creds)

        return service
