


import os

import gspread

from google.oauth2.service_account import Credentials


# ============================================================
# GOOGLE SHEETS SCOPES
# ============================================================

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


# ============================================================
# GOOGLE CREDENTIALS
# ============================================================

CREDENTIALS_FILE = os.getenv(
    "GOOGLE_CREDENTIALS_FILE",
    "credentials.json"
)


creds = Credentials.from_service_account_file(
    CREDENTIALS_FILE,
    scopes=SCOPES
)


# ============================================================
# GOOGLE SHEETS CLIENT
# ============================================================

client = gspread.authorize(creds)


# ============================================================
# OPEN SPREADSHEETS ONCE
# ============================================================

patient_spreadsheet = client.open(
    "Patient Database"
)

monitor_spreadsheet = client.open(
    "Moniter_BPM_OXY"
)

oxy_spreadsheet = client.open(
    "Moniter_OXY"
)


# ============================================================
# WORKSHEETS
# ============================================================

patient_sheet = patient_spreadsheet.worksheet(
    "PatientSheet"
)

bpm_sheet = monitor_spreadsheet.worksheet(
    "BpmSheet"
)

oxy_sheet = oxy_spreadsheet.worksheet(
    "OxySheet"
)

