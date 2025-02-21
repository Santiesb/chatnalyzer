import sys
import os

# Add project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_loader import TelegramDataLoader
from src.data_cleaner import ChatDataCleaner
from src.eda import ChatEDA
import streamlit as st
import pandas as pd
import json


# Streamlit UI
st.title("Chat Analyzer MVP 🗨️📊")
st.write("Upload your Telegram or WhatsApp chat file to analyze.")

# File uploader
uploaded_file = st.file_uploader("Upload your chat file", type=["json", "txt"])

if uploaded_file:
    file_extension = uploaded_file.name.split(".")[-1]

    if file_extension == "json":
        # Load Telegram JSON
        data = json.load(uploaded_file)
        messages = data.get("messages", [])

        # Process messages (Removed @st.cache_data for speed)
        cleaner = ChatDataCleaner(messages)
        cleaned_df = cleaner.clean_data()

        # Run EDA
        eda = ChatEDA(cleaned_df)

        # Display stats
        st.subheader("Chat Statistics 📊")
        st.write(f"**Total messages:** {len(cleaned_df)}")

        st.write("### Messages Per User")
        st.dataframe(eda.messages_per_user())

        # Visualizations
        st.subheader("Visualizations 📈")

        st.write("### Messages Over Time")
        st.line_chart(eda.messages_over_time("D").set_index("Date"))

        st.write("### Messages Per User")
        st.bar_chart(eda.messages_per_user().set_index("User"))

    else:
        st.warning("Currently, only Telegram JSON files are supported.")
