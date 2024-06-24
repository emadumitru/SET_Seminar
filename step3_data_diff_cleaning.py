from support.cleaning_functions import filter_match_actions

input_dataset_dir = "data_diffs"
output_dataset_dir = "data_diffs_clean"

filter_match_actions(input_dataset_dir, output_dataset_dir)
