"""
Main runtime for FunnelAI NLP service
"""
import os
import pickle

from flask import jsonify, Response

from similarity_api.app import APP

with open('final_user_similarity.pickle', 'rb') as sim_file:
    SIMILARITY_TABLE = pickle.load(sim_file)


@APP.route('/user/similarity/<handle>')
def get_similar_users(handle):
    try:
        similar_users = SIMILARITY_TABLE[int(handle)]
    except KeyError:
        return Response('User not found. Try another handle'), 400
    return jsonify(similar_users)


@APP.route('/health')
def home():
    """
    Healthcheck
    """
    return Response('Similarity API'), 200

