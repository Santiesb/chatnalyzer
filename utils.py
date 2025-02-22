import streamlit as st
import time

log_messages = []
log_placeholder = st.empty()

def log(msg):
    """Log messages dynamically to Streamlit."""
    log_messages.append(msg)
    log_placeholder.text("\n".join(log_messages))
    print(msg)
    time.sleep(0.2)
