# Given a set of tweets from a hashtag or a user, plot the cloud of its embeddings.
# An embedding of a tweet is a probability over latent topics.
import scipy
import tensorflow as tf
import numpy as np
import pandas as pd

from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.manifold import TSNE

import condor
from condor.config import PATHS
from condor.utils.utils_json import load_jsonl
import pprint

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

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
    """Given a list of texts, build a Term x Document matrix"""
    # TODO check efficient ways to do this.
    pass


def embeddings_Gamma_Poisson():
    raise NotImplementedError


def embeddings_Bernoulli():
    raise NotImplementedError


def embeddings_LDA(data):
    n_features = 1000

    # use scikit-learn implementation
    # https://scikit-learn.org/stable/auto_examples/applications/plot_topics_extraction_with_nmf_lda.html
    tf_vectorizer = CountVectorizer(max_df=0.95, 
                                    min_df=0.2,
                                    max_features=n_features,
                                    stop_words=None)                         
    tf = tf_vectorizer.fit_transform(data)
    lda = LatentDirichletAllocation(n_components=3, max_iter=5,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)
    lda.fit(tf)

    print("\nTopics in LDA model:")
    tf_feature_names = tf_vectorizer.get_feature_names()
    print_top_words(lda, tf_feature_names, n_top_words=100)
    params = lda.get_params()
    print(params)
    # Show topic distribution over words
    # https://stackoverflow.com/questions/44208501/getting-topic-word-distribution-from-lda-in-scikit-learn
    topic_embeddings = lda.components_ / lda.components_.sum(axis=1)[:, np.newaxis]
    print(topic_embeddings)
    # TODO project with t-SNE
    # t SNE ok for user embeddings.
    # Will be harder for product embeddings, too many dimensions.
    tsne = TSNE(n_components=2, verbose=0, perplexity=40, n_iter=300)
    tsne_results = tsne.fit_transform(topic_embeddings)

    N = 10000
    df = pd.DataFrame(tsne_results)
    rndperm = np.random.permutation(df.shape[0])

    df_subset = df.loc[rndperm[:N],:].copy()
    df_subset['tsne-one'] = tsne_results[:,0]
    df_subset['tsne-two'] = tsne_results[:,1]

    plt.figure(figsize=(16,4))
    ax = plt.subplot(1, 3, 3)
    sns.scatterplot(
        x="tsne-one", y="tsne-two",
        hue="y",
        palette=sns.color_palette("hls", 10),
        data=df_subset,
        legend="full",
        alpha=0.3,
        ax=ax
)

def embeddings_VAE():
    pass


def embeddings_NLP():
    pass


def plot_embeddings():
    """Plot a cloud of embeddings using t-SNE"""
    pass

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)
    print()


if __name__ == '__main__':
    data = read_file(keyword="hola")
    data = data[0:10]
    tweets = [d['text'] for d in data]
    pprint.pprint(tweets)
    embeddings_LDA(tweets)