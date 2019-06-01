# Import all the cool stuff that makes stuff look cool... oh, and the 'sciency' stuff...
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# The 'stars' of the show - the movies themselves!
movies = pd.read_csv('moovees.csv', encoding='latin-1')

# Break up the big genre string into a string array
movies['genres'] = movies['genres'].str.split('|')
# Convert genres to string value
movies['genres'] = movies['genres'].fillna("").astype('str')

# CONVERTS THE MOVIE GENRES INTO A MATRIX OF TF-IDF FEATURES AND FORMATS THE DATA FOR THE COSINE SIMILARITY ALGORYTHM
tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(movies['genres'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)





