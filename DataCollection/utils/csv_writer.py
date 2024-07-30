import csv
import os
import logging

def write_to_csv(file_path, data, headers):
    log = logging.getLogger(__name__)
    file_exists = os.path.isfile(file_path)
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='|')
        if not file_exists:
            writer.writerow(headers)
        writer.writerows(data)


def update_csv_files(data, csv_files, headers, data_folder):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    for key, rows in data.items():
        file_path = os.path.join(parent_dir, data_folder, csv_files[key])
        write_to_csv(file_path, rows, headers[key])
