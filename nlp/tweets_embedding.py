# Given a set of tweets from a hashtag or a user, plot the cloud of its embeddings.
# An embedding of a tweet is a probability over latent topics.
import scipy
import tensorflow as tf
import numpy as np
import json

# Read tweets from json file.
# V: size of vocabulary
# D: number of tweets
# GaP: X_{vd} = Poisson(w h)...
# Ber: X_{xd} = Ber(w h)
# LDA: X_{*d} = Multinomial(W h)
# VAE: X_{*d} = p(x | z)
# MF-VAE?: X_{*d} = p(x | Wh)

file = 
#TODO: read json file, but in the future we will use JSON lines format.
def read_file(file):
    

