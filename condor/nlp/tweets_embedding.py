# Given a set of tweets from a hashtag or a user, plot the cloud of its embeddings.
# An embedding of a tweet is a probability over latent topics.
import scipy
import tensorflow as tf
import numpy as np

import condor
from condor.config import PATHS
from condor.utils.utils_json import load_jsonl

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
    data = load_jsonl(filename)
    print(filename)
    print(data)


if __name__ == '__main__':
    read_file()