import os
import tomllib
import streamlit as st

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

class GoogleDriveService:
    def __init__(self):
        self._SCOPES = ['https://www.googleapis.com/auth/drive']

        # Accesso alle credenziali di accesso in locale
        #_base_path = os.path.dirname(__file__)  
        #_secrets_path = os.path.join(_base_path, ".streamlit", "secrets.toml")  
        #with open(_secrets_path, "rb") as f:
        #    secrets = tomllib.load(f)  
        #self._credentials_dict = secrets["google_drive_API_service_account"]  
        
        # Accesso alle credenziali da Streamlit cloud
        self._credentials_dict = st.secrets["google_drive_API_service_account"] 

    def build(self):
        creds = ServiceAccountCredentials.from_json_keyfile_dict(self._credentials_dict, self._SCOPES)
        service = build('drive', 'v3', credentials=creds)

        return service
