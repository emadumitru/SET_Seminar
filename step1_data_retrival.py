from support.github_rethrieve import process_refactorings  
import json

hidden = 'ghp_l4QNDIKcHnJYhyqT -- gY0RN4nnlOiPkE2b22RI'
access_token = hidden.replace(' -- ', '')

json_path = 'data_initial\\refactorings.json'
output_dir = 'data_initial\\code_files'
failed_ids, access_errors, successful_ids = process_refactorings(json_path, output_dir, access_token)

with open('data_initial/failed_ids_silva.json', 'w') as json_file:
    json.dump(failed_ids, json_file)
with open('data_initial/access_errors_silva.json', 'w') as json_file:
    json.dump(access_errors, json_file)
with open('data_initial/successful_ids_silva.json', 'w') as json_file:
    json.dump(successful_ids, json_file)