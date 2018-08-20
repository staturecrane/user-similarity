import math
import operator
import pickle

from tqdm import tqdm

import similarity_api.utils as utils

with open('svd_views.pickle', 'rb') as view_file:
    svd_views = pickle.load(view_file)

with open('svd_interests.pickle', 'rb') as interests_file:
    svd_interests = pickle.load(interests_file)

with open('svd_assessment.pickle','rb') as assessment_file:
    svd_assessments = pickle.load(assessment_file)

user_similarity_table = {i: {} for i in range(1, 10000)}
final_user_similarity_table = {i: [] for i in range(1, 10000)}

for i in tqdm(range(1, 10000)):
    user_a_views = svd_views[0][i-1]
    user_a_interests = svd_interests[0][i-1]
    user_a_assessments = svd_assessments[0][i-1]

    for j in range(1, 10000):
        if j != i:
            user_b_views = svd_views[0][j-1]
            user_b_interests = svd_interests[0][j-1]
            user_b_assessments = svd_assessments[0][j-1]
    
            views_sim = utils.cosine_similarity(user_a_views, user_b_views)
            interests_sim = utils.cosine_similarity(user_a_interests, user_b_interests)
            assessments_sim = utils.cosine_similarity(user_a_assessments, user_b_assessments)
            
            total_sim = 0
            for sim in [views_sim, interests_sim, assessments_sim]:
                if not math.isnan(sim):
                    total_sim += sim
            user_similarity_table[i][j] = total_sim / 3

    most_similar = utils.sort_most_similar(user_similarity_table[i])
    final_user_similarity_table[i] = most_similar

with open('final_user_similarity.pickle', 'wb') as sim_pickle:
    pickle.dump(final_user_similarity_table, sim_pickle)