from flask import Flask
from flask_cors import CORS
import gspread
from flask import jsonify
from google.oauth2.service_account import Credentials

from threading import Thread
from scheduler import check_devices


app = Flask(__name__)
CORS(app)

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=scope
)


client = gspread.authorize(creds)

# Patient Spreadsheet
sheet = client.open("Patient Database").worksheet("PatientSheet")
# BPM Spreadsheet
doctor_sheet = client.open("Moniter_BPM_OXY").worksheet("BpmSheet")
# OXY Spreadsheet
doctor_sheet_oxy = client.open("Moniter_OXY").worksheet("OxySheet")


scheduler_thread = Thread(
    target=check_devices,
    args=(sheet, doctor_sheet, doctor_sheet_oxy),
    daemon=True
)

scheduler_thread.start()



@app.route("/")
def home():
    return "Python Backend Running Successfully"


# @app.route("/patients")
# def get_patients():
#     data = sheet.get_all_records()
#     return data
@app.route("/patients")
def get_patients():
    data = sheet.get_all_records()

    return jsonify({
        "success": True,
        "message": "Patients fetched GET successfully.",
        "count": len(data),
        "data": data
    })



@app.route("/bpm")
def get_doctors():
    data = doctor_sheet.get_all_records()

    return jsonify({
        "success": True,
        "message": "Doctors fetched successfully.",
        "count": len(data),
        "data": data
    })


@app.route("/oxy")
def get_doctors_oxy():
    data = doctor_sheet_oxy .get_all_records()

    return jsonify({
        "success": True,
        "message": "Oxy_Sheet fetched successfully.",
        "count": len(data),
        "data": data
    })


if __name__ == "__main__":
    app.run(debug=True)