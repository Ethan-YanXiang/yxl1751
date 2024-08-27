import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from app.database.db import save_cluster_to_db, update_cluster_in_db, get_clusters_from_db


def real_time_single_pass_clustering(tfidf_matrix, feature_names, threshold=0.425):

    tfidf_matrix = tfidf_matrix.toarray()  #
    clusters = get_clusters_from_db()
    print(f'tfidf matrix:\n{tfidf_matrix} has {tfidf_matrix.shape[1]} features')

    if len(clusters) == 0:
        keywords = get_keywords(tfidf_matrix[0], feature_names)
        cluster_id = save_cluster_to_db(tfidf_matrix[0], keywords)
        print(f'Saved cluster {cluster_id}\n')
        return cluster_id
    else:
        cluster_centers = np.array([cluster[1] for cluster in clusters])
        print(f'cluster_centers:\n{cluster_centers}')
        similarities = cosine_similarity(tfidf_matrix, cluster_centers)[0]
        max_similarity_index = np.argmax(similarities)
        max_similarity_value = similarities[max_similarity_index]
        print(f'The most similar cluster center is {clusters[max_similarity_index][0]} with similarity {max_similarity_value}')

        if max_similarity_value < threshold:
            keywords = get_keywords(tfidf_matrix[0], feature_names)
            cluster_id = save_cluster_to_db(tfidf_matrix[0], keywords)
            print(f'similarity less than {threshold}: create new cluster {cluster_id}\n')
            return cluster_id
        else:
            cluster = clusters[max_similarity_index]
            new_cluster_center = (np.array(cluster[1]) + tfidf_matrix[0]) / 2
            keywords = get_keywords(new_cluster_center, feature_names)
            update_cluster_in_db(cluster[0], new_cluster_center, keywords)
            print(f'update cluster {cluster[0]}\n')
            return cluster[0]


def get_keywords(tfidf_matrix, feature_names):
    most_relevant_elements = np.argsort(-tfidf_matrix)[:5]
    keywords = ' '.join(feature_names[i] for i in most_relevant_elements)
    return keywords
