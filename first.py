import glob
import regex
import re
import pprint


list_of_files = glob.glob('./ustawy/*.txt')  # create the list of file

bill_dict = {}

for file_name in list_of_files:
    with open(file_name, 'r') as myfile:
        data = myfile.read()

        dict = {}
        aaa = regex.findall(r'(ustaw(?=.{,15} dni).*?(\d{4}) r\..*?)((\(Dz\.U\..*?(poz\. \d*).*?\))|\.)', data, regex.DOTALL)
        print(aaa)
        # for i in aaa:
        #     dict[i] = dict.get(i, 0) + 1
        # dict2 = sorted(dict.items(), key=lambda x: x[1])
        #
        # bill_dict[title] = [myfile.name ,dict2, len(aaa)]
        #
        # myfile.close()

# bill_dict_sorted = sorted(bill_dict.items(), key=lambda x: x[1][2])
#
# pp = pprint.PrettyPrinter(indent=1)
# pp.pprint(bill_dict_sorted)

# FO = open(file_name.replace('txt', 'out'), 'w')


# FO.close()
