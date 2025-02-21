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
        st.sidebar.header("🔍 Filters")
        date_range = st.sidebar.date_input("Select Date Range", [])
        selected_user = st.sidebar.selectbox("Filter by User", ["All"] + list(cleaned_df["from"].unique()))
        keyword = st.sidebar.text_input("Search for Keyword")

        # Apply filters
        if selected_user != "All":
            cleaned_df = cleaned_df[cleaned_df["from"] == selected_user]
        if keyword:
            cleaned_df = cleaned_df[cleaned_df["cleaned_text"].str.contains(keyword, case=False, na=False)]

        # Main statistics
        st.subheader("Chat Statistics 📊")
        st.write(f"**Total messages:** {len(cleaned_df)}")
        st.dataframe(cleaned_df[["from", "date", "original_text", "cleaned_text"]])

        # Visualizations
        st.subheader("Visualizations 📈")

        # Messages Over Time
        st.write("### Messages Over Time")
        st.line_chart(eda.messages_over_time("D").set_index("Date"))

        # Messages Per User
        st.write("### Messages Per User")
        st.bar_chart(eda.messages_per_user().set_index("User"))

        # Most Frequent Words
        st.write("### Most Frequent Words")
        word_freq = fe.word_frequency(20)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=word_freq, x="Word", y="Count", ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Word Cloud
        st.write("### Word Cloud")
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(" ".join(cleaned_df["cleaned_text"].dropna()))
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        st.pyplot(plt)

        # Emoji Frequency Analysis
        st.write("### Most Used Emojis")
        emoji_counts = cleaned_df["emojis"].dropna().explode().value_counts().reset_index()
        emoji_counts.columns = ["Emoji", "Count"]
        st.dataframe(emoji_counts.head(10))

        # Most Shared URLs
        st.write("### Most Shared URLs")
        if "urls" in cleaned_df.columns:
            url_counts = cleaned_df["urls"].dropna().value_counts().reset_index()
            url_counts.columns = ["URL", "Message Count"]
            st.dataframe(url_counts.head(10))

        # Named Entity Recognition (NER)
        st.write("### Named Entities Detected (People, Locations, Brands)")
        ner_df = fe.named_entity_recognition()
        if not ner_df.empty:
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.barplot(data=ner_df, x="Entity", y="Count", ax=ax)
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.write("No named entities detected.")

        # TF-IDF Word Importance
        st.write("### Most Important Words (TF-IDF)")
        tfidf_df = fe.compute_tfidf(20)
        st.dataframe(tfidf_df)

        log("✅ Analysis Completed!")
        st.success("Analysis Completed! ✅")

    else:
        st.warning("Currently, only Telegram JSON files are supported.")
