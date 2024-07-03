import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import json
import os
from scipy.stats import entropy

   # Define the coordinates
# coordinates = np.array([
#         [1745, 758], [1794, 758], [1220, 954], [1740, 742], [1782, 741],
#         [1183, 929], [1739, 761], [1782, 762], [1182, 987], [1759, 761],
#         [1799, 761], [1267, 987], [1762, 750], [1800, 751], [1268, 929],
#         [1750, 754], [1793, 755], [1228, 956]
#     ])

def load_coordinates(filename):
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'recordings', filename)

    with open(file_path, 'r') as file:
        events = json.load(file)
    
    coordinates = []
    for event in events:
        pos = event.get('pos')
        if pos and isinstance(pos, list) and len(pos) == 2:
            coordinates.append(pos)

    return np.array(coordinates)

    # coordinates = np.array([event['pos'] for event in events])
    # return coordinates

def cluster(coordinates, n_clusters=3):
    # Apply K-Means Clustering

    kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
    kmeans.fit(coordinates)
    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_

    # Plotting the results
    plt.scatter(coordinates[:, 0], coordinates[:, 1], c=labels, cmap='viridis')
    plt.scatter(centroids[:, 0], centroids[:, 1], s=300, c='red')
    plt.xlabel('X coordinate')
    plt.ylabel('Y coordinate')
    plt.title('K-Means Clustering of Coordinates')
    plt.show()

    # Compute frequency distribution of coordinates
    unique, counts = np.unique(coordinates, axis=0, return_counts=True)
    probs = counts / len(coordinates)

    # Calculate Shannon Entropy, the uncertainty of a probability distribution.
    shannon_entropy = entropy(probs)
    print(f"Shannon Entropy: {shannon_entropy}")

def elbow_method(coordinates):
    wcss = []
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i, n_init=10, random_state=42)
        kmeans.fit(coordinates)
        wcss.append(kmeans.inertia_)

    plt.plot(range(1, 11), wcss, marker="o")
    plt.title('Elbow Method')
    plt.xlabel('Number of clusters')
    plt.ylabel('WCSS')
    plt.show()

    first_derivative = np.diff(wcss)
    second_derivative = np.diff(first_derivative)
    elbow_point = np.argmax(second_derivative) + 2  # +2 to account for the diff shifting the indices
    return elbow_point

def silhouette_scores(coordinates):
    silhouette_scores = []
    for i in range(2, 11):
        kmeans = KMeans(n_clusters=i, n_init=10, random_state=42)
        kmeans.fit(coordinates)
        score = silhouette_score(coordinates, kmeans.labels_)
        silhouette_scores.append(score)

    plt.plot(range(2, 11), silhouette_scores)
    plt.title('Silhouette Scores')
    plt.xlabel('Number of clusters')
    plt.ylabel('Silhouette Score')
    plt.show()

    optimal_clusters = np.argmax(silhouette_scores) + 2
    return optimal_clusters

input = input("enter filename")
filename = input
coordinates = load_coordinates(filename)
optimal_clusters_elbow = elbow_method(coordinates)
optimal_clusters_silhouette = silhouette_scores(coordinates)
final_clusters = max(optimal_clusters_elbow, optimal_clusters_silhouette)
print(optimal_clusters_elbow, optimal_clusters_silhouette)
cluster(coordinates, n_clusters=final_clusters)