


from datetime import datetime

import pandas as pd

from services.sms_service import send_sms
from utils.phone_utils import format_mobile_number


# ============================================================
# CONSTANT
# ============================================================

ONE_DAY_SECONDS = 300


# ============================================================
# CHECK BPM DEVICES
# ============================================================

def check_bpm(patient_df, bpm_df):

    print("\n========================================")
    print("CHECKING BPM DEVICES")
    print("========================================")


    # ========================================================
    # REQUIRED COLUMNS
    # ========================================================

    required_bpm_columns = [
        "patient_id",
        "bpm_mac_id",
        "reading_date"
    ]


    # ========================================================
    # CHECK REQUIRED COLUMNS
    # ========================================================

    missing_columns = [
        column
        for column in required_bpm_columns
        if column not in bpm_df.columns
    ]


    if missing_columns:

        print(
            "BPM missing columns:",
            missing_columns
        )

        return


    # ========================================================
    # SELECT ONLY REQUIRED COLUMNS
    # ========================================================

    bpm_df = bpm_df[
        required_bpm_columns
    ].copy()


    # ========================================================
    # CONVERT READING DATE
    # ========================================================

    bpm_df["reading_date"] = pd.to_datetime(
        bpm_df["reading_date"],
        format="%m/%d/%Y %I:%M:%S %p",
        errors="coerce"
    )


    # ========================================================
    # REMOVE INVALID DATES
    # ========================================================

    bpm_df = bpm_df.dropna(
        subset=["reading_date"]
    )


    # ========================================================
    # GET LATEST READING FOR EACH PATIENT
    # ========================================================

    bpm_df = (
        bpm_df
        .sort_values(
            "reading_date",
            ascending=False
        )
        .drop_duplicates(
            subset=[
                "patient_id",
                "bpm_mac_id"
            ],
            keep="first"
        )
    )


    # ========================================================
    # MERGE PATIENT + BPM DATA
    # ========================================================

    bpm_merge = patient_df.merge(

        bpm_df,

        how="left",

        left_on=[
            "Patient Num",
            "bpm_mac_id"
        ],

        right_on=[
            "patient_id",
            "bpm_mac_id"
        ]
    )


    # ========================================================
    # CURRENT TIME
    # ========================================================

    current_time = datetime.now()


    # ========================================================
    # CHECK EACH PATIENT
    # ========================================================

    for row in bpm_merge.itertuples(
        index=False
    ):


        patient_name = str(
            getattr(
                row,
                "First",
                ""
            )
        ).strip()


        mobile = format_mobile_number(
            getattr(
                row,
                "Mobile",
                None
            )
        )


        reading_date = getattr(
            row,
            "reading_date",
            None
        )


        # ====================================================
        # NO READING
        # ====================================================

        if pd.isna(reading_date):

            print(
                f"{patient_name} - "
                f"BPM reading not available"
            )

            continue


        # ====================================================
        # CALCULATE READING AGE
        # ====================================================

        diff_seconds = (
            current_time - reading_date
        ).total_seconds()


        reading_age_hours = (
            diff_seconds / 3600
        )


        print("----------------------------------------")

        print(
            f"Patient: {patient_name}"
        )

        print(
            f"BPM Reading: {reading_date}"
        )

        print(
            f"Reading Age: "
            f"{reading_age_hours:.2f} hours"
        )


        # ====================================================
        # 24 HOURS CHECK
        # ====================================================

        if diff_seconds >= ONE_DAY_SECONDS:


            message = (
                "Please check your BP"
            )


            print(
                f"{patient_name} - "
                f"BPM ALERT: "
                f"Reading older than 24 hours"
                f"Please check your BP"
            )


            # =================================================
            # SEND SMS ONLY IF MOBILE EXISTS
            # =================================================

            if mobile:

                send_sms(
                    mobile,
                    message
                )

            else:

                print(
                    f"Mobile number not available "
                    f"for {patient_name}"
                )


        else:


            # =================================================
            # RECENT READING
            # NO SMS
            # =================================================

            print(
                f"{patient_name} - "
                f"BPM STATUS: BPM--READING IS RECENT "
            )


        print("----------------------------------------")

