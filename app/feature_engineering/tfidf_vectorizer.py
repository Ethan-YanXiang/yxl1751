import os
import pickle
from app import basedir
from sklearn.feature_extraction.text import TfidfVectorizer

basedir = basedir
vectorizer_file = os.path.join(basedir, 'data', 'tfidf_vectorizer.pkl')
corpus_file = os.path.join(basedir, 'data', 'corpus.pkl')


def save_corpus(cleaned_body):
    if os.path.exists(corpus_file):
        with open(corpus_file, 'rb') as file:
            corpus = pickle.load(file)
            corpus.append(cleaned_body)
            print(f'{len(corpus)} documents to corpus')
    else:
        corpus = [cleaned_body]
        print(f'{len(corpus)} documents to corpus')
    with open(corpus_file, 'wb') as file:
        pickle.dump(corpus, file)


def train_and_save_tfidf_vectorizer():
    with open(corpus_file, 'rb') as file:
        corpus = pickle.load(file)
        if os.path.exists(vectorizer_file):
            with open(vectorizer_file, 'rb') as f:
                tfidf_vectorizer = pickle.load(f)
                tfidf_vectorizer.fit(corpus)
        else:
            tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.95, min_df=0.01, ngram_range=(1, 2), max_features=10000, norm='l2', use_idf=True)
            tfidf_vectorizer.fit(corpus)
        with open(vectorizer_file, 'wb') as w:
            pickle.dump(tfidf_vectorizer, w)


def body_to_vectors(cleaned_body):
    with open(vectorizer_file, 'rb') as file:
        tfidf_vectorizer = pickle.load(file)
        tfidf_matrix = tfidf_vectorizer.transform([cleaned_body])
        feature_names = tfidf_vectorizer.get_feature_names_out()
    return tfidf_matrix, feature_names
