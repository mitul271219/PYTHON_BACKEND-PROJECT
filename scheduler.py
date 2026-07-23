
# from datetime import datetime
# import time


# def check_devices(sheet, doctor_sheet, doctor_sheet_oxy):

#     while True:

#         patients = sheet.get_all_records()
#         bpms = doctor_sheet.get_all_records()
#         oxys = doctor_sheet_oxy.get_all_records()

#         for patient in patients:

#             patient_id = patient.get("Patient Num")

#             bpm_mac = patient.get("bpm_mac_id")
#             pox_mac = patient.get("pox_mac_id")

       
#             # BPM CHECK
#             if bpm_mac:

#                 bpm = next(

#                     (
#                         x for x in bpms
#                         if x.get("patient_id") == patient_id
#                         and x.get("bpm_mac_id") == bpm_mac
#                     ),

#                     None

#                 )

#                 if bpm:

#                     reading = bpm.get("reading_date")

#                     if reading:

#                         reading_time = datetime.strptime(
#                             reading,
#                             "%m/%d/%Y %I:%M:%S %p"
#                         )

#                         diff = datetime.now() - reading_time

#                         if diff.total_seconds() >= 300:

#                             print(
#                                 patient["First"],
#                                 "Please check your BP."
#                             )

#                         else:

#                             print(
#                                 patient["First"],
#                                 "BP Reading is recent."
#                             )

    
#             # OXY CHECK
#             if pox_mac:

#                 oxy = next(

#                     (
#                         x for x in oxys
#                         if x.get("patient_id") == patient_id
#                         and x.get("pox_mac_id") == pox_mac
#                     ),

#                     None

#                 )

#                 if oxy:

#                     reading = oxy.get("reading_date")

#                     if reading:

#                         reading_time = datetime.strptime(
#                             reading,
#                             "%m/%d/%Y %I:%M:%S %p"
#                         )

#                         diff = datetime.now() - reading_time

#                         if diff.total_seconds() >= 300:

#                             print(
#                                 patient["First"],
#                                 "Please check your POX Monitor."
#                             )

#                         else:

#                             print(
#                                 patient["First"],
#                                 "POX Reading is recent."
#                             )

#         time.sleep(60)







# from datetime import datetime
# import pandas as pd
# import numpy as np
# import time


# def check_devices(sheet, doctor_sheet, doctor_sheet_oxy):

#     while True:

#         # -----------------------------
#         # Read Google Sheet Data
#         # -----------------------------
#         patients = sheet.get_all_records()
#         # print(patients)
#         bpms = doctor_sheet.get_all_records()
#         oxys = doctor_sheet_oxy.get_all_records()

#         # -----------------------------
#         # Convert to DataFrame
#         # -----------------------------
#         patient_df = pd.DataFrame(patients)
#         # print(patient_df) pd.DataFrame is convertin into excel formet data
#         bpm_df = pd.DataFrame(bpms)
#         oxy_df = pd.DataFrame(oxys)

#         # =====================================================
#         # BPM
#         # =====================================================

#         bpm_merge = patient_df.merge(
#             bpm_df,
#             how="left",
#             left_on=["Patient Num", "bpm_mac_id"],
#             right_on=["patient_id", "bpm_mac_id"]
#         )   
#         # print(bpm_merge )

#         bpm_merge["reading_date"] = pd.to_datetime(
#             bpm_merge["reading_date"],
#             format="%m/%d/%Y %I:%M:%S %p",
#             errors="coerce"
#         ) # string date and time convert into Timestamp('2026-07-17 19:30:00')
#         # print(type(bpm_merge["reading_date"][0]))
    
    

#         bpm_merge["diff_seconds"] = (
#             datetime.now() - bpm_merge["reading_date"]
#         ).dt.total_seconds()
#         # print(bpm_merge["diff_seconds"])

#         bpm_merge["message"] = np.where(
#             bpm_merge["diff_seconds"] >= 300,
#             "Please check your BP.",
#             "BP Reading is recent."
#         )

#         # =====================================================
#         # OXY
#         # =====================================================

