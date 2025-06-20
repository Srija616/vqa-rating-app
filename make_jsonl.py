import csv
import json

input_file = "/mnt/data/users/srija/annotation_app/vqa-rating-app/data_english.csv"
output_file = "/mnt/data/users/srija/annotation_app/vqa-rating-app/data_english.jsonl"

with open(input_file, newline='', encoding='utf-8') as csvfile, open(output_file, 'w', encoding='utf-8') as jsonlfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        json.dump(row, jsonlfile, ensure_ascii=False)
        jsonlfile.write("\n")