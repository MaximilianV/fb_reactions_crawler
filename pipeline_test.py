from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from training.model import Model
import json


file="data\\evaluation\\affectivetext_trial_normalized.json"
with open(file, 'r') as infile:
    posts = json.load(infile)
corpus = map(lambda post: post['message'], posts)
reactions = list(map(lambda post: Model.translate_reaction(post['reaction']), posts))


tfidf = TfidfVectorizer()
model = MultinomialNB()

pipeline = Pipeline([("tfidf", tfidf), ("mnb", model)])
pipeline.fit(corpus, reactions)

print(pipeline.predict(["republicans tax"]))