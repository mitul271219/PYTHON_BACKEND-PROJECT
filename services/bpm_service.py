from datetime import datetime

import pandas as pd

from services.sms_service import send_sms
from utils.phone_utils import format_mobile_number

def check_bpm(patient_df, bpm_df):
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
        patient_name = str(row.get("First", "")).strip()

        # ----------------------------------------------
        # GET MOBILE NUMBER
        # ----------------------------------------------
        mobile = format_mobile_number(row.get("Mobile"))

        # ----------------------------------------------
        # GET READING DATE
        # ----------------------------------------------
        reading_date = row.get("reading_date")

        # ----------------------------------------------
        # GET DIFFERENCE IN SECONDS
        # ----------------------------------------------
        diff_seconds = row.get("diff_seconds")

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
        print("Patient:",patient_name)

        print("Mobile:",mobile)

        print("BPM Reading Time:",reading_date)

        print("Reading Age:",round(diff_seconds),"seconds")


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
