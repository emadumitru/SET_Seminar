import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from support.eval_setups import setup_count, setup_countplus, setup_ratio, setup_ngram
import pandas as pd

#repress user warnings
import warnings
from sklearn.exceptions import ConvergenceWarning
warnings.filterwarnings(action='ignore', category=ConvergenceWarning)
warnings.simplefilter("ignore", UserWarning)

splits = ['PBS', 'normal', 'SMOTE']
uses = ['single', 'all']

folder_path = 'data_diffs_clean\\'
refactoring_df = pd.read_csv('results\\dataset_results\\available_data_distribution.csv')

splits = ['SMOTE']
uses = ['single']

for split in splits:
    for use in uses:
        try:
            print(f'\n\nRunning setups for ratio for {split} and {use}')
            setup_ratio(folder_path, refactoring_df, split, use)
        except Exception as e:
            print(f'Error in ratio for {split} and {use}')
            print(e)