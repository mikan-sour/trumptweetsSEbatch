from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import json
import pandas as pd

# Tweet Data to Dataframe

file = './realdonaldtrump.csv'
df = pd.read_csv(file)
json_data = json.loads(df.to_json(orient='records'))

# Client Config

es = Elasticsearch()




