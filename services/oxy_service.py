from datetime import datetime

import pandas as pd

from services.sms_service import send_sms
from utils.phone_utils import format_mobile_number


def check_oxy(patient_df, oxy_df):
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
