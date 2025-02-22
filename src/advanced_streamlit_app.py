import sys
import os
import json
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from src.data_loader import TelegramDataLoader
from src.data_cleaner import ChatDataCleaner
from src.eda import ChatEDA
from src.feature_engineering import FeatureEngineering
import time  # Simulate process timing

# Configure visualization
sns.set(style="whitegrid")

# Add project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Streamlit UI
st.set_page_config(page_title="Chat Analyzer", layout="wide")
st.title("📊 Advanced Chat Analyzer Dashboard 🗨️")
st.write("Upload your Telegram or WhatsApp chat file to analyze conversations deeply.")

# File uploader
uploaded_file = st.file_uploader("Upload your chat file", type=["json", "txt"])

# ✅ Create a dynamic log display
log_placeholder = st.empty()
log_messages = []

def log(msg):
    """Log messages dynamically to Streamlit."""
    log_messages.append(msg)
    log_placeholder.text("\n".join(log_messages))  # Update log UI dynamically
    print(msg)  # Print to console as well
    time.sleep(0.2)  # Simulate delay for visibility

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
            col1, col2 = st.columns(2)
            with col1:
                date_range = st.date_input("Date Range", [])
            with col2:
                selected_user = st.selectbox("User", ["All"] + list(cleaned_df["from"].unique()))
            keyword = st.text_input("Search Keyword")

        # Apply filters
        if selected_user != "All":
            cleaned_df = cleaned_df[cleaned_df["from"] == selected_user]
        if keyword:
            cleaned_df = cleaned_df[cleaned_df["cleaned_text"].str.contains(keyword, case=False, na=False)]

        # Main statistics
        st.subheader("Chat Statistics 📊")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Messages", len(cleaned_df))
        with col2:
            st.metric("Unique Users", cleaned_df["from"].nunique())
        
        with st.expander("View Data Table"):
            st.dataframe(cleaned_df[["from", "date", "original_text", "cleaned_text"]])

        # Visualizations
        st.subheader("Visualizations 📈")
        col1, col2 = st.columns(2)

        with col1:
            st.write("### Messages Over Time")
            st.line_chart(eda.messages_over_time("D").set_index("Date"))

        with col2:
            st.write("### Messages Per User")
            st.bar_chart(eda.messages_per_user().set_index("User"))

        # Heatmap of Message Activity by Hour and Day
        st.write("### Message Activity Heatmap (Hour vs. Day)")
        heatmap_data = eda.messages_by_day_hour()

        if heatmap_data is not None and not heatmap_data.empty:
            fig, ax = plt.subplots(figsize=(8, 3))
            heatmap = sns.heatmap(
                            heatmap_data
                            , cmap="coolwarm"
                            , linewidths=0.5
                            , annot=True
                            , fmt=".0f"
                            , ax=ax
                            , annot_kws={"size": 4}
                            , cbar=False
                            ) # Plot heatmap
            # Set heatmap labels and reduce side legend
            heatmap.figure.colorbar(heatmap.collections[0]).ax.tick_params(labelsize=6)
            plt.xticks(fontsize=6, rotation=0)
            plt.yticks(fontsize=5, rotation=0)
            plt.xlabel("Day of the Week", fontsize=8)
            plt.ylabel("Hour of the Day", fontsize=8)
            st.pyplot(fig)
        else:
            st.write("No data available for heatmap.")

        # Word Cloud
        st.write("### Word Cloud")
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(" ".join(cleaned_df["cleaned_text"].dropna()))
        plt.figure(figsize=(8, 4))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        st.pyplot(plt)

        log("✅ Analysis Completed!")
        st.success("Analysis Completed! ✅")

    else:
        st.warning("Currently, only Telegram JSON files are supported.")
