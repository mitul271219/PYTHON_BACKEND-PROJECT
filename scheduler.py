

import time
import pandas as pd

from services.bpm_service import check_bpm
from services.oxy_service import check_oxy



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


            # ================================================
            # CHECK BPM DEVICES
            # ================================================
            check_bpm(
                patient_df,
                bpm_df
            )


            # ================================================
            # CHECK OXY DEVICES
            # ================================================
            check_oxy(
                patient_df,
                oxy_df
            )




            # ================================================
            # WAIT 60 SECONDS
            # ================================================

            print("\n")
            print("========================================")
            print("CHECK COMPLETED")
            print("NEXT CHECK AFTER 60 SECONDS")
            print("========================================")


            time.sleep(60)


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