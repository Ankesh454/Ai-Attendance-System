import requests
import random
import streamlit as st


def send_otp(phone_number):

    otp = str(random.randint(100000, 999999))

    url = "https://www.fast2sms.com/dev/bulkV2"

    payload = {
        "route": "q",
        "message": f"Your SnapShot Class password reset OTP is {otp}. Do not share this OTP.",
        "language": "english",
        "flash": 0,
        "numbers": phone_number
    }

    headers = {
        "authorization": st.secrets["FAST2SMS_API_KEY"],
        "Content-Type": "application/json"
    }

    try:

        response = requests.post(
            url,
            json=payload,
            headers=headers
        )

        result = response.json()

        print("FAST2SMS RESPONSE:", result)

        if response.status_code == 200 and result.get("return") is True:
            return True, otp

        return False, None

    except Exception as e:

        print("FAST2SMS ERROR:", e)

        return False, None