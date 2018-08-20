"""
Utility functions for Pluralsight similarity challenge
"""
import numpy as np
import operator
import tensorflow as tf


def normalize(x, scoremin, scoremax):
    return (x - scoremin) / (scoremax - scoremin)


def euclidean(x, y):
    return np.sqrt(np.sum((x-y)**2))


def cosine_similarity(x, y):
    return np.dot(x, y) / (np.sqrt(np.dot(x, x)) * np.sqrt(np.dot(y, y)))


def make_svd(data, nb_factors=10):
    graph = tf.Graph()

    with graph.as_default():
        user_item_matrix = tf.placeholder(tf.float32, shape=data.shape)
        st, ut, vt = tf.svd(user_item_matrix)
        
        sk = tf.diag(st)[0:nb_factors, 0:nb_factors]
        uk = ut[:, 0:nb_factors]
        vk = vt[0:nb_factors, :]
        
        su = tf.matmul(uk, tf.sqrt(sk))
        
    session = tf.InteractiveSession(graph=graph)

    feed_dict = {user_item_matrix: data}
    su_ = session.run([su], feed_dict=feed_dict)

    session.close()
    return su_


def sort_most_similar(similarity_table, num_items=10):
    most_similar_tuple = sorted(similarity_table.items(), 
                                key=operator.itemgetter(1),
                                reverse=True)
    return list(map(lambda x: x[0], most_similar_tuple[:10]))
