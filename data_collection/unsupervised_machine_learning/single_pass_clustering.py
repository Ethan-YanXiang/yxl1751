import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from data_collection.database import save_cluster_to_db, update_cluster_in_db, get_clusters_from_db


def real_time_single_pass_clustering(tfidf_matrix, feature_names, threshold=0.5):
    clusters = get_clusters_from_db()
    tfidf_matrix = tfidf_matrix.toarray()

    if not clusters:
        keywords = get_top_keywords(tfidf_matrix, feature_names)
        cluster_id = save_cluster_to_db(tfidf_matrix.tolist(), keywords)
        return cluster_id
    else:
        similarities = [cosine_similarity(tfidf_matrix.reshape(1, -1), np.array(cluster[1]).reshape(1, -1))[0][0] for cluster in clusters]
        max_similarity_index = np.argmax(similarities)
        max_similarity_value = similarities[max_similarity_index]

        if max_similarity_value < threshold:
            keywords = get_top_keywords(tfidf_matrix, feature_names)
            cluster_id = save_cluster_to_db(tfidf_matrix.tolist(), keywords)
            return cluster_id
        else:
            cluster = clusters[max_similarity_index]
            new_cluster_center = (np.array(cluster[1]) + tfidf_matrix) / 2
            keywords = get_top_keywords(new_cluster_center, feature_names)
            update_cluster_in_db(cluster[0], new_cluster_center.tolist(), keywords)
            return cluster[0]


def get_top_keywords(tfidf_matrix, feature_names, top_n=5):
    top_keywords_indices = np.argsort(tfidf_matrix).flatten()[-top_n:]
    return [feature_names[i] for i in top_keywords_indices]
