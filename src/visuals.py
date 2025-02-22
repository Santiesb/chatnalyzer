# visuals.py
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

        if show_labels:
            text = chart.mark_text(align='center', dx=0, dy=-15).encode(text="Messages:Q")
            chart = chart + text
        
        st.altair_chart(chart, use_container_width=True)

    def plot_messages_per_user(self):
        """Messages per user bar chart."""
        st.write("### Messages Per User")
        user_counts = self.eda.messages_per_user()
        sorted_counts = user_counts.sort_values(by="Messages", ascending=False)
        
        chart = alt.Chart(sorted_counts).mark_bar().encode(
            x=alt.X("User:N", sort=alt.EncodingSortField(field="Messages", op="sum", order="descending"), title="User"),
            y=alt.Y("Messages:Q", title="Messages")
        ).interactive()
        
        st.altair_chart(chart, use_container_width=True)

    def plot_heatmap(self):
        """Heatmap visualization."""
        st.write("### Message Activity Heatmap (Hour vs. Day)")
        heatmap_data = self.eda.messages_by_day_hour()
        
        if not heatmap_data.empty:
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.heatmap(
                heatmap_data,
                cmap="coolwarm",
                linewidths=0.5,
                annot=True,
                fmt=".0f",
                ax=ax,
                annot_kws={"size": 6},
                cbar=False
            )
            plt.xticks(fontsize=7, rotation=0)
            plt.yticks(fontsize=7, rotation=0)
            plt.xlabel("Day of the Week", fontsize=8)
            plt.ylabel("Hour of the Day", fontsize=8)
            st.pyplot(fig)
        else:
            st.write("No data available for heatmap.")

    def plot_wordcloud(self):
        """Generate a word cloud using filtered tokens if available."""
        st.write("### Word Cloud")
        
        if "filtered_tokens" in self.eda.df.columns:
            tokens_list = self.eda.df["filtered_tokens"].dropna().tolist()
            flat_tokens = [token for sublist in tokens_list for token in sublist]
            text = " ".join(flat_tokens)
        elif "cleaned_text" in self.eda.df.columns:
            text = " ".join(self.eda.df["cleaned_text"].dropna())
        else:
            st.error("No valid text data for word cloud.")
            return
   
        if not text.strip():
            st.warning("No text available for word cloud.")
            return
   
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)

    def plot_user_interactions_network(self):
        """
        Plots an interactive network graph of user interactions using Plotly.
        An edge from Replier to Original indicates a reply.
        """
        import networkx as nx
        import plotly.graph_objects as go
        
        # Retrieve interactions from EDA
        interactions_df = self.eda.user_interactions()
        if interactions_df.empty:
            st.info("No user interactions found.")
            return
        
        # Build directed graph
        G = nx.DiGraph()
        edges = list(zip(interactions_df['Replier'], interactions_df['Original']))
        G.add_edges_from(edges)
        
        # Circular layout for disk appearance
        pos = nx.circular_layout(G)
        
        # Prepare edge traces
        edge_x, edge_y = [], []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            
        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            line=dict(width=1, color='#888'),
            hoverinfo='none',
            mode='lines'
        )
        
        # Prepare node traces
        node_x, node_y, node_text = [], [], []
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)
            
        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode='markers+text',
            text=node_text,
            textposition="bottom center",
            hoverinfo='text',
            marker=dict(
                size=20,
                color='#FFA500',
                line=dict(width=2)
            )
        )
        
        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title='User Interaction Network',
                            titlefont_size=16,
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                        ))
        fig.update_layout(clickmode='event+select')
        st.plotly_chart(fig, use_container_width=True)
