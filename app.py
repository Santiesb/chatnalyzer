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

# `set_page_config` MUST be the first Streamlit command
st.set_page_config(page_title="Chat Analyzer", layout="wide")

# Streamlit UI
st.title("📊 Advanced Chat Analyzer Dashboard 🗨️")
st.write("Upload your Telegram or WhatsApp chat file to analyze conversations deeply.")

# File uploader
uploaded_file = st.file_uploader("Upload your chat file", type=["json", "txt"])

if uploaded_file:
    file_extension = uploaded_file.name.split(".")[-1]

    if file_extension == "json":
        log("📂 Loading chat data...")
        data = json.load(uploaded_file)
        messages = data.get("messages", [])

        log("🧹 Cleaning data...")
        cleaner = ChatDataCleaner(messages)
        cleaned_df = cleaner.clean_data()

        log("📊 Running Exploratory Data Analysis...")
        eda = ChatEDA(cleaned_df)

        log("🛠️ Extracting Features...")
        fe = FeatureEngineering(cleaned_df)

        # Sidebar filters
        with st.sidebar:
            st.header("🔍 Filters")
            selected_user = st.selectbox("User", ["All"] + list(cleaned_df["from"].unique()))
            keyword = st.text_input("Search Keyword")

        # Apply filters
        if selected_user != "All":
            cleaned_df = cleaned_df[cleaned_df["from"] == selected_user]
        if keyword:
            cleaned_df = cleaned_df[cleaned_df["cleaned_text"].str.contains(keyword, case=False, na=False)]

        # Main statistics
        st.subheader("Chat Statistics 📊")
        st.metric("Total Messages", len(cleaned_df))
        st.metric("Unique Users", cleaned_df["from"].nunique())

        # Data Table (Inside Expander)
        with st.expander("View Data Table"):
            st.dataframe(cleaned_df[["from", "date", "original_text", "cleaned_text"]])

        # Visualizations
        st.subheader("Visualizations 📈")
        
        plot_messages_over_time(eda)
        plot_messages_per_user(eda)
        plot_heatmap(eda)
        plot_wordcloud(cleaned_df)

        log("✅ Analysis Completed!")
        st.success("Analysis Completed! ✅")

    else:
        st.warning("Currently, only Telegram JSON files are supported.")
