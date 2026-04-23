from google.oauth2 import id_token
from google.auth.transport import requests
import os
from dotenv import load_dotenv

# load .env
load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


def verify_google_token(token: str):
    try:
        # 🔍 verify token with Google
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            GOOGLE_CLIENT_ID
        )

        # ✅ issuer check (extra security)
        if idinfo["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
            return None

        return idinfo

    except Exception as e:
        print("Google Token Error:", e)
        return None