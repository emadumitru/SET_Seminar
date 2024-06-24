# Towards Automated Code Refactoring: Validating refactoring presence with abstract syntax trees

## Project Overview

This project explores the use of abstract syntax trees (ASTs) to validate the presence of refactorings between versions of source code files, aiming to develop a language-agnostic identification approach. By implementing AST differencing and machine learning models, the project addresses the need for better refactoring datasets essential for automated refactoring methods. Key findings include:

- Superior performance of sequential approaches that consider the order of edit actions.
- Importance of balanced training data.
- Need for high-quality and well-represented datasets.
- Training models on entries with single labels yielded better results, suggesting that tailored datasets with simpler entries could enhance performance.

Future work should investigate additional programming languages and further validate these approaches.

## Folder Structure

```
SET_SEMINAR/
├── clustereing_split_files
├── data_diffs
├── data_diffs_clean
├── data_initial
├── results
│   ├── clustering_results
│   ├── dataset_results
│   ├── overleaf_plots
│   │   ├── best_results_summary.csv
│   │   ├── classification_summary.csv
│   │   ├── overleaf_distribution_table.tex
│   │   ├── overleaf_gridsearch_table.tex
│   │   ├── overleaf_max_table.tex
├── support
│   ├── __pycache__
│   ├── analysis_data.py
│   ├── analysis_functions.py
│   ├── cleaning_functions.py
│   ├── diffing_functions.py
│   ├── eval_setups.py
│   ├── eval_variables.py
│   ├── github_rethrive.py
│   ├── support_functions.py
├── step1_data_retrival.py
├── step2_data_gumtree_diffing.py
├── step3_data_diff_cleaning.py
├── step4_data_analysis.py
├── step5_clustering.py
├── step6_clustering_analysis.py
```

## Folder explanations
- `data_initial`
    - `code_files`: Results of Step 1 (retreived pairs of source code files)
    - `refactorings.json`: Input for Step 1
- `data_diffs`: Results of Step 2 (ASTs differencing)
- `data_diffs_clean`: Results of step 3 (Data used for Step 5)

## Steps to Run the Project

To run the code, you need to execute steps 1 through 6 in order. The dependencies are already uploaded, so you can also run them independently.

### Step 1: Retrieve Data
Run the script `step1_data_retrival.py` to retrieve the necessary data for the project.

### Step 2: AST Differencing
Run the script `step2_data_gumtree_diffing.py` to perform AST differencing on the retrieved data.

### Step 3: Clean Data
Run the script `step3_data_diff_cleaning.py` to clean the data by deleting match actions.

### Step 4: Dataset Analysis
Run the script `step4_data_analysis.py` to analyze the dataset.

### Step 5: Machine Learning Clustering Implementation
Run the script `step5_clustering.py` to implement machine learning clustering. Note that this step is split into multiple files in the folder `clustereing_split_files` because running step 5 all at once will (probably) take several days to complete.

### Step 6: Result Analysis
Run the script `step6_clustering_analysis.py` to analyze the results of the clustering implementation.

## Results and Findings

The results of the project are stored in the `results` folder, which includes:
- Clustering results
- Dataset results
- Overleaf plots and summaries in CSV and LaTeX formats

## Support Scripts

The `support` folder contains various helper scripts and functions used throughout the project:
- `analysis_data.py`
- `analysis_functions.py`
- `cleaning_functions.py`
- `diffing_functions.py`
- `eval_setups.py`
- `eval_variables.py`
- `github_rethrive.py`
- `support_functions.py`

These scripts provide essential functionalities for data analysis, cleaning, differencing, evaluation setups, and GitHub retrieval.

## About the author

Ema enjoys tea, crocheting, playing DND and reading books, apart from coding like a maniac.

#noprobllamma