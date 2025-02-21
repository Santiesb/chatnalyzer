import pandas as pd
import nltk
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy

# Ensure necessary resources are available
nltk.download("stopwords")
nltk.download("punkt")
nlp = spacy.load("es_core_news_sm")  # Load small Spanish NLP model

class FeatureEngineering:
    def __init__(self, cleaned_data: pd.DataFrame):
        """
        Initializes the FeatureEngineering class with cleaned chat data.
        
        :param cleaned_data: DataFrame containing the cleaned chat messages.
        """
        self.df = cleaned_data

    def word_frequency(self, top_n: int = 20) -> pd.DataFrame:
        """
        Computes the most frequently used words in the chat.

        :param top_n: Number of top words to return.
        :return: DataFrame with the most frequent words.
        """
        all_words = [word for tokens in self.df["filtered_tokens"].dropna() for word in tokens]
        word_counts = Counter(all_words).most_common(top_n)

        return pd.DataFrame(word_counts, columns=["Word", "Count"])

    def compute_tfidf(self, max_features: int = 50) -> pd.DataFrame:
        """
        Computes TF-IDF scores for the most important words.

        :param max_features: Number of top TF-IDF words to return.
        :return: DataFrame with words and their TF-IDF scores.
        """
        tfidf_vectorizer = TfidfVectorizer(max_features=max_features)
        tfidf_matrix = tfidf_vectorizer.fit_transform(self.df["cleaned_text"].dropna())

        # Extract feature names and TF-IDF scores
        feature_names = tfidf_vectorizer.get_feature_names_out()
        tfidf_scores = tfidf_matrix.sum(axis=0).A1  # Convert matrix to array

        return pd.DataFrame(zip(feature_names, tfidf_scores), columns=["Word", "TF-IDF"]).sort_values(by="TF-IDF", ascending=False)

    def named_entity_recognition(self) -> pd.DataFrame:
        """
        Extracts named entities (persons, locations, brands) using spaCy.

        :return: DataFrame with named entities and their counts.
        """
        entities = []
        for text in self.df["cleaned_text"].dropna():
            doc = nlp(text)
            entities.extend([ent.text for ent in doc.ents])

        entity_counts = Counter(entities).most_common(20)
        return pd.DataFrame(entity_counts, columns=["Entity", "Count"])
