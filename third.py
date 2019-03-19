import glob
import regex

list_of_files = glob.glob('./ustawy/*.txt')

word_counter = 0
for file_name in list_of_files:
    with open(file_name, 'r') as myfile:
        data = myfile.read()
        bills = regex.findall(r'(?i)(ustaw)(?=(ą|ę|y|a|ie|([ ])|om|ami|ach|o))', data)
        word_counter += len(bills)
        myfile.close()

print(word_counter)