#         oxy_merge = patient_df.merge(
#             oxy_df,
#             how="left",
#             left_on=["Patient Num", "pox_mac_id"],
#             right_on=["patient_id", "pox_mac_id"]
#         )

#         oxy_merge["reading_date"] = pd.to_datetime(
#             oxy_merge["reading_date"],
#             format="%m/%d/%Y %I:%M:%S %p",
#             errors="coerce"
#         )

#         oxy_merge["diff_seconds"] = (
#             datetime.now() - oxy_merge["reading_date"]
#         ).dt.total_seconds()

#         oxy_merge["message"] = np.where(
#             oxy_merge["diff_seconds"] >= 300,
#             "Please check your POX Monitor.",
#             "POX Reading is recent."
#         )

#         # =====================================================
#         # Print BPM Result
#         # =====================================================

#         for _, row in bpm_merge.iterrows():
#             # print(row)

#             if pd.notna(row["reading_date"]):

#                 print(row["First"], "-", row["message"])

#         # =====================================================
#         # Print OXY Result
#         # =====================================================

#         for _, row in oxy_merge.iterrows():

#             if pd.notna(row["reading_date"]):

#                 print(row["First"], "-", row["message"])

#         print("========================================")

#         time.sleep(60)













from datetime import datetime
import pandas as pd
import time
import os

from twilio.rest import Client
from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================
load_dotenv()


# ============================================================
# TWILIO CONFIGURATION - GET .ENV FILES access
# ============================================================
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_API_KEY_SID = os.getenv("TWILIO_API_KEY_SID")
TWILIO_API_SECRET = os.getenv("TWILIO_API_SECRET")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")


# ============================================================
# CREATE TWILIO CLIENT
# ============================================================
twilio_client = Client(
    TWILIO_API_KEY_SID,
    TWILIO_API_SECRET,
    TWILIO_ACCOUNT_SID
)


# ============================================================
# SEND SMS FUNCTION
# ============================================================
def send_sms(to_number, message):

    try:

        # sms = twilio_client.messages.create(
        #     body=message,
        #     from_=TWILIO_FROM_NUMBER,
        #     to=to_number
        # )

        # print("========================================")
        # print("( SMS )SENT SUCCESSFULLY")
        # print("Message SID:", sms.sid)
        # print("Message Status:", sms.status)
        # print("Message Body:", sms.body)
        # print("To:", to_number)
        # print("Message:", message)
        # print("========================================")


        # ========================================
        # CHECK SMS CURRENT STATUS
        # ========================================
        message_status = twilio_client.messages("SM5a879bcc6ec651314a73934e039816e5").fetch()
        print("========================================")
        print("CHECK SMS CURRENT STATUS")
        print("Message SID:", message_status.sid)
        print("To:", message_status.to)
        print("Message:", message_status.body)
        print("Status:", message_status.status)
        print("Error Code:", message_status.error_code)
        print("Error Message:", message_status.error_message)
        print("========================================")


        return True

    except Exception as e:

        print("========================================")
        print("SMS SENDING FAILED")
        print("To:", to_number)
        print("Error:", e)
        print("========================================")

        return False


# ============================================================
# FORMAT MOBILE NUMBER
# ============================================================
def format_mobile_number(mobile):

    if mobile is None:
        return None

    mobile = str(mobile).strip()  #strip() removing extra spaces.

    # Empty mobile number
    if not mobile:
        return None

    # Remove .0 if Google Sheet returns number as float
    # Example:
    # 15005550006.0
    # Convert to:
    # 15005550006
    if mobile.endswith(".0"):
        mobile = mobile[:-2]

    # Add + if number does not have it
    if not mobile.startswith("+"):
        mobile = "+1" + mobile
        print("mobieNUMBER "+mobile)

    return mobile


