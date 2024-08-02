import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

clusters = []
cluster_keywords = []


def real_time_single_pass_clustering(tfidf_matrix, threshold=0.5):
    global clusters, cluster_keywords
    tfidf_matrix = tfidf_matrix.toarray()

    if not clusters:
        clusters.append(tfidf_matrix)
        top_keywords = np.argsort(tfidf_matrix).flatten()[-5:]
        cluster_keywords.append(top_keywords)
    else:
        similarities = [cosine_similarity(tfidf_matrix.reshape(1, -1), cluster_center) for cluster_center in clusters]
        max_similarity_index = np.argmax(similarities)
        max_similarity_value = similarities[max_similarity_index]

        if max_similarity_value < threshold:
            clusters.append(tfidf_matrix)
            top_keywords = np.argsort(tfidf_matrix).flatten()[-5:]
            cluster_keywords.append(top_keywords)
        else:
            clusters[max_similarity_index] = (clusters[max_similarity_index] + tfidf_matrix) / 2
            top_keywords = np.argsort(clusters[max_similarity_index]).flatten()[-5:]
            cluster_keywords[max_similarity_index] = top_keywords

    return clusters, cluster_keywords
