import glob
from collections import Counter
from pprint import pprint

from task4.pim import llr_compare

unigrams = {}
bigrams = {}

list_of_files = glob.glob('./*.txt')


def strip_split(line):
    return line.strip().split()


for bill in list_of_files:
    with open(bill, 'r', encoding='utf-8') as processed_bill_file:
        processed_words = [strip_split(line)[0] + ":" + strip_split(line)[1].split(":")[0]
                           for line in processed_bill_file.readlines()
                           if len(line.strip()) > 0
                           and strip_split(line)[-1] == 'disamb'
                           and strip_split(line)[1] != 'interp']

        unigrams.update(Counter(processed_words))
        bigrams = Counter(
            [processed_words[i] + ' ' + processed_words[i + 1] for i in range(0, len(processed_words) - 1)])

noun_classes = ('subst', 'depr', 'num', 'numcol')
adj_classes = ('adj', 'adja', 'adjp', 'adjc')

llr_ratio = llr_compare(Counter(bigrams), Counter(unigrams))
llr_diff_list = list(sorted(llr_ratio.items(), key=lambda kv: kv[1], reverse=True))
filtered_adj_noun = [word for word in llr_diff_list
                     if len(word[0].split()) > 1
                     and word[0].split()[0].split(":")[1] in noun_classes
                     and word[0].split()[1].split(":")[1] in noun_classes + adj_classes][:50]

print('top 50 results including noun at the first position and noun or adjective at the second position')
pprint(filtered_adj_noun)
