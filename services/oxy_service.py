



from datetime import datetime

import pandas as pd

from services.sms_service import send_sms
from utils.phone_utils import format_mobile_number


# ============================================================
# CONSTANT
# ============================================================
# 24 hours = 24 × 60 × 60 seconds
ONE_DAY_SECONDS = 86400


# ============================================================
# CHECK OXY DEVICES
# ============================================================
def check_oxy(patient_df, oxy_df):

    print("\n========================================")
    print("CHECKING OXY DEVICES")
    print("========================================")


    # ========================================================
    # REQUIRED COLUMNS
    # ========================================================

    required_oxy_columns = [
        "patient_id",
        "pox_mac_id",
        "reading_date"
    ]


    # ========================================================
    # CHECK REQUIRED COLUMNS
    # ========================================================

    missing_columns = [
        column
        for column in required_oxy_columns
        if column not in oxy_df.columns
    ]


    if missing_columns:

        print(
            "OXY missing columns:",
            missing_columns
        )

        return


    # ========================================================
    # SELECT ONLY REQUIRED COLUMNS
    # ========================================================

    oxy_df = oxy_df[
        required_oxy_columns
    ].copy()


    # ========================================================
    # CONVERT READING DATE
    # ========================================================

    oxy_df["reading_date"] = pd.to_datetime(
        oxy_df["reading_date"],
        format="%m/%d/%Y %I:%M:%S %p",
        errors="coerce"
    )


    # ========================================================
    # REMOVE INVALID DATES
    # ========================================================

    oxy_df = oxy_df.dropna(
        subset=["reading_date"]
    )


    # ========================================================
    # GET LATEST READING
    # ========================================================

    oxy_df = (
        oxy_df
        .sort_values(
            "reading_date",
            ascending=False
        )
        .drop_duplicates(
            subset=[
                "patient_id",
                "pox_mac_id"
            ],
            keep="first"
        )
    )


    # ========================================================
    # MERGE PATIENT + OXY DATA
    # ========================================================

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


    # ========================================================
    # CURRENT TIME
    # ========================================================

    current_time = datetime.now()


    # ========================================================
    # CHECK EACH PATIENT
    # ========================================================

    for row in oxy_merge.itertuples(
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
                f"OXY reading not available"
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
            f"OXY Reading: {reading_date}"
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
                "Please check your POX Monitor"
            )


            print(
                f"{patient_name} - "
                f"OXY ALERT: "
                f"Reading older than 24 hours"
                f"Please check your POX Monitor"
            )


            # =================================================
            # SEND SMS
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
                f"OXY STATUS: POX--READING IS RECENT"
            )


        print("----------------------------------------")