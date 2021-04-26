from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
from elasticsearch.exceptions import ConnectionError, ConnectionTimeout
import json
import tqdm
import pandas as pd
from time import sleep
import os

# Tweet Data to Dataframe

file = './realdonaldtrump.csv'
df = pd.read_csv(file)
json_data = json.loads(df.to_json(orient='records'))
docker_env = os.environ.get("DOCKER_ENV")

hosts =  [{'host': host, 'port': 9200} for host in ['elasticsearch1','elasticsearch2']] if docker_env else "http://localhost:9200"

# Client Config
es = Elasticsearch(hosts=hosts, timeout=60)

def check_connection():
    result = None
    tries = 1

    while result == None:
        try:
            print(f'trying to connect, try {tries}')
            conn = es.ping()
            if conn:
                result = True
                print(f'Connected after {tries} try(ies)')
            else:
                raise ConnectionError

        except ConnectionError:
            print(f'connection attempt failed, trying again')
            tries = tries +1
            sleep(10)
            continue



def gendata():
    for doc in json_data:
        yield doc

def main():
    check_connection()

    total_len = len(json_data)

    progress = tqdm.tqdm(unit="docs", total=total_len)
    successes = 0
    print("starting dataload")
    for ok, action in streaming_bulk(
            client=es, index="tweets", actions=gendata(),
    ):
        progress.update(1)
        successes += ok
    print("Indexed %d/%d documents" % (successes, total_len))

if __name__ == '__main__':
    main()

