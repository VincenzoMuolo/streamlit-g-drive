import streamlit as st
import os
import logging
from g_drive_oauth import GoogleDriveService
from googleapiclient.http import MediaFileUpload

# Id della cartella, ottenibile dall'url, prendendo solo la parte finale, senza path
FOLDER_ID = st.secrets["google_drive_folder"]["folder-id"]

def getFileListFromGDrive():
    try:
        selected_fields = "files(id, name, webViewLink)"
        drive_service = GoogleDriveService().build()
        query = f"'{FOLDER_ID}' in parents"
        list_file = drive_service.files().list(q=query, fields=selected_fields).execute()
        return {"files": list_file.get("files", [])}
    except Exception as e:
        return {"error": str(e)}     

if __name__ == "__main__":   
    st.title("Streamlit - Google Drive API")

    # Metodo di caricamento file su drive
    st.subheader("Upload File su Google Drive")
    uploaded_file = st.file_uploader("Scegli un file", type=["csv", "png", "jpg", "pdf"])
    if uploaded_file is not None:
        st.write(f"Caricamento di: {uploaded_file.name}")
        
        # Salvataggio temporaneo
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Upload su Google Drive usando MediaFileUpload
        file_metadata = {
            "name": uploaded_file.name,
            "parents": [FOLDER_ID]
        }
        drive_service = GoogleDriveService().build()
        media = MediaFileUpload(uploaded_file.name, mimetype=uploaded_file.type)

        media_body = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id"
        ).execute()

        # Eliminare il file temporaneo dopo l'upload
        os.remove(uploaded_file.name)

        st.success(f"File caricato con successo! ID: {media_body['id']}")
    # Fine metodo di caricamento file su drive
    
    st.subheader("Lista File su Google Drive")
    if st.button("Visualizza File"):
        result = getFileListFromGDrive()
        if "error" in result:
            st.error(f"Errore: {result['error']}")
        else:
            files = result["files"]
            if not files:
                st.write("Nessun file presente nella cartella.")
            else:
                for file in files:
                    st.write(f"[]{file['name']} - [Apri]({file['webViewLink']})")
