import glob
import regex
import re
import pprint


list_of_files = glob.glob('./ustawy/*.txt')  # create the list of file

bills = []

# didnt sort, simple solution with errors

for file_name in list_of_files:
    with open(file_name, 'r') as myfile:
        data = myfile.read()

        matches = regex.findall(r'(ustaw(?=.{,15} dni).*?(\d{4}).*?r\..*?)(?:\(Dz\.U\..*?(poz\. \d*).*?\)|\.)', data, regex.DOTALL)

        for i in matches:
            bills.append(i)

for i in bills:
    print(str(i) + "\n")