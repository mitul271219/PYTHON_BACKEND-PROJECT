

import pandas as pd

from google_sheets import (
    patient_sheet,
    bpm_sheet,
    oxy_sheet
)

from services.bpm_service import check_bpm
from services.oxy_service import check_oxy


# ============================================================
# CHECK DEVICES
# ============================================================

def check_devices():

    print("\n")
    print("========================================")
    print("STARTING DAILY DEVICE CHECK")
    print("========================================")


    try:

        # ====================================================
        # GET DATA FROM GOOGLE SHEETS
        # ====================================================

        print("Fetching Patient data...")
        patients = patient_sheet.get_all_records()


        print("Fetching BPM data...")
        bpms = bpm_sheet.get_all_records()


        print("Fetching OXY data...")
        oxys = oxy_sheet.get_all_records()


        # ====================================================
        # CONVERT TO DATAFRAME
        # ====================================================

        patient_df = pd.DataFrame(
            patients
        )

        bpm_df = pd.DataFrame(
            bpms
        )

        oxy_df = pd.DataFrame(
            oxys
        )


        # ====================================================
        # CHECK BPM
        # ====================================================

        print("\n")
        print("STARTING BPM CHECK")

        check_bpm(
            patient_df,
            bpm_df
        )


        # ====================================================
        # CHECK OXY
        # ====================================================

        print("\n")
        print("STARTING OXY CHECK")

        check_oxy(
            patient_df,
            oxy_df
        )


        # ====================================================
        # SUCCESS
        # ====================================================

        print("\n")
        print("========================================")
        print("DAILY DEVICE CHECK COMPLETED")
        print("========================================")


        return {

            "success": True,

            "message":
                "BPM and OXY devices checked successfully"

        }


    except Exception as e:


        # ====================================================
        # ERROR
        # ====================================================

        print("\n")
        print("========================================")
        print("DEVICE CHECK ERROR")
        print("========================================")


        print(
            "Error:",
            e
        )


        return {

            "success": False,

            "message": str(e)

        }