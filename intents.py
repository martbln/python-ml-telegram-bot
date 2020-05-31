import json
import random

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

CLASSIFIER_THRESHOLD = 0.3


with open('data/intents.json') as file:
    INTENTS_DATA = json.load(file)


X_text = []  # texts
y = []  # class and intents for texts

for intent, value in INTENTS_DATA['intents'].items():
    for example in value['examples']:
        X_text.append(example)
        y.append(intent)


VECTORIZER = TfidfVectorizer(
    analyzer='char', norm='l2', ngram_range=(1, 3), sublinear_tf=True)
X = VECTORIZER.fit_transform(X_text)

CLF = LogisticRegression(C=1000, class_weight='balanced')
CLF.fit(X, y)


def get_intent(text):
    probas = CLF.predict_proba(VECTORIZER.transform([text]))
    max_proba = max(probas[0])
    if max_proba >= CLASSIFIER_THRESHOLD:
        index = list(probas[0]).index(max_proba)
        return CLF.classes_[index]


def get_response_by_intent(intent):
    responses = INTENTS_DATA['intents'][intent]['responses']
    return random.choice(responses)


def get_failure_phrase():
    phrases = INTENTS_DATA['failure_phrases']
    return random.choice(phrases)
