import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer_file = 'tfidf_vectorizer.pkl'


def train_tfidf_vectorizer(bodies):
    if os.path.exists(vectorizer_file):
        with open(vectorizer_file, 'rb') as file:
            tfidf_vectorizer = pickle.load(file)
        tfidf_vectorizer.fit(bodies)
    else:
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_vectorizer.fit(bodies)

    with open(vectorizer_file, 'wb') as file:
        pickle.dump(tfidf_vectorizer, file)


def body_to_vectors(body):
    with open(vectorizer_file, 'rb') as file:
        tfidf_vectorizer = pickle.load(file)
    tfidf_matrix = tfidf_vectorizer.fit_transform([body])  # tfidf_matrix = tfidf_vectorizer.transform([body]) ???
    feature_names = tfidf_vectorizer.get_feature_names_out()
    return tfidf_matrix, feature_names
