import os

from dotenv import load_dotenv
from twilio.rest import Client

# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================
load_dotenv()


# ============================================================
# TWILIO CONFIGURATION - GET .ENV FILES access
# ============================================================
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_API_KEY_SID = os.getenv("TWILIO_API_KEY_SID")
TWILIO_API_SECRET = os.getenv("TWILIO_API_SECRET")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")


# ============================================================
# CREATE TWILIO CLIENT
# ============================================================
twilio_client = Client(
    TWILIO_API_KEY_SID,
    TWILIO_API_SECRET,
    TWILIO_ACCOUNT_SID
)


# ============================================================
# SEND SMS FUNCTION
# ============================================================
def send_sms(to_number, message):

    try:

        sms = twilio_client.messages.create(
            body=message,
            from_=TWILIO_FROM_NUMBER,
            to=to_number
        )

        print("========================================")
        print("( SMS )SENT SUCCESSFULLY")
        print("Message SID:", sms.sid)
        print("Message Status:", sms.status)
        print("Message Body:", sms.body)
        print("To:", to_number)
        print("Message:", message)
        print("========================================")


        # ========================================
        # CHECK SMS CURRENT STATUS
        # ========================================
        message_status = twilio_client.messages(sms.sid).fetch()
        print("========================================")
        print("CHECK SMS CURRENT STATUS")
        print("Message SID:", message_status.sid)
        print("To:", message_status.to)
        print("Message:", message_status.body)
        print("Status:", message_status.status)
        print("Error Code:", message_status.error_code)
        print("Error Message:", message_status.error_message)
        print("========================================")


        return True

    except Exception as e:

        print("========================================")
        print("SMS SENDING FAILED")
        print("To:", to_number)
        print("Error:", e)
        print("========================================")

        return False