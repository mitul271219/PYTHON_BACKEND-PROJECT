

# improve and fast code ,

from datetime import datetime

import pandas as pd

from services.sms_service import send_sms
from utils.phone_utils import format_mobile_number


def check_oxy(patient_df, oxy_df):

    print("\n========================================")
    print("CHECKING OXY DEVICES")
    print("========================================")

    required_oxy_columns = [
        "patient_id",
        "pox_mac_id",
        "reading_date"
    ]

    oxy_df = oxy_df[
        required_oxy_columns
    ].copy()

    oxy_df["reading_date"] = pd.to_datetime(
        oxy_df["reading_date"],
        format="%m/%d/%Y %I:%M:%S %p",
        errors="coerce"
    )

    oxy_df = oxy_df.dropna(
        subset=["reading_date"]
    )

    oxy_df = (
        oxy_df
        .sort_values(
            "reading_date",
            ascending=False
        )
        .drop_duplicates(
            subset=["patient_id"],
            keep="first"
        )
    )

    print("\nLATEST OXY READINGS")
    print("========================================")

    print(
        oxy_df[
            [
                "patient_id",
                "pox_mac_id",
                "reading_date"
            ]
        ].to_string(index=False)
    )

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

    current_time = datetime.now()

    for row in oxy_merge.itertuples(index=False):

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
                f"{patient_name} - OXY reading not available"
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
            f"OXY Reading Time: {reading_date}"
        )

        print(
            f"Reading Age: {round(diff_seconds)} seconds"
        )

        if diff_seconds >= 300:

            message = "Please check your POX Monitor"

            print(
                f"{patient_name} OXY STATUS: {message}"
            )

        else:

            message = "OXY STATUS: READING IS RECENT"

            print(
                f"{patient_name} OXY STATUS: {message}"
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










# from datetime import datetime

# import pandas as pd

# from services.sms_service import send_sms
# from utils.phone_utils import format_mobile_number

# def check_oxy(patient_df, oxy_df):

# print("\n========================================")
# print("CHECKING OXY DEVICES")
# print("========================================")

# required_oxy_columns = [
#     "patient_id",
#     "pox_mac_id",
#     "reading_date"
# ]

# oxy_df = oxy_df[
#     required_oxy_columns
# ].copy()

# oxy_df["reading_date"] = pd.to_datetime(
#     oxy_df["reading_date"],
#     format="%m/%d/%Y %I:%M:%S %p",
#     errors="coerce"
# )

# oxy_df = oxy_df.dropna(
#     subset=["reading_date"]
# )

# oxy_df = (
#     oxy_df
#     .sort_values(
#         "reading_date",
#         ascending=False
#     )
#     .drop_duplicates(
#         subset=["patient_id"],
#         keep="first"
#     )
# )

# print("\nLATEST OXY READINGS")
# print("========================================")

# print(
#     oxy_df[
#         [
#             "patient_id",
#             "pox_mac_id",
#             "reading_date"
#         ]
#     ].to_string(index=False)
# )

# oxy_merge = patient_df.merge(
#     oxy_df,
#     how="left",
#     left_on=[
#         "Patient Num",
#         "pox_mac_id"
#     ],
#     right_on=[
#         "patient_id",
#         "pox_mac_id"
#     ]
# )

# current_time = datetime.now()

# for row in oxy_merge.itertuples(index=False):

#     patient_name = str(
#         getattr(row, "First", "")
#     ).strip()

#     mobile = format_mobile_number(
#         getattr(row, "Mobile", None)
#     )

#     reading_date = getattr(
#         row,
#         "reading_date",
#         None
#     )

#     if pd.isna(reading_date):

#         print(
#             f"{patient_name} - OXY reading not available"
#         )

#         continue

#     diff_seconds = (
#         current_time - reading_date
#     ).total_seconds()

#     print("----------------------------------------")

#     print(
#         f"Patient: {patient_name}"
#     )

#     print(
#         f"Mobile: {mobile}"
#     )

#     print(
#         f"OXY Reading Time: {reading_date}"
#     )

#     print(
#         f"Reading Age: {round(diff_seconds)} seconds"
#     )

#     if diff_seconds >= 300:

#         message = "Please check your POX Monitor"

#         print(
#             f"{patient_name} OXY STATUS: {message}"
#         )

#     else:

#         message = "OXY STATUS: READING IS RECENT"

#         print(
#             f"{patient_name} OXY STATUS: {message}"
#         )

#     if mobile:

#         send_sms(
#             mobile,
#             message
#         )

#     else:

#         print(
#             f"Mobile number not available for {patient_name}"
#         )

#     print("----------------------------------------")