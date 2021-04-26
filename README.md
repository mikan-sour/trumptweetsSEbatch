# About this

It's a batch for importing data into elasticsearch

# Important points

## Elasticsearch

- runs in a docker container
- use this command to run:
    docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.12.0


## This part
- it's just the batch that loads data
- the app that fetches the data is written in golang

### Environment variables
- must make a .env vile
- include DOCKER_ENV=True or DOCKER_ENV=False

# To Do
- build the app
- unit tests