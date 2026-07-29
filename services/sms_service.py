


import os

from dotenv import load_dotenv
from twilio.rest import Client


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# TWILIO CONFIGURATION
# ============================================================

TWILIO_ACCOUNT_SID = os.getenv(
    "TWILIO_ACCOUNT_SID"
)

TWILIO_API_KEY_SID = os.getenv(
    "TWILIO_API_KEY_SID"
)

TWILIO_API_SECRET = os.getenv(
    "TWILIO_API_SECRET"
)

TWILIO_FROM_NUMBER = os.getenv(
    "TWILIO_FROM_NUMBER"
)


# ============================================================
# CREATE TWILIO CLIENT ONCE
# ============================================================

twilio_client = Client(
    TWILIO_API_KEY_SID,
    TWILIO_API_SECRET,
    TWILIO_ACCOUNT_SID
)


# ============================================================
# SEND SMS
# ============================================================

def send_sms(to_number, message):

    if not to_number:
        print(
            "SMS NOT SENT: Mobile number is missing"
        )

        return False


    try:

        sms = twilio_client.messages.create(
            body=message,
            from_=TWILIO_FROM_NUMBER,
            to=to_number
        )


        print(
            f"SMS SENT | "
            f"To: {to_number} | "
            f"SID: {sms.sid} | "
            f"Status: {sms.status}"
        )


        return True


    except Exception as e:

        print(
            f"SMS FAILED | "
            f"To: {to_number} | "
            f"Error: {e}"
        )

        return False

