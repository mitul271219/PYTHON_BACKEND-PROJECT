

# improve and fast code , 


from datetime import datetime

import pandas as pd

from services.sms_service import send_sms
from utils.phone_utils import format_mobile_number


def check_bpm(patient_df, bpm_df):

    print("\n========================================")
    print("CHECKING BPM DEVICES")
    print("========================================")

    required_bpm_columns = [
        "patient_id",
        "bpm_mac_id",
        "reading_date"
    ]

    bpm_df = bpm_df[
        required_bpm_columns
    ].copy()

    bpm_df["reading_date"] = pd.to_datetime(
        bpm_df["reading_date"],
        format="%m/%d/%Y %I:%M:%S %p",
        errors="coerce"
    )

    bpm_df = bpm_df.dropna(
        subset=["reading_date"]
    )

    bpm_df = (
        bpm_df
        .sort_values(
            "reading_date",
            ascending=False
        )
        .drop_duplicates(
            subset=["patient_id"],
            keep="first"
        )
    )

    print("\nLATEST BPM READINGS")
    print("========================================")

    print(
        bpm_df[
            [
                "patient_id",
                "bpm_mac_id",
                "reading_date"
            ]
        ].to_string(index=False)
    )

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

    current_time = datetime.now()

    for row in bpm_merge.itertuples(index=False):

        patient_name = str(
            getattr(row, "First", "")
        ).strip()

        mobile = format_mobile_number(
            getattr(row, "Mobile", None)
        )

        reading_date = getattr(
            row,
            "reading_date",
            None
        )

        if pd.isna(reading_date):

            print(
                f"{patient_name} - BPM reading not available"
            )

            continue

        diff_seconds = (
            current_time - reading_date
        ).total_seconds()

        print("----------------------------------------")

        print(
            f"Patient: {patient_name}"
        )

        print(
            f"Mobile: {mobile}"
        )

        print(
            f"BPM Reading Time: {reading_date}"
        )

        print(
            f"Reading Age: {round(diff_seconds)} seconds"
        )

        if diff_seconds >= 300:

            message = "Please check your BP"

            print(
                f"{patient_name} BPM STATUS: {message}"
            )

        else:

            message = "BPM STATUS: READING IS RECENT"

            print(
                f"{patient_name} BPM STATUS: {message}"
            )

        if mobile:

            send_sms(
                mobile,
                message
            )

        else:

            print(
                f"Mobile number not available for {patient_name}"
            )

        print("----------------------------------------")