from sklearn.feature_extraction.text import TfidfVectorizer

tfidf_vectorizer = TfidfVectorizer(stop_words='english')


def body_to_vectors(body):
    tfidf_matrix = tfidf_vectorizer.fit_transform([body])
    feature_names = tfidf_vectorizer.get_feature_names_out()
    return tfidf_matrix, feature_names
