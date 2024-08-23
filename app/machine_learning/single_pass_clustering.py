import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from app.database.db import save_cluster_to_db, update_cluster_in_db, get_clusters_from_db


def real_time_single_pass_clustering(tfidf_matrix, feature_names, threshold=0.3):
    from app import app

    with app.app_context():
        tfidf_matrix = tfidf_matrix.toarray()
        print(f'The tfidf matrix {tfidf_matrix} has {tfidf_matrix.shape[1]} features')

        clusters = get_clusters_from_db()

        if not clusters:
            keywords = get_top_keywords(tfidf_matrix[0], feature_names)
            cluster_id = save_cluster_to_db(tfidf_matrix[0], keywords)
            return cluster_id
        else:
            cluster_centers = np.array([cluster[1] for cluster in clusters])
            similarities = cosine_similarity(tfidf_matrix, cluster_centers)[0]
            max_similarity_index = np.argmax(similarities)
            max_similarity_value = similarities[max_similarity_index]
            print(f'The most similar cluster center is {clusters[max_similarity_index]} with similarity {max_similarity_value}')

            if max_similarity_value < threshold:
                keywords = get_top_keywords(tfidf_matrix[0], feature_names)
                cluster_id = save_cluster_to_db(tfidf_matrix[0], keywords)
                return cluster_id
            else:
                cluster = clusters[max_similarity_index]
                new_cluster_center = (np.array(cluster[1]) + tfidf_matrix[0]) / 2
                keywords = get_top_keywords(new_cluster_center, feature_names)
                update_cluster_in_db(cluster[0], new_cluster_center, keywords)
                return cluster[0]


def get_top_keywords(tfidf_matrix, feature_names):
    top_keywords = np.argsort(-tfidf_matrix)[:5]
    keywords = []
    for i in top_keywords:
        feature_name = feature_names[i]
        keywords.append(feature_name)
    return ' '.join(keywords)
