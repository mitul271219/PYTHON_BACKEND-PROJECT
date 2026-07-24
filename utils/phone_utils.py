# ============================================================
# FORMAT MOBILE NUMBER
# ============================================================
def format_mobile_number(mobile):

    if mobile is None:
        return None

    mobile = str(mobile).strip()  #strip() removing extra spaces.

    # Empty mobile number
    if not mobile:
        return None

    # Remove .0 if Google Sheet returns number as float
    # Example:
    # 15005550006.0
    # Convert to:
    # 15005550006
    if mobile.endswith(".0"):
        mobile = mobile[:-2]

    # Add + if number does not have it
    if not mobile.startswith("+"):
        mobile = "+" + mobile
        # print("mobieNUMBER "+mobile)

    return mobile
