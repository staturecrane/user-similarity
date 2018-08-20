import pickle
import sys

import numpy as np
import pandas as pd
import tensorflow as tf

import similarity_api.utils as utils

data_folder = sys.argv[1]

course_tags = pd.read_csv(f'{data_folder}/course_tags.csv')
user_assessment = pd.read_csv(f'{data_folder}/user_assessment_scores.csv')
user_views = pd.read_csv(f'{data_folder}/user_course_views.csv')
user_interests = pd.read_csv(f'{data_folder}/user_interests.csv')

# gather users from all sources and turn into unique set
users = list(user_interests.user_handle.unique()) + list(user_assessment.user_handle.unique()) + list(user_views.user_handle.unique())

users = set(users)
num_users = len(users)

courses = course_tags.course_id.unique()
course_mapping = {course: i for i, course in enumerate(courses)}
num_courses = len(courses)

# create mappings from string ids to numeric indices
user_interest_tags = user_interests.interest_tag.unique()
user_interest_mapping = {tag: i for i, tag in enumerate(user_interest_tags)}
num_interest_tags = len(user_interest_tags)

assessment_tags = user_assessment.assessment_tag.unique()
assessment_mapping = {tag: i for i, tag in enumerate(assessment_tags)}
num_assessment_tags = len(assessment_tags)

# get min-max value of assessment scores for normalization -- this is a naive approach
# as I don't know the true potential maximum score
assessment_scores = list(user_assessment.user_assessment_score)
score_max = max(assessment_scores)
score_min = min(assessment_scores)

# create dicts for each similarity mapping to make creating similarity matrices easier
user_views_dict = {}
user_interests_dict = {}
user_assessments_dict = {}

for x in user_views.itertuples():
    user = getattr(x, 'user_handle')
    course_id = getattr(x, 'course_id')
    try:
        user_views_dict[user].append(course_id)
    except KeyError:
        user_views_dict[user] = [course_id]

for x in user_interests.itertuples():
    user = getattr(x, 'user_handle')
    interest_tag = getattr(x, 'interest_tag')
    try:
        user_interests_dict[user].append(interest_tag)
    except KeyError:
        user_interests_dict[user] = [interest_tag]

for x in user_assessment.itertuples():
    user = getattr(x, 'user_handle')
    assessment_tag = getattr(x, 'assessment_tag')
    score = getattr(x, 'user_assessment_score')
    assessment_tuple = (assessment_tag, score)
    try:
        user_assessments_dict[user].append(assessment_tuple)
    except KeyError:
        user_assessments_dict[user] = [assessment_tuple]
        
# remove any redundant user views
user_views_dict = {user_handle: list(set(views)) for user_handle, views in user_views_dict.items()}

# create sparse data matricies of NUM_USERSxITEM_LENGTH
user_views_data = np.zeros((num_users, num_courses))
for user_handle, views in user_views_dict.items():
    for course in views:
        course_index = course_mapping[course]
        user_views_data[user_handle-1][course_index] = 1

user_interest_data = np.zeros((num_users, num_interest_tags))
for user_handle, tags in user_interests_dict.items():
    for tag in tags:
        tag_index = user_interest_mapping[tag]
        user_interest_data[user_handle-1][tag_index] = 1
        
user_assessment_data = np.zeros((num_users, num_assessment_tags))
for user_handle, assessments in user_assessments_dict.items():
    for (tag, score) in assessments:
        tag_index = assessment_mapping[tag]
        user_interest_data[user_handle-1][tag_index] = utils.normalize(score, score_min, score_max)


# compute SVD for each feature and save factor matricies for similarity comparison
svd_views = utils.make_svd(user_views_data)
svd_interests = utils.make_svd(user_interest_data)
svd_assessment = utils.make_svd(user_assessment_data)

# save SVDs
with open('svd_views.pickle', 'wb') as user_views_file:
    pickle.dump(svd_views, user_views_file)

with open('svd_interests.pickle', 'wb') as user_interests_file:
    pickle.dump(svd_interests, user_interests_file)

with open('svd_assessment.pickle', 'wb') as user_assessment_file:
    pickle.dump(svd_assessment, user_assessment_file)