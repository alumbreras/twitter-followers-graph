# Given a set of tweets from a hashtag or a user, plot the cloud of its embeddings.
# An embedding of a tweet is a probability over latent topics.
import scipy
import tensorflow as tf
import numpy as np
from sklearn.decomposition import NMF, LatentDirichletAllocation

import condor
from condor.config import PATHS
from condor.utils.utils_json import load_jsonl
import pprint

# Execute with python -m condor.nlp.tweets_embedding from root folder

# Read tweets from json file.
# V: size of vocabulary
# D: number of tweets
# GaP: X_{vd} = Poisson(w h)...
# Ber: X_{xd} = Ber(w h)
# LDA: X_{*d} = Multinomial(W h)
# VAE: X_{*d} = p(x | z)
# MF-VAE?: X_{*d} = p(x | Wh)

def read_file(keyword="hola"):
    filename = PATHS['tracked'] + keyword + ".jsonl"
    return load_jsonl(filename)

def build_term_document_matrix(data):
    """Given a list of texts, build a Term x Document matrix""""
    # TODO check efficient ways to do this.
    pass


def embeddings_Gamma_Poisson():
    raise NotImplementedError


def embeddings_Bernoulli():
    raise NotImplementedError


def embeddings_LDA(data):
    # use scikit-learn implementation
    # https://scikit-learn.org/stable/auto_examples/applications/plot_topics_extraction_with_nmf_lda.html
    LatentDirichletAllocation
    tf_vectorizer = CountVectorizer(max_df=0.95, 
                                    min_df=2,
                                    max_features=n_features,
                                    stop_words='spanish')
    tf = tf_vectorizer.fit_transform(data)
    lda = LatentDirichletAllocation(n_components=10, max_iter=5,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)
    lda.fit(tf)
    pass


def embeddings_VAE():
    pass


def embeddings_NLP():
    pass


def plot_embeddings():
    """Plot a cloud of embeddings using t-SNE"""
    pass


if __name__ == '__main__':
    data = read_file(keyword="hola")
    data = data[0:2]
    tweets = [d['text'] for d in data]
    pprint.pprint(tweets)