# import sys
# import os
import json
import streamlit as st
import pandas as pd
# import time
# from src.data_loader import TelegramDataLoader
from src.data_cleaner import ChatDataCleaner
from src.eda import ChatEDA
from src.feature_engineering import FeatureEngineering
from utils import log
from visualizations import plot_messages_over_time, plot_messages_per_user, plot_heatmap, plot_wordcloud

# Streamlit UI
st.title("📊 Advanced Chat Analyzer Dashboard 🗨️")
st.write("Upload your Telegram or WhatsApp chat file to analyze conversations deeply.")

# File uploader
uploaded_file = st.file_uploader("Upload your chat file", type=["json", "txt"])

# ✅ Create a placeholder for logs (after file is uploaded)
log_container = st.container()

# Cache data processing to avoid reloading on every interaction
@st.cache_data
def process_data(messages):
    cleaner = ChatDataCleaner(messages)
    cleaned_df = cleaner.clean_data()
    eda = ChatEDA(cleaned_df)
    fe = FeatureEngineering(cleaned_df)
    return cleaned_df, eda, fe

if uploaded_file:
    file_extension = uploaded_file.name.split(".")[-1]

    with log_container:
        log_status = st.empty()  # Placeholder for status updates

    if file_extension == "json":
        with log_container:
            log(log_status, "📂 Loading chat data...")
            data = json.load(uploaded_file)
            messages = data.get("messages", [])

            log(log_status, "🧹 Processing data...")
            cleaned_df, eda, fe = process_data(messages)
            log(log_status, "✅ Analysis Completed!", status="success")

        # Sidebar filters
        with st.sidebar:
            st.header("🔍 Filters")
            date_range = st.date_input("Select Date Range", [])
            selected_user = st.selectbox("Filter by User", ["All"] + list(cleaned_df["from"].unique()))

        # Apply filters
        if selected_user != "All":
            cleaned_df = cleaned_df[cleaned_df["from"] == selected_user]

        # Now show the statistics & visualizations below
        st.subheader("Chat Statistics 📊")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Messages", len(cleaned_df))
        with col2:
            st.metric("Unique Users", cleaned_df["from"].nunique())

        # Show visualizations
        st.subheader("Visualizations 📈")
        col1, col2 = st.columns(2)
        with col1:
            col_gran, col_labels = st.columns([3, 1])
            plot_messages_over_time(eda)
        
        with col2:
            plot_heatmap(eda)

        # Additional visualizations
        plot_messages_per_user(eda)
        plot_wordcloud(cleaned_df)

    else:
        st.warning("Currently, only Telegram JSON files are supported.")