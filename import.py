import sys
import pandas as pd
import pymongo
import json
from tqdm import tqdm

if __name__ == "__main__":
    argv = sys.argv
    if len(argv) < 3:
        print("Usage: python import.py mongodb_uri filename collection")
        exit(-1)

    mongodb_uri = argv[1]
    filename = argv[2]
    collection = argv[3]
    
    df = pd.read_csv(filename).fillna('')
    db = pymongo.MongoClient(mongodb_uri).get_database()
    
    for index in tqdm(range(len(df.index))):
        record = json.loads(df.iloc[index].to_json())
        id = record.get('id', str(index))
        record['_id'] = id
        #print(json.dumps(record, indent=2))
        db[collection].replace_one({'_id': id}, record, True)


    
