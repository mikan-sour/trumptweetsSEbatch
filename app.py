from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
import json
import tqdm
import pandas as pd

# Tweet Data to Dataframe

file = './realdonaldtrump.csv'
df = pd.read_csv(file)
json_data = json.loads(df.to_json(orient='records'))

# Client Config
es = Elasticsearch()

def gendata():
    for doc in json_data:
        yield doc

def main():
    print("starting dataload")

    total_len = len(json_data)

    progress = tqdm.tqdm(unit="docs", total=total_len)
    successes = 0
    for ok, action in streaming_bulk(
            client=es, index="tweets", actions=gendata(),
    ):
        progress.update(1)
        successes += ok
    print("Indexed %d/%d documents" % (successes, total_len))

if __name__ == '__main__':
    main()

