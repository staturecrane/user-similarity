import math
import numpy as np
import similarity_api.utils as utils


def test_normalization():
    score_max = 200
    score_min = 0
    
    for i in range(200):
        normalized_score = utils.normalize(i, score_min, score_max)
        assert normalized_score >= 0.0
        assert normalized_score <= 1.0

        non_prob = utils.normalize(202, score_min, score_max)
        assert non_prob > 1.0


def test_svd():
    user_count = 100
    item_count = 1000
    nb_factors = 10
    test_matrix = np.zeros((user_count, item_count))
    svd = utils.make_svd(test_matrix, nb_factors=nb_factors)
    assert len(svd[0]) == user_count
    assert len(svd[0][0]) == nb_factors


def test_cosine_similarity():
    good_a = [1.4, 0.01, 5.1]
    good_b = [4.1, 0.0341, 2.0]
    sim = utils.cosine_similarity(good_a, good_b)
    
    assert not math.isnan(sim)
    assert sim > -math.inf or sim < math.inf

    bad_a = [0.0, 0.0, 0.0]
    bad_b = [0.0, 0.0, 0.0]
    assert math.isnan(utils.cosine_similarity(bad_a, bad_b))