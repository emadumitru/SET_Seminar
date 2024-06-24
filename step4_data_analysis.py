import os
from support.analysis_data import load_data, analyze_data, prepare_combined_data, save_combined_data, plot_data, save_text_summary, save_refactorings_distribution, generate_latex_table, create_overleaf_table_GS

initial_path = 'data_initial\\refactorings.json'
diffs_path = 'data_diffs_clean\\'
output_dir = 'results\\dataset_results\\'
output_dir_overleaf = 'results\\'

data_pre, data_post = load_data(initial_path, diffs_path)
print('Original number of files:', len(data_pre))
print('Available number of files:', len(data_post))
print('Missing files %:', round((len(data_pre) - len(data_post)) / len(data_pre) * 100))
print('Available files %:', round(len(data_post) / len(data_pre) * 100))

orig_single, orig_multiple, orig_total, details_pre = analyze_data(data_pre)
retr_single, retr_multiple, retr_total, details_post = analyze_data(data_post)

combined_data, single_types_combined, multiple_types_combined, total_types_combined = prepare_combined_data(
    orig_single, orig_multiple, orig_total, retr_single, retr_multiple, retr_total)

save_combined_data(combined_data, output_dir, 'combined_refactoring_analysis.csv')

plot_data(single_types_combined, 'Count of Files with Single Refactoring Type', 'single_refactoring_types.png', output_dir)
plot_data(multiple_types_combined, 'Count of Files with Mixed Refactoring Types', 'mixed_refactoring_types.png', output_dir)
plot_data(total_types_combined, 'Total Refactoring Types Count', 'total_refactoring_types.png', output_dir)

save_text_summary(single_types_combined, multiple_types_combined, total_types_combined, output_dir, 'analysis_summary.txt')
save_refactorings_distribution(details_post, data_post, output_dir, 'available_data_distribution.csv')
generate_latex_table(os.path.join(output_dir, 'combined_refactoring_analysis.csv'), output_dir_overleaf, 'overleaf_distribution_table.tex')
create_overleaf_table_GS(os.path.join(output_dir_overleaf, 'overleaf_gridserach_table.tex'))

print(os.listdir(output_dir))
