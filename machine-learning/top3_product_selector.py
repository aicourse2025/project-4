"""
    Select the top 3 product for each category
"""

import pandas as pd

top3_csv = pd.read_csv("../data/reviews.csv")

# Group by ASIN and aggregate product data
groups = top3_csv.groupby("asins").agg({
    "name": "first",  # Take first product name
    "cluster_name": lambda x: x.mode().iloc[0],  # Most frequent cluster name
    "rating": ["mean", "count"],
    "imageURLs": lambda x: ','.join(set(
        # Combine unique image URLs
        url for urls in x.dropna().astype(str) for url in urls.split(',')
    )),
})

groups.columns = ["name", "cluster_name", "rating_mean", "rating_count", "imageURLs"]
groups = groups.reset_index()

# Round average rating to 2 decimals
groups["rating_mean"] = groups["rating_mean"].round(2)

# Calculate average
C = groups["rating_count"].mean()
m = groups["rating_mean"].mean()

# Compute weighted score (Bayesian average)
groups["weighted_score"] = (
    (groups["rating_count"] / (groups["rating_count"] + C)) * groups["rating_mean"]
    + (C / (groups["rating_count"] + C)) * m
)

# Get top 3 products per cluster
top3_per_cluster = (
    groups.sort_values(["cluster_name", "weighted_score"], ascending=[True, False])
    .groupby("cluster_name")
    .head(100)
    .reset_index(drop=True)
)

# Filter reviews for top products
reviews = top3_csv[["asins", "rating", "title_text_processed"]]
filtered_reviews = reviews[reviews["asins"].isin(top3_per_cluster["asins"])]

# Add title length column
filtered_reviews['title_length_chars'] = filtered_reviews['title_text_processed'].str.len()

# Count reviews per product
reviews_per_asin = filtered_reviews.groupby('asins').size().reset_index(name='count')

# Filter for medium length reviews (300-500 chars)
reviews_in_range = filtered_reviews[
    (filtered_reviews['title_length_chars'] >= 300) &
    (filtered_reviews['title_length_chars'] <= 500)
]


# Categorize review sentiment
def categorize_rating(rating):
    """Map rating to category"""
    if rating in [1, 2]:
        return "negative"
    if rating == 3:
        return "neutral"
    return "positive"

# Apply sentiment to both DataFrames
filtered_reviews['sentiment'] = filtered_reviews['rating'].apply(categorize_rating)
reviews_in_range['sentiment'] = reviews_in_range['rating'].apply(categorize_rating)

# Count reviews by sentiment
rating_counts = filtered_reviews.groupby(
    ['asins', 'sentiment']).size().reset_index(name='total_reviews')
range_counts = reviews_in_range.groupby(
    ['asins', 'sentiment']).size().reset_index(name='reviews_title_300_500')

# Merge counts
final_counts = pd.merge(
    rating_counts,
    range_counts,
    on=['asins', 'sentiment'],
    how='left'
).fillna(0).astype({'reviews_title_300_500': int})

# Combine top 5 reviews per sentiment as strings
grouped_reviews = (
    reviews_in_range
    .groupby(['asins', 'sentiment'])
    ['title_text_processed']
    .apply(lambda x: ' '.join(x.head(5)))  # Join first 5 reviews
    .unstack()
    .rename(columns={
        'positive': 'positive_reviews',
        'negative': 'negative_reviews'
    })
    .reset_index()
)

# Merge with product data
final_df = pd.merge(
    top3_per_cluster,
    grouped_reviews[['asins', 'positive_reviews', 'negative_reviews']],
    on='asins',
    how='left'
)

final_df.to_csv("../data/top3_products.csv", index=False)
