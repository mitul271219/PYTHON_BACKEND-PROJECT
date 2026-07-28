






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
    print("CHECKING DEVICES")
    print("========================================")


    try:

        # ====================================================
        # GET PATIENT DATA
        # ====================================================
        patients = patient_sheet.get_all_records()

        # ====================================================
        # GET BPM DATA
        # ====================================================
        bpms = bpm_sheet.get_all_records()

        # ====================================================
        # GET OXY DATA
        # ====================================================
        oxys = oxy_sheet.get_all_records()

        # ====================================================
        # CONVERT DATA TO DATAFRAME
        # ====================================================
        patient_df = pd.DataFrame(patients)
        bpm_df = pd.DataFrame(bpms)
        oxy_df = pd.DataFrame(oxys)
        # print(patient_df) pd.DataFrame is convertin into excel table format data

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
        print("DEVICE CHECK COMPLETED")
        print("========================================")


        return {

            "success": True,

            "message": "BPM and OXY devices checked successfully"

        }


    except Exception as e:

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