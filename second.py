import glob
import regex
import re
import pprint


list_of_files = glob.glob('./ustawy/*.txt')  # create the list of file

bill_dict = {}

for file_name in list_of_files:
    with open(file_name, 'r') as myfile:
        data = myfile.read()

        ## regex to extract the title of the bill
        title_match = regex.search(r'(?i)U[ ]*S[ ]*T[ ]*A[ ]*W[ ]*A.*?(?=[ \t\r\n\f]*(Rozdział|Art.*?\d*\.))', data,
                                   regex.DOTALL)

        ## when no bill is present in the file
        if title_match is None:
            continue

        title = " ".join(str(title_match[0]).split())

        regulation_to_counter_map = {}
        matches = regex.findall(r'(art)\.*? (\d*) .{,9}(ust)\.* ? (\d *)', data, regex.DOTALL)
        for i in matches:
            regulation_to_counter_map[i] = regulation_to_counter_map.get(i, 0) + 1
        dict2 = sorted(regulation_to_counter_map.items(), key=lambda x: x[1])

        bill_dict[title] = [myfile.name , dict2, len(matches)]

        myfile.close()

bill_dict_sorted = sorted(bill_dict.items(), key=lambda x: x[1][2])

pp = pprint.PrettyPrinter(indent=1)
pp.pprint(bill_dict_sorted)

