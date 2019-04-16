import glob

from elasticsearch.client import IndicesClient, Elasticsearch

INDEX = 'leg'
TYPE = 'diary'

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

ic = IndicesClient(es)

if ic.exists(index=INDEX):
    ic.delete(INDEX)
ic.create(index=INDEX, body={
    "settings": {
        "analysis": {
            "analyzer": "morfologik",
            "filter": ["lowercase"]
        }
    },
    "mappings": {
        "diary": {
            "properties": {
                "content": {
                    "term_vector": "yes",
                    "type": "text",
                    "analyzer": "morfologik"
                }
            }
        }
    }
})

list_of_files = glob.glob('../ustawy/*.txt')  # create the list of file

print("loading files....")

for file_name in list_of_files:
    with open(file_name, 'r') as myfile:
        data = myfile.read()
        es.index(index=INDEX, doc_type=TYPE, id=file_name, body={
            "content": data,
        })

print(es.mtermvectors(index=INDEX, doc_type=TYPE))

