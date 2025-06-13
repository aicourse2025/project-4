"""
    Cluster product categories (Unsupervised learning)
"""

import sys
import os
import matplotlib.pyplot as plt
import joblib
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from notebooks.preprocessing import load_and_preprocess_data, split_data

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

data = load_and_preprocess_data()
X_train, X_test, y_train, y_test, csv_data = split_data(data)

# Embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")
emb = model.encode(csv_data["combined_text_processed"].tolist(), show_progress_bar=True)

amount_of_clusters = range(4, 7)
inertia = []
scores = []

# Find the best amount of clusters with the elbow method and silhouette score
for k in amount_of_clusters:
    kmeans = KMeans(n_clusters=k, random_state=0)
    labels = kmeans.fit_predict(emb)

    inertia.append(kmeans.inertia_)
    score = silhouette_score(emb, labels)
    scores.append(score)

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(list(amount_of_clusters), inertia, marker='o')
plt.title("Elbow-Methode (Inertia)")
plt.xlabel("Anzahl Cluster (k)")
plt.ylabel("Inertia")

plt.subplot(1, 2, 2)
plt.plot(list(amount_of_clusters), scores, marker='o', color='green')
plt.title("Silhouette Score")
plt.xlabel("Anzahl Cluster (k)")
plt.ylabel("Silhouette Score")

plt.tight_layout()
plt.show()

# Choosing 4 clusters over 5 provides a better balance
# between model simplicity and cluster quality.
# The silhouette score is higher with 4 clusters,
# indicating more distinct and well-separated groups,
# while adding a fifth cluster leads to more overlap and less meaningful segmentation.

K_FINAL = 4

final_kmeans = KMeans(n_clusters=K_FINAL, random_state=0)
csv_data["cluster"] = final_kmeans.fit_predict(emb)

for i in range(K_FINAL):
    print(f"\nCluster {i} – top categories:\n")
    print(csv_data[csv_data["cluster"] == i]["categories"].value_counts().head(5))

# Find good names for the clusters
mapper = {
    0: "Entertainment Tablets",
    1: "E-Reader & Office Tablets",
    2: "Health & household accessories",
    3: "Smart Home & Amazon devices"
}

# Add cluster name to csv
csv_data["cluster_name"] = csv_data["cluster"].apply(lambda x: mapper[x])

# Save the model
joblib.dump(final_kmeans, "../models/kmeans_model.pkl")

# Save relevant data to a new csv file
csv_data[[
    "asins",
    "name",
    "rating",
    "title_text_processed",
    "imageURLs", "cluster_name"
]].to_csv("../data/reviews.csv", index=False)
