import gspread

from google.oauth2.service_account import Credentials


# ============================================================
# GOOGLE SHEETS SCOPES
# ============================================================
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


# ============================================================
# GOOGLE CREDENTIALS
# ============================================================
creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=scope
)


# ============================================================
# GOOGLE SHEETS CLIENT
# ============================================================
client = gspread.authorize(creds)


# ============================================================
# PATIENT SHEET
# ============================================================
patient_sheet = client.open("Patient Database").worksheet("PatientSheet")

# ============================================================
# BPM SHEET
# ============================================================
bpm_sheet = client.open("Moniter_BPM_OXY").worksheet("BpmSheet")

# ============================================================
# OXY SHEET
# ============================================================
oxy_sheet = client.open("Moniter_OXY").worksheet("OxySheet")