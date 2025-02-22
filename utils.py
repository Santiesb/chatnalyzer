import streamlit as st

def log(status_placeholder, message, status="loading"):
    """Provides UI status updates efficiently in Streamlit."""
    if status == "loading":
        status_placeholder.info(f"⏳ {message}")
    elif status == "success":
        status_placeholder.success(f"✅ {message}")
    elif status == "error":
        status_placeholder.error(f"❌ {message}")
    else:
        status_placeholder.warning(f"⚠️ {message}")
