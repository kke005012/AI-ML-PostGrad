from google.oauth2 import service_account
from googleapiclient.discovery import build
import streamlit as st

# Authenticate with Google using service account info from secrets.toml
creds = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)

# Google Sheet ID (replace with yours or import from app.py if needed)
SPREADSHEET_ID = "1BomItCLK3VrduEhevlB7W-B0btpL_xUDI092J1x26P8"
SHEET_NAME = "Sheet1"

def append_log_to_sheet(log_entry: dict):
    """Append a dictionary log entry to the Google Sheet."""
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    
    # Ensure consistent order
    row = [
        log_entry.get("timestamp", ""),
        log_entry.get("email", ""),
        log_entry.get("filename", ""),
        log_entry.get("row_count", ""),
        log_entry.get("charged", "")
    ]
    
    response = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!A1",
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body={"values": [row]},
    ).execute()

    return response
