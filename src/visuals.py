import streamlit as st
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud


class ChatVisualizer:
    def __init__(self, eda):
        """
        Initializes the visualization class.

        :param eda: Instance of ChatEDA containing preprocessed data.
        """
        self.eda = eda  # Store reference to ChatEDA instance

    def plot_messages_over_time(self):
        """Interactive messages over time."""
        st.write("### Messages Over Time")
        
        col1, col2 = st.columns(2)
        with col1:
            time_granularity = st.selectbox("Time Granularity", ["Day", "Week", "Month", "Year"])
        with col2:
            show_labels = st.checkbox("Show Labels", value=True)
        
        # Adjust time granularity
        freq_map = {"Day": "D", "Week": "W", "Month": "M", "Year": "Y"}
        time_series = self.eda.messages_over_time(freq_map[time_granularity])

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

    def plot_messages_per_user(self):
        """Messages per user bar chart."""
        st.write("### Messages Per User")
        user_counts = self.eda.messages_per_user()
        st.bar_chart(user_counts.set_index("User"))

    def plot_heatmap(self):
        """Heatmap visualization."""
        st.write("### Message Activity Heatmap (Hour vs. Day)")
        heatmap_data = self.eda.messages_by_day_hour()
        
        if not heatmap_data.empty:
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

    def plot_wordcloud(self):
        """Generate a word cloud."""
        st.write("### Word Cloud")
        
        # Check if 'cleaned_text' exists before using it
        if "cleaned_text" not in self.eda.df.columns:
            st.error("Word cloud cannot be generated: 'cleaned_text' column is missing.")
            return

        text = " ".join(self.eda.df["cleaned_text"].dropna())

        if not text.strip():
            st.warning("No text available for word cloud.")
            return

        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)
