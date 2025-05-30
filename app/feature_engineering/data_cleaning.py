import re

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# import nltk
# nltk.download('stopwords')
# nltk.download('wordnet')

# 初始化停用詞列表和詞形還原器
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def clean_text(body):
    body = body.lower()
    body = re.sub(r"\S+@\S+", "", body)
    body = re.sub(r"http\S+|www\S+", "", body)
    body = re.sub(r"[^\w\s]", " ", body)
    body = re.sub(r"\s+", " ", body).strip()  # 合并多余空格
    words = body.split()

    # 移除停用詞並進行詞形還原
    words = " ".join(
        lemmatizer.lemmatize(word) for word in words if word not in stop_words
    )

    return words
