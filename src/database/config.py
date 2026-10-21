
import os
import streamlit as st
from supabase import create_client
from streamlit.errors import StreamlitSecretNotFoundError


def get_secret(key):
    # First, check Render environment variables
    value = os.getenv(key)

    if value:
        return value

    # If not found, check local Streamlit secrets
    try:
        return st.secrets[key]
    except (KeyError, StreamlitSecretNotFoundError):
        return None


SUPABASE_URL = get_secret("SUPABASE_URL")
SUPABASE_KEY = get_secret("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "Supabase credentials missing. "
        "Set SUPABASE_URL and SUPABASE_KEY."
    )

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
