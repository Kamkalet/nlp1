import glob
import time

from elasticsearch.client import IndicesClient, Elasticsearch

INDEX = 'legislatives'
TYPE = 'text'

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

ic = IndicesClient(es)

if ic.exists(index=INDEX):
    ic.delete(INDEX)
ic.create(index=INDEX, body={
    "settings": {
        "analysis": {
            "analyzer": {
                "custom_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": [
                        "morfologik_stem",
                        "lowercase"
                    ]
                }
            },
            "filter": {
                "synonyms": {
                    "type": "synonym",
                    "synonyms": [
                        "kpk => kodeks postępowania karnego",
                        "kpc => kodeks postępowania cywilnego",
                        "kk => kodeks karny",
                        "kc => kodeks cywilny",
                    ]
                }
            }
        }
    },
    "mappings": {
        "text": {
            "properties": {
                "text": {
                    "type": "text",
                    "analyzer": "custom_analyzer"
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
            "text": data,
        })

time.sleep(5)

print("Number of legislative acts containing the word ustawa (in any form):\t{}".format(
    es.search(index=INDEX, doc_type=TYPE, body={
        "query": {
            "match": {
                "text": {
                    "query": "ustawa",
                }
            }
        }
    })['hits']['total']))

print("Number of legislative acts containing the words kodeks postępowania cywilnego in the specified order, "
      "but in an any inflection form:\t{}".format(
    es.search(index=INDEX, doc_type=TYPE, body={
        "query": {
            "match_phrase": {
                "text": {
                    "query": "kodeks postępowania cywilnego",
                }
            }
        }
    })['hits']['total']))

print("Number of legislative acts containing the words wchodzi w życie (in any form) allowing for up to 2 additional "
      "words in the searched phrase:\t{}".format(
    es.search(index=INDEX, doc_type=TYPE, body={
        "query": {
            "match_phrase": {
                "text": {
                    "query": "wchodzi w życie",
                    "slop": 2
                }
            }
        }
    })['hits']['total']))

constitutions = sorted(es.search(index=INDEX, body={
    "query": {
        "match": {
            "text": {
                "query": "konstytucja",
            }
        }
    },
    "highlight": {
        "fields": {
            "text": {}
        },
        "number_of_fragments": 3
    }
})['hits']['hits'], key=lambda x: -x["_score"])[:10]

print("most relevant for the phrase konstytucja: \t")

for x in constitutions:
    print("{}:\t{}\t{}".format(x['_id'], x["_score"], x['highlight']['text']))
