# Project 4

**Objective**
This project uses an Amazon products review database as a source from which to generate article summaries with an LLM in the style of a blog article summary and review of a product.

## Dataset
We could choose between two sets of data.

1. https://www.kaggle.com/datasets/datafiniti/consumer-reviews-of-amazon-products/data
2. https://cseweb.ucsd.edu/~jmcauley/datasets.html#amazon_reviews 

We chose the first one because it was much smaller and easier to handle. But it still had enough data records to be able to work with it properly.


## Table of Contents
1. [Notebooks](#notebooks)
   - [Preprocessing](#preprocessing-preproccessingipynb)
   - [Clustering the Data](#clustering-the-data-cluster-product-categoriesipynb)
   - [Classifying Customer Reviews](#classifying-the-reviews-classify-customer-reviewsipynb)
   - [Top 3 Product Selector](#top-3-product-selector-top3_product_selectoripynb)
   - [Summary Fine-Tuning](#summary-fine-tuning-summary-fine-tuningipynb)
2. [Web](#web)
3. [API](#api)

## Notebooks:
- Preprocessing: preproccessing.ipynb
- Clustering the data: cluster-product-categories.ipynb
- Classification of Customer Reviews: classify-customer-reviews.ipynb
- Preprocessed, Clustered, and Classified Dataset: top3_product_selector.ipnyb
- Generation of a summary from different LLMs: summary-fine-tuning.ipynb

### Preprocessing: preproccessing.ipynb
#### Data loading: 
We download the most recent version of the dataset and then loop through the various files, searching for reading only the files with certain categories. Adding missing columns if necessary, renaming columns and concatening the files into one dataset.

#### Data Cleaning: 
We cleaned the data by removing rows with identical review text to prevent redundancy and bias from repeated entries.
We checked for empty rows and removed them, checked for unique ratings and combined certain columns with great similarity, and encoded categories.

#### Plotting
We used countplot to visualize how many reviews fall into each rating. And discovered a strong bias towards a 5 star review.

#### Sentiment analysis

#### Preprocessing
Uses a function to:
- Remove HTML tags using regex.
- Lowercase and tokenizes text.
- Remove stopwords and punctuation to clean the input.
- Lemmatizes tokens to reduce inflected words to their base forms.
- Returns a single cleaned string—ready for modeling or embedding.

Applies preprocessing to both title_text and combined_text columns.

#### Train / Test Split
Splits the cleaned data into training and testing data

#### Feature Extraction
We used TFidfVectorization to encode text into numeric features that emphasize particularly impactful rare words -- A process that is most directly effective when discerning whether a text is positive or negative.

#### Handle Imbalanced Data
As the data was quite imbalances and heavily biased towards 5 start ratings, it was necessary to address class imbalance by generating synthetic samples for underrepresented classes with SMOTE

### Clustering the data: cluster-product-categories.ipynb

#### Embeddings
- Uses embeddings to transform the unstructured data into numerical representations so that the model can understand the semantic meaning and relationship between words and phrases.

#### Setting Up K‑Means Clustering
- Uses k-means clustering to track the relationship between the data, and group together similar reviews.
- Uses Elbow method to determine the optimal number of clusters clusters and determine 
- Uses Silhouette analysis to determinethe cohesion of clusters and the distance between them.
- Findings: 4 clusters is better because it provides a better balance between model simplicity and cluster quality than 5. The silhouette score is also higher with 4 clusters, indicating more distinct and well-separated groups, while adding a fifth cluster leads to more overlap and less meaningful segmentation.
- Then we filtered the dataset rows to find the most frequent category of the cluster and assigned the top 5 clusters names that correspond to their most prominent themes and adds a new column with category names to the dataset. 

### Classifying the Reviews classify-customer-reviews.ipynb

- First we created a Naive Bayes model and trained it on the training data. We used MultinomialNB because it is ideal for text-based classification with TF-IDF features, modeling word counts per class.
- Then we made predictions on both training and test data to assess performance
- We used the XGBoost model for grid search to determine the optimal hyper parameters
- Then we extracted the best estimator that's been retrained on all of X_train with optimal parameters.

### Top 3 Product Selector top3_product_selector.ipynb

- We grouped the clustered and classified data by ASIN and aggregated the data with different rules
- We calculated Bayesian-style weighted score
- Filtered reviews for top products
- Categorized review sentiment
- Consolidated sample reviews by sentiment

### Summary Fine Tuning summary-fine-tuning.ipynb

The small prompt engineering notebook consists of various attempts to prompt-engineer smaller LLMs that are already uniquely designed to produce summaries.

- T5-small
- Flan-T5-base
- Flan-T5-large

This project utilizes the FLAN-T5-base and FLAN-T5-base, as well as the T5-small model from the Hugging Face transformers library to generate high-quality, blog-style product reviews from raw product review data. The model is guided by few-shot examples to produce polished summaries that resemble the writing style of top product reviewers.

#### Description
The code demonstrates the following steps:
 - Loading the FLAN-T5-base/large or T5-small model and tokenizer from Hugging Face.
 - Using few-shot examples to guide the model in generating blog-style reviews.
 - Loading a product review dataset from a CSV file.
 - Combining positive and negative reviews for each product.
 - Generating a summary using the model for each product, styled like a professional review (similar to Wirecutter blog style).
 - Printing the output summary for each product.

#### Findings:
After different attempts at prompting and variation in the model configuration the summary output from the models was strongly effected by the tokenized, broken English of the data set, and often returned summaries in similarly broken English or sentence fragments, often displaying repetition and speaking from the first person (a reflection of whom ever wrote the review in the original data). Likewise, these small models could not be trained to adopt a role in product review expertise that would reflect a more professional tone in the output. It seems that these LLMs are best applied to this kind of task with very short and concise general analysis of a product.

## Web

The web application provides a user-friendly interface to display the generated product summaries and reviews. For more details, please refer to the [Web-README](web/README.md).

## API

The API provides endpoints to access the product summaries and reviews programmatically. For more details, please refer to the [API-README](api/README.md).
