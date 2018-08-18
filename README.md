# Pluralsight User Similarity

API to determine similarity between Pluralsight users

## Requirements

You must have the latest edition of Docker Community Edition. 

## Running with Docker

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

