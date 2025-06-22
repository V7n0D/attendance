import os
import gspread
from google.oauth2.service_account import Credentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive',
        ]


def get_client():
    """Returns the authenticated gspread client."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    creds_path = os.path.join(base_dir, 'google_sheets_credentials.json')
    creds = Credentials.from_service_account_file(
        creds_path, 
        scopes=SCOPES
    )

    client = gspread.authorize(creds)
    return client, creds