# ============================================================
# CHECK DEVICES
# ============================================================
def check_devices(sheet, doctor_sheet, doctor_sheet_oxy):

    print("========================================")
    print("DEVICE SCHEDULER STARTED")
    print("========================================")


    # ========================================================
    # CONTINUOUS LOOP
    # ========================================================

    while True:

        try:

            print("\n")
            print("========================================")
            print("CHECKING DEVICES")
            print("Current Time:", datetime.now())
            print("========================================")


            # ====================================================
            # GET PATIENT DATA
            # ====================================================
            patients = sheet.get_all_records()

            # ====================================================
            # GET BPM DATA
            # ====================================================
            bpms = doctor_sheet.get_all_records()

            # ====================================================
            # GET OXY DATA
            # ====================================================
            oxys = doctor_sheet_oxy.get_all_records()


            # ====================================================
            # CONVERT DATA TO DATAFRAME
            # ====================================================
            patient_df = pd.DataFrame(patients)
            # print(patient_df) pd.DataFrame is convertin into excel table format data
            bpm_df = pd.DataFrame(bpms)
            oxy_df = pd.DataFrame(oxys)


            # ====================================================
            # BPM SECTION
            # ====================================================
            print("\n")
            print("========================================")
            print("CHECKING BPM DEVICES")
            print("========================================")


            # ----------------------------------------------------
            # MERGE PATIENT SHEET WITH BPM SHEET
            # ----------------------------------------------------
            bpm_merge = patient_df.merge(
                bpm_df,
                how="left",
                left_on=["Patient Num","bpm_mac_id"],
                right_on=["patient_id","bpm_mac_id" ]
            )


            # ----------------------------------------------------
            # CONVERT BPM READING DATE
            # ----------------------------------------------------
            bpm_merge["reading_date"] = pd.to_datetime(
                bpm_merge["reading_date"],
                format="%m/%d/%Y %I:%M:%S %p",
                errors="coerce"
            )
             # string date and time convert into (datetime object) Timestamp('2026-07-17 19:30:00')


            # ----------------------------------------------------
            # CALCULATE BPM READING AGE
            # ----------------------------------------------------
            bpm_merge["diff_seconds"] = (
                datetime.now() - bpm_merge["reading_date"]
            ).dt.total_seconds()


            #         oxy_merge["message"] = np.where(
            #             oxy_merge["diff_seconds"] >= 300,
            #             "Please check your POX Monitor.",
            #             "POX Reading is recent."
            #         )


            # ----------------------------------------------------
            # LOOP THROUGH BPM PATIENTS
            # ----------------------------------------------------
            for _, row in bpm_merge.iterrows():
                # print(row)

                # ----------------------------------------------
                # GET PATIENT NAME
                # ----------------------------------------------
                patient_name = str(
                    row.get("First", "")
                ).strip()

                # ----------------------------------------------
                # GET MOBILE NUMBER
                # ----------------------------------------------
                mobile = format_mobile_number(
                    row.get("Mobile")
                )

                # ----------------------------------------------
                # GET READING DATE
                # ----------------------------------------------
                reading_date = row.get(
                    "reading_date"
                )

                # ----------------------------------------------
                # GET DIFFERENCE IN SECONDS
                # ----------------------------------------------
                diff_seconds = row.get(
                    "diff_seconds"
                )

                # ----------------------------------------------
                # CHECK IF READING EXISTS
                # ----------------------------------------------
                if pd.isna(reading_date):   # (NaT) ya (NaN) 
                    print(
                        patient_name,
                        "- BPM reading not available"
                    )

                    continue


                # ----------------------------------------------
                # PRINT READING INFORMATION
                # ----------------------------------------------
                print(
                    "Patient:",
                    patient_name
                )

                print(
                    "Mobile:",
                    mobile
                )

                print(
                    "BPM Reading Time:",
                    reading_date
                )

                print(
                    "Reading Age:",
                    round(diff_seconds),
                    "seconds"
                )


                # =================================================
                # BPM STATUS
                # =================================================
                if diff_seconds >= 300:

                    # --------------------------------------------
                    # BPM OLD READING
                    # --------------------------------------------
                    message = "Please check your BP"
                    print(
                        patient_name + " BPM STATUS:",
                        message
                    )


                else:

                    # --------------------------------------------
                    # BPM RECENT READING
                    # --------------------------------------------
                    message = "BPM STATUS: READING IS RECENT"
                    print(
                        patient_name + " BPM STATUS:",
                        message
                    )


                # =================================================
                # SEND BPM SMS
                # =================================================

                if mobile:

                    send_sms(
                        mobile,
                        message
                    )

                else:

                    print(
                        "Mobile number not available for",
                        patient_name
                    )


                print("----------------------------------------")


            # ====================================================
            # OXY SECTION
            # ====================================================
            print("\n")
            print("========================================")
            print("CHECKING OXY DEVICES")
            print("========================================")


            # ----------------------------------------------------
            # MERGE PATIENT SHEET WITH OXY SHEET
            # ----------------------------------------------------
            oxy_merge = patient_df.merge(
                oxy_df,
                how="left",
                left_on=[
                    "Patient Num",
                    "pox_mac_id"
                ],
                right_on=[
                    "patient_id",
                    "pox_mac_id"
                ]
            )


            # ----------------------------------------------------
            # CONVERT OXY READING DATE
            # ----------------------------------------------------
            oxy_merge["reading_date"] = pd.to_datetime(
                oxy_merge["reading_date"],
                format="%m/%d/%Y %I:%M:%S %p",
                errors="coerce"
            )


            # ----------------------------------------------------
            # CALCULATE OXY READING AGE
            # ----------------------------------------------------
            oxy_merge["diff_seconds"] = (
                datetime.now()
                - oxy_merge["reading_date"]
            ).dt.total_seconds()


            # ----------------------------------------------------
            # LOOP THROUGH OXY PATIENTS
            # ----------------------------------------------------
            for _, row in oxy_merge.iterrows():

                # ----------------------------------------------
                # GET PATIENT NAME
                # ----------------------------------------------
                patient_name = str(
                    row.get("First", "")
                ).strip()


                # ----------------------------------------------
                # GET MOBILE NUMBER
                # ----------------------------------------------
                mobile = format_mobile_number(
                    row.get("Mobile")
                )


                # ----------------------------------------------
                # GET READING DATE
                # ----------------------------------------------
                reading_date = row.get(
                    "reading_date"
                )


                # ----------------------------------------------
                # GET DIFFERENCE IN SECONDS
                # ----------------------------------------------
                diff_seconds = row.get(
                    "diff_seconds"
                )


                # ----------------------------------------------
                # CHECK IF READING EXISTS
                # ----------------------------------------------
                if pd.isna(reading_date):
                    print(
                        patient_name,
                        "- OXY reading not available"
                    )

                    continue


                # ----------------------------------------------
                # PRINT READING INFORMATION
                # ----------------------------------------------
                print(
                    "Patient:",
                    patient_name
                )

                print(
                    "Mobile:",
                    mobile
                )

                print(
                    "OXY Reading Time:",
                    reading_date
                )

                print(
                    "Reading Age:",
                    round(diff_seconds),
                    "seconds"
                )


                # =================================================
                # OXY STATUS
                # =================================================
                if diff_seconds >= 300:

                    # --------------------------------------------
                    # OXY OLD READING
                    # --------------------------------------------
                    message = "Please check your POX Monitor"
                    print(
                        "OXY STATUS:",
                        message
                    )


                else:

                    # --------------------------------------------
                    # OXY RECENT READING
                    # --------------------------------------------
                    message = "OXY STATUS: READING IS RECENT"
                    print(
                        "OXY STATUS:",
                        message
                    )


                # =================================================
                # SEND OXY SMS
                # =================================================
                if mobile:

                    send_sms(
                        mobile,
                        message
                    )

                else:

                    print(
                        "Mobile number not available for",
                        patient_name
                    )

                print("----------------------------------------")


            # ====================================================
            # WAIT 60 SECONDS
            # ====================================================
            print("\n")
            print("========================================")
            print("CHECK COMPLETED")
            print("NEXT CHECK AFTER 60 SECONDS")
            print("========================================")

            time.sleep(60)


        # ========================================================
        # HANDLE ERROR
        # ========================================================
        except Exception as e:

            print("\n")
            print("========================================")
            print("SCHEDULER ERROR")
            print("========================================")

            print(
                "Error:",
                e
            )

            print(
                "Retrying after 60 seconds..."
            )


            time.sleep(60)









