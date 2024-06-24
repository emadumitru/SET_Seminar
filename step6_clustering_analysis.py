from support.analysis_functions import load_summaries, extract_all_results, create_aggregate_table, make_overleaf_table, make_overleaf_plots

file_format = 'results\\clustering_results\\classification_summary_{}_{}_{}.pkl'
approaches = ['count', 'countplus', 'ratio', 'ngram']
splits = ['PBS', 'normal', 'SMOTE']
uses = ['single', 'all']

non_viable_options = [file_format.format(approach, split, use) for approach in ['ratio', 'ngram'] for split in ['SMOTE'] for use in uses]
file_paths = [file_format.format(approach, split, use) for approach in approaches for split in splits for use in uses]
file_paths = [file_path for file_path in file_paths if file_path not in non_viable_options]

summaries = load_summaries(file_paths)
summary_df = extract_all_results(summaries)

summary_df.to_csv('results\\classification_summary.csv', index=False)
best_results = create_aggregate_table(summary_df)
best_results.to_csv('results\\best_results_summary.csv', index=False)

make_overleaf_table(best_results, output_file='results\\overleaf_max_table.tex')
make_overleaf_plots(best_results, 'results\\overleaf_plots\\')
