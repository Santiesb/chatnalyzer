import streamlit as st
import time

def log(status_placeholder, message, status="loading"):
    """Dynamically updates a status indicator in Streamlit."""
    with status_placeholder.status(message, expanded=True) as status_box:
        time.sleep(0.5)  # Simulate delay
        if status == "success":
            status_box.update(label=message, state="complete")
        elif status == "error":
            status_box.update(label=message, state="error")
