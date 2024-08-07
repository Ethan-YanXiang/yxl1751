import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer_file = 'tfidf_vectorizer.pkl'
corpus_file = 'corpus.pkl'


def save_corpus(body):
    if os.path.exists(corpus_file):
        with open(corpus_file, 'rb') as file:
            corpus = pickle.load(file)
    else:
        corpus = []
    corpus.append(body)
    print(f'{len(corpus)} documents')
    with open(corpus_file, 'wb') as file:
        pickle.dump(corpus, file)
    return corpus


def train_and_save_tfidf_vectorizer(corpus):
    if os.path.exists(vectorizer_file):
        tfidf_vectorizer = load_tfidf_vectorizer()
        tfidf_vectorizer.fit(corpus)
    else:
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_vectorizer.fit(corpus)
        with open(vectorizer_file, 'wb') as file:
            pickle.dump(tfidf_vectorizer, file)


def load_tfidf_vectorizer():
    with open(vectorizer_file, 'rb') as file:
        tfidf_vectorizer = pickle.load(file)
    return tfidf_vectorizer


def body_to_vectors(body, tfidf_vectorizer):
    tfidf_matrix = tfidf_vectorizer.transform([body])
    feature_names = tfidf_vectorizer.get_feature_names_out()
    return tfidf_matrix, feature_names
