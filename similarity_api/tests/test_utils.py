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