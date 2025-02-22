import json
import streamlit as st
import pandas as pd
from src.data_cleaner import ChatDataCleaner
from src.eda import ChatEDA
from src.visuals import ChatVisualizer
from utils import log
import logging
nltk_logger = logging.getLogger('nltk')
nltk_logger.setLevel(logging.WARNING)

# Streamlit UI
st.set_page_config(layout='wide')
st.title("📊 Advanced Chat Analyzer Dashboard 🗨️")
st.write("Upload your Telegram or WhatsApp chat file to analyze conversations deeply.")

# File uploader
uploaded_file = st.file_uploader("Upload your chat file", type=["json"])

@st.cache_data
def process_data(messages):
    cleaner = ChatDataCleaner(messages)
    cleaned_df = cleaner.clean_data() 
    cleaned_actions = cleaner.standardize_timestamps(cleaner.cleaned_actions)
    actions_df = pd.DataFrame(cleaned_actions)
    
    return cleaned_df, actions_df

if uploaded_file:
    try:
        data = json.load(uploaded_file)
        messages = data.get("messages", [])
        if not messages:
            st.error("Uploaded JSON does not contain messages.")
    except json.JSONDecodeError:
        st.error("Invalid JSON file. Please upload a valid chat export.")
    else:
        # Process Data
        cleaned_df, actions_df = process_data(messages)

        # Sidebar filters
        with st.sidebar:
            st.header("🔍 Filters")
            with st.form(key="filter_form"):
                date_range = st.date_input("Select Date Range", [])
                selected_user = st.selectbox("Filter by User", ["All"] + list(cleaned_df["from"].unique()))
                submitted = st.form_submit_button("Apply Filters")

        # Apply filters globally
        filtered_df = cleaned_df.copy()
        filtered_actions_df = actions_df.copy()

        if selected_user != "All":
            filtered_df = filtered_df[filtered_df["from"] == selected_user]
            filtered_actions_df = filtered_actions_df[filtered_actions_df["actor"] == selected_user]

        if date_range:
            filtered_df = filtered_df[
                (filtered_df["date"] >= pd.to_datetime(date_range[0])) &
                (filtered_df["date"] <= pd.to_datetime(date_range[-1]))
            ]
            filtered_actions_df = filtered_actions_df[
                (filtered_actions_df["date"] >= pd.to_datetime(date_range[0])) &
                (filtered_actions_df["date"] <= pd.to_datetime(date_range[-1]))
            ]

        # Run EDA on the filtered data
        eda = ChatEDA(filtered_df, filtered_actions_df)

        # Initialize visualizer with filtered data
        visualizer = ChatVisualizer(eda)

        # Display filtered data preview
        st.subheader("🔍 Data Preview")
        st.dataframe(filtered_df.head(10), use_container_width=True)

        # Display actions (service messages)
        with st.expander("🔍 View Actions (User Joins, Name Changes, etc.)"):
            st.dataframe(filtered_actions_df, use_container_width=True)

        # show the statistics & visualizations below
        st.subheader("Chat Statistics 📊")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Messages", len(cleaned_df))
        with col2:
            st.metric("Unique Users", cleaned_df["from"].nunique())

        #  visualizations
        st.subheader("Visualizations 📈")
        col1, col2 = st.columns(2)
        with col1:
            col_gran, col_labels = st.columns([3, 1])
            visualizer.plot_messages_over_time()
        
        with col2:
            visualizer.plot_heatmap()

        visualizer.plot_messages_per_user()
        visualizer.plot_wordcloud()