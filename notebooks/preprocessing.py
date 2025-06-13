"""
    Preprocessing of the CSV data
"""

import os
import string
import re
import pandas as pd
import kagglehub
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

def load_and_preprocess_data():
    """
    Loads and preprocesses Amazon product review data.
    
    Returns:
        pd.DataFrame: Preprocessed data
    """
    # Download latest version
    path = kagglehub.dataset_download("datafiniti/consumer-reviews-of-amazon-products")

    csv_data = []

    # Loop through each file
    for file in os.listdir(path):
        csv_file = os.path.join(path, file)
        df = pd.read_csv(
            csv_file,
            usecols=lambda col: col in
                [
                    "asins",
                    "name",
                    "categories",
                    "reviews.rating",
                    "reviews.text",
                    "reviews.title",
                    "imageURLs"
                ]
        )

        # Add missing column
        if "imageURLs" not in df.columns:
            df["imageURLs"] = ""

        df = df.rename(columns={
            "reviews.rating": "rating",
            "reviews.text": "text",
            "reviews.title": "title"
        })
        csv_data.append(df)

    # Concat data of all csv files it to one dataframe
    csv_data = pd.concat(csv_data)

    # Remove duplicates
    csv_data.drop_duplicates(subset=["text"], inplace=True)

    # Remove empty rows
    csv_data.dropna(inplace=True)

    # Combine text columns
    csv_data["title_text"] = csv_data["title"] + " " + csv_data["text"]
    csv_data["combined_text"] = (csv_data["title"] + " " + csv_data["text"] +
                                " " + csv_data["categories"] + " " + csv_data["name"])

    # Label Encoding
    le = LabelEncoder()
    csv_data["categories_encoded"] = le.fit_transform(csv_data["categories"])

    # Rating to sentiment
    def map_rating_to_sentiment(rating):
        """Map the rating (1-5 integer) to sentiment. 0 = negative, 1 = neutral, 2 = positive"""
        if rating < 2:
            return 0
        if rating == 3:
            return 1
        return 2

    csv_data["sentiment"] = csv_data["rating"].apply(map_rating_to_sentiment)

    # Text preprocessing
    lemmatizer = WordNetLemmatizer()

    def text_preprocessing_pipeline(text):
        """
        Preprocesses a text string by applying standard NLP cleaning steps:
        tokenization, stop word removal, punctuation removal, and lemmatization.

        Parameters:
            text (str): The input text string to preprocess.

        Returns:
            str: A cleaned and lemmatized string with tokens joined by spaces.
        """
        # Remove HTML
        text_without_html = re.sub(r'<[^<>]*>', '', text)

        # Tokenize the text
        tokenized_text = word_tokenize(text_without_html.lower())

        # Remove stop words
        stop_words = set(stopwords.words("english"))
        filtered_tokens = [w for w in tokenized_text if w.lower() not in stop_words]

        # Remove punctuation
        filtered_tokens = [w for w in filtered_tokens if w not in string.punctuation]

        # Apply lemmatization
        lemmatized_tokens = [lemmatizer.lemmatize(w) for w in filtered_tokens]

        return " ".join(lemmatized_tokens)

    csv_data["title_text_processed"] = csv_data["title_text"].apply(text_preprocessing_pipeline)
    csv_data["combined_text_processed"] = csv_data["combined_text"].apply(text_preprocessing_pipeline)

    return csv_data

def split_data(csv_data):
    """
    Splits the data into training and test sets and applies feature extraction.
    
    Parameters:
        csv_data (pd.DataFrame): Preprocessed data
        
    Returns:
        tuple: (X_train, X_test, y_train, y_test, csv_data)
    """
    # Train / Test Split
    y = csv_data["sentiment"]
    X = csv_data["title_text_processed"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=0)

    # Feature extraction
    vectorizer = TfidfVectorizer(ngram_range=(1,2))
    X_train = vectorizer.fit_transform(X_train)
    X_test = vectorizer.transform(X_test)

    # Handle imbalanced data
    smote = SMOTE(random_state=0)
    X_train, y_train = smote.fit_resample(X_train, y_train)

    return X_train, X_test, y_train, y_test, csv_data