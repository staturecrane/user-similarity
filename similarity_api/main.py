"""
Main runtime for FunnelAI NLP service
"""
import os

from flask import Response

from similarity_api.app import APP


@APP.route('/health')
def home():
    """
    Healthcheck
    """
    return 'Similarity API', 200

