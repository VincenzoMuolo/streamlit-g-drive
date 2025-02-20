import os
import tomllib

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

class GoogleDriveService:
    def __init__(self):
        self._SCOPES = ['https://www.googleapis.com/auth/drive']

        # Ottieni la directory corrente del file Python
        _base_path = os.path.dirname(__file__)  
        
        # Percorso corretto del file secrets.toml nella stessa directory del file Python
        _secrets_path = os.path.join(_base_path, ".streamlit", "secrets.toml")  

        # Apri il file TOML correttamente
        with open(_secrets_path, "rb") as f:
            secrets = tomllib.load(f)  

        # Salva le credenziali
        self._credentials_dict = secrets["google_drive_API_service_account"]  

    def build(self):
        creds = ServiceAccountCredentials.from_json_keyfile_dict(self._credentials_dict, self._SCOPES)
        service = build('drive', 'v3', credentials=creds)

        return service
