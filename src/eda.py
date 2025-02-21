import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Any

# Configure seaborn for better plots
sns.set(style="whitegrid")

class ChatEDA:
    def __init__(self, cleaned_data: pd.DataFrame):
        """
        Initializes the EDA class with cleaned chat data.
        
        :param cleaned_data: DataFrame containing the cleaned chat messages.
        """
        self.df = cleaned_data

    def messages_per_user(self) -> pd.DataFrame:
        """
        Computes the number of messages sent per user.

        :return: DataFrame with user message counts.
        """
        user_counts = self.df["from"].value_counts().reset_index()
        user_counts.columns = ["User", "Messages"]
        return user_counts

    def messages_over_time(self, time_unit: str = "D") -> pd.DataFrame:
        """
        Aggregates messages over time (daily, hourly).

        :param time_unit: Time unit for aggregation ('D' for daily, 'H' for hourly).
        :return: DataFrame with message counts over time.
        """
        self.df["date"] = pd.to_datetime(self.df["date"])
        time_series = self.df.set_index("date").resample(time_unit).size().reset_index()
        time_series.columns = ["Date", "Messages"]
        return time_series

    def most_common_words(self, top_n: int = 10) -> pd.DataFrame:
        """
        Finds the most frequently used words in the chat.

        :param top_n: Number of most frequent words to return.
        :return: DataFrame with the top N most used words.
        """
        all_text = " ".join(self.df["text"].dropna())  # Join all messages into a single string
        words = pd.Series(all_text.split())  # Split into words
        word_counts = words.value_counts().head(top_n).reset_index()
        word_counts.columns = ["Word", "Count"]
        return word_counts

    def urls_table(self) -> pd.DataFrame:
        """
        Creates a table showing URLs and the number of messages they appear in.

        :return: DataFrame with URL counts.
        """
        if "urls" not in self.df.columns:
            return pd.DataFrame(columns=["URL", "Message Count"])
        
        # Explode lists of URLs into individual rows
        urls_df = self.df.explode("urls")
        
        # Count occurrences of each URL
        url_counts = urls_df["urls"].dropna().value_counts().reset_index()
        url_counts.columns = ["URL", "Message Count"]
        return url_counts

    def plot_messages_per_user(self):
        """
        Generates a bar plot of messages per user, ensuring proper color handling.
        """
        user_counts = self.messages_per_user()
        plt.figure(figsize=(10, 5))
        sns.barplot(data=user_counts, x="User", y="Messages", hue="User", palette="viridis", legend=False)
        plt.xticks(rotation=45, ha="right", fontfamily="sans-serif")
        plt.title("Messages per User")
        plt.xlabel("User")
        plt.ylabel("Message Count")
        plt.show()

    def plot_messages_over_time(self, time_unit: str = "D"):
        """
        Generates a time series plot of message activity.

        :param time_unit: Time unit for aggregation ('D' for daily, 'H' for hourly).
        """
        time_series = self.messages_over_time(time_unit)
        plt.figure(figsize=(12, 5))
        sns.lineplot(data=time_series, x="Date", y="Messages", marker="o")
        plt.xticks(rotation=45, fontfamily="sans-serif")
        plt.title(f"Messages Over Time ({time_unit})")
        plt.xlabel("Date")
        plt.ylabel("Number of Messages")
        plt.show()
