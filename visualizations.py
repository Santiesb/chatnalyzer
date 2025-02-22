import streamlit as st
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud

def plot_messages_over_time(eda):
    """Interactive messages over time."""
    st.write("### Messages Over Time")
    
    time_series = eda.messages_over_time("D")
    time_series["Date"] = pd.to_datetime(time_series["Date"])
    
    col1, col2 = st.columns(2)
    with col1:
        time_granularity = st.selectbox("Time Granularity", ["Day", "Week", "Month", "Year"])
    with col2:
        show_labels = st.checkbox("Show Labels", value=True)
    
    if time_granularity == "Week":
        time_series = time_series.resample("W", on="Date").sum().reset_index()
    elif time_granularity == "Month":
        time_series = time_series.resample("ME", on="Date").sum().reset_index()
    elif time_granularity == "Year":
        time_series = time_series.resample("YE", on="Date").sum().reset_index()

    chart = alt.Chart(time_series).mark_line(point=True).encode(
        x=alt.X("Date:T", title="Date"),
        y=alt.Y("Messages:Q", title="Number of Messages"),
        tooltip=["Date:T", "Messages:Q"]
    ).interactive()

    # Add labels if enabled
    if show_labels:
        text = chart.mark_text(align='center', dx=0, dy=-15).encode(text="Messages:Q")
        chart = chart + text
    
    st.altair_chart(chart, use_container_width=True)

def plot_messages_per_user(eda):
    """Messages per user bar chart."""
    st.write("### Messages Per User")
    user_counts = eda.messages_per_user()
    st.bar_chart(user_counts.set_index("User"))

def plot_heatmap(eda):
    """Heatmap visualization."""
    st.write("### Message Activity Heatmap (Hour vs. Day)")
    heatmap_data = eda.messages_by_day_hour()
    
    if heatmap_data is not None and not heatmap_data.empty:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.heatmap(
            heatmap_data
            , cmap="coolwarm"
            , linewidths=0.5
            , annot=True
            , fmt=".0f"
            , ax=ax
            , annot_kws={"size": 6}
            , cbar=False)
        plt.xticks(fontsize=7, rotation=0)
        plt.yticks(fontsize=7, rotation=0)
        plt.xlabel("Day of the Week", fontsize=8)
        plt.ylabel("Hour of the Day", fontsize=8)
        st.pyplot(fig)
    else:
        st.write("No data available for heatmap.")

def plot_wordcloud(cleaned_df):
    """Generate a word cloud."""
    st.write("### Word Cloud")
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(" ".join(cleaned_df["cleaned_text"].dropna()))
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)
