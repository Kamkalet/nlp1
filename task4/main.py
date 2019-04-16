import glob
import math

from collections import Counter
from pprint import pprint

from elasticsearch.client import IndicesClient, Elasticsearch

from task4.pim import pmi, llr_compare, llr

INDEX = 'leg'
TYPE = 'diary'

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

ic = IndicesClient(es)

if ic.exists(index=INDEX):
    ic.delete(INDEX)
ic.create(index=INDEX, body={
    "settings": {
        "analysis": {
            "analyzer": {
                "custom_a": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "shingle_filter",
                    ]
                }
            },
            "filter": {
                "shingle_filter": {
                    "type": "shingle"
                }
            }
        }
    },
    "mappings": {
        "diary": {
            "properties": {
                "content": {
                    "term_vector": "yes",
                    "type": "text",
                    "analyzer": "custom_a"
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

vec_list = []

for file_name in list_of_files:
    vec_list.append(es.mtermvectors(index=INDEX, doc_type=TYPE, ids=file_name))

frequencies = {}
for vec in vec_list:
    for diary in vec['docs']:
        items = diary['term_vectors']['content']['terms'].items()

        for key, value in items:
            frequencies[key] = value['term_freq'] if key not in frequencies else frequencies[key] + value['term_freq']

# print(frequencies)

unigrams = {k: v for k, v in frequencies.items() if len(k.split()) == 1}
bigrams = {k: v for k, v in frequencies.items() if len(k.split()) == 2}

unigrams_sum = sum(unigrams.values())
bigrams_sum = sum(bigrams.values())

pointwise_mutual_information = {
    bigram: pmi(
        unigrams[bigram.split()[0]] / unigrams_sum,
        unigrams[bigram.split()[1]] / unigrams_sum,
        v / bigrams_sum)
    for bigram, v in bigrams.items()
}
pmi_list = list(sorted(pointwise_mutual_information.items(), key=lambda kv: kv[1], reverse=True))
print('Pointwise mutual information')
print(pmi_list[:30])

llr_diff = llr_compare(Counter(bigrams), Counter(unigrams))
llr_diff_list = list(sorted(llr_diff.items(), key=lambda kv: kv[1], reverse=True))
print('Log likelihood ratio')
pprint(llr_diff_list[:30])
