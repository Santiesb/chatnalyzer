import pandas as pd
from typing import Any

class ChatEDA:
    def __init__(self, messages_df: pd.DataFrame, actions_df: pd.DataFrame = None):
        """
        Initializes the EDA class with cleaned chat data and service messages (actions).
        
        :param messages_df: DataFrame containing the cleaned chat messages.
        :param actions_df: DataFrame containing service messages (optional).
        """
        self.df = messages_df
        self.actions_df = actions_df  # Service messages (user joins, name changes, etc.)

    def messages_per_user(self) -> pd.DataFrame:
        """Computes the number of messages sent per user."""
        user_counts = self.df["from"].value_counts().reset_index()
        user_counts.columns = ["User", "Messages"]
        return user_counts

    def messages_over_time(self, time_unit: str = "D") -> pd.DataFrame:
        """Aggregates messages over time (daily, hourly)."""
        self.df["date"] = pd.to_datetime(self.df["date"])
        time_series = self.df.set_index("date").resample(time_unit).size().reset_index()
        time_series.columns = ["Date", "Messages"]
        return time_series

    def actions_over_time(self, time_unit: str = "D") -> pd.DataFrame:
        """Aggregates service actions over time."""
        if self.actions_df is not None and not self.actions_df.empty:
            self.actions_df["date"] = pd.to_datetime(self.actions_df["date"])
            time_series = self.actions_df.set_index("date").resample(time_unit).size().reset_index()
            time_series.columns = ["Date", "Actions"]
            return time_series
        return pd.DataFrame(columns=["Date", "Actions"])  # Empty DataFrame for safety

    def messages_by_day_hour(self) -> pd.DataFrame:
        """Aggregates message counts by day of the week and hour of the day."""
        self.df["date"] = pd.to_datetime(self.df["date"])
        self.df["day_of_week"] = self.df["date"].dt.day_name()
        self.df["hour"] = self.df["date"].dt.hour

        heatmap_data = self.df.groupby(["hour", "day_of_week"]).size().reset_index(name="message_count")

        days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        pivot_table = heatmap_data.pivot(index="hour", columns="day_of_week", values="message_count")

        pivot_table = pivot_table.reindex(index=range(0, 24), columns=days_order, fill_value=0)
        return pivot_table

    def urls_table(self) -> pd.DataFrame:
        """Creates a table showing URLs and the number of messages they appear in."""
        if "urls" not in self.df.columns:
            return pd.DataFrame(columns=["URL", "Message Count"])

        urls_df = self.df.explode("urls")
        url_counts = urls_df["urls"].dropna().value_counts().reset_index()
        url_counts.columns = ["URL", "Message Count"]
        return url_counts
