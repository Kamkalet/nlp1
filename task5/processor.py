import glob
import requests

list_of_files = glob.glob('../ustawy/*.txt')  # create the list of file

print("loading files....")


def parse_file_name_from_file_path(path):
    return path.rsplit('/', 1)[1]


for file_name in list_of_files:
    with open(file_name, 'r') as bill_file:
        with open(parse_file_name_from_file_path(file_name), 'w') \
                as processed_bill_file:
            data = bill_file.read()
            response = requests.post('http://localhost:9200',
                                     data=data.lower().replace("[^\w\s]+", " ").encode('utf-8'))
            processed_bill_file.write(response.text)

            bill_file.close()
            processed_bill_file.close()

print("bills processed")
