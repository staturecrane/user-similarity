# Pluralsight User Similarity

API to determine similarity between Pluralsight users

## Requirements

You must have the latest edition of Docker Community Edition. To run the preprocessing steps, please load a virtual environment and run:

```shell
pip install -r requirements.txt
```

The scripts expect a Python3.6+ environment.

## Analyzing and Processing Data

The data folder should contain the following files:
- course_tags.csv
- user_assessment_scores.csv
- user_course_views.csv
- user_interests.csv

Compute the initial SVD factors for each feature by running the following:

```shell
python compute_similarity.py --data <DATA_FOLDER>
```
This will leave you with three pickled numpy arrays:
- svd_views.pickle
- svd_interests.pickle
- svd_assessments.pickle

Leave these in the root directory. They will be needed for the next step.

```shell
python compute_similarity.py
```

This will save the final similarity dictionary, `final_user_similarity.pickle' that will be used at API runtime.

## Running with Docker

**NOTE: The Docker build expects the `final_user_similarity.pickle` file to be present in Docker context (root directory).**

```shell
docker build -t sim .
```

```shell
docker run --rm -it -p 5000:5000 sim
```

The service will now be running at `http://localhost:5000`. Check its health by running a GET request against `http://localhost:5000/health`.

## Testing with Docker

```shell
docker build -t sim-tests -f Dockerfile-tests .
```

```shell
docker run --rm -it sim-tests
```

Tests should all pass.

## Query a user

# GET **/user/similarity/[handle]**

Returns JSON list of 10 most similar users