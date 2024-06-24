import json
import os
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter, defaultdict
from support.eval_varaiables import alternative_grid, get_evaluation_variables

def load_data(initial_path, diffs_path):
    # Load original data
    with open(initial_path, 'r') as file:
        full_data = json.load(file)
    data_pre = {str(ref['id']): [refactoring['type'] for refactoring in ref['refactorings']] for ref in full_data}

    # Load retrieved data
    ids_post = [file.split('_')[0] for file in os.listdir(diffs_path) if file.endswith('_diff.md')]
    data_post = {file_id: data_pre[file_id] for file_id in ids_post}

    return data_pre, data_post

def analyze_data(data):
    details_by_id = defaultdict(Counter)
    single_refactoring = Counter()
    multiple_refactoring = Counter()
    total_refactoring_count = Counter()
    
    for ref_id, refactorings in data.items():
        types = set(refactorings)
        details_by_id[ref_id].update(refactorings)
        if len(types) == 1:
            single_refactoring[list(types)[0]] += 1
        else:
            for ref_type in types:
                multiple_refactoring[ref_type] += 1
        for ref_type in types:
            total_refactoring_count[ref_type] += 1
            
    return single_refactoring, multiple_refactoring, total_refactoring_count, details_by_id

def prepare_combined_data(orig_single, orig_multiple, orig_total, retr_single, retr_multiple, retr_total):
    single_types_combined = pd.DataFrame({'Original Single': orig_single, 'Retrieved Single': retr_single}).fillna(0)
    multiple_types_combined = pd.DataFrame({'Original Mixed': orig_multiple, 'Retrieved Mixed': retr_multiple}).fillna(0)
    total_types_combined = pd.DataFrame({'Original Total': orig_total, 'Retrieved Total': retr_total}).fillna(0)
    
    combined_data = pd.concat([total_types_combined, multiple_types_combined, single_types_combined], axis=1)
    return combined_data, single_types_combined, multiple_types_combined, total_types_combined

def save_combined_data(combined_data, output_dir, filename):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    combined_data.to_csv(os.path.join(output_dir, filename))

def add_labels(ax, show_values=True):
    if show_values:
        for p in ax.patches:
            _x = p.get_x() + p.get_width() / 2
            _y = p.get_y() + p.get_height()
            value = int(p.get_height())
            ax.text(_x, _y, value, ha="center")

def plot_data(df, title, filename, output_dir):
    ax = df.plot(kind='bar', figsize=(10, 6))
    ax.set_title(title)
    ax.set_ylabel('Count')
    plt.xticks(rotation=45)
    add_labels(ax)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, filename))

def save_text_summary(single_types_combined, multiple_types_combined, total_types_combined, output_dir, filename):
    summary_path = os.path.join(output_dir, filename)
    with open(summary_path, 'w') as file:
        file.write("Analysis Summary of Refactoring Types\n")
        file.write("Single Refactoring Types:\n")
        file.write(single_types_combined.to_string() + "\n")
        file.write("Mixed Refactoring Types:\n")
        file.write(multiple_types_combined.to_string() + "\n")
        file.write("Total Refactoring Types:\n")
        file.write(total_types_combined.to_string() + "\n")

def save_refactorings_distribution(details_post, data_post, output_dir, filename):
    refactorings = ['Inline Method', 'Extract Method', 'Move Class', 'Extract Interface',
                    'Rename Package', 'Pull Up Method', 'Pull Up Attribute', 'Move Attribute',
                    'Move Method', 'Extract Superclass', 'Push Down Attribute', 'Push Down Method']
    post_df = {file_id: [details_post[file_id][ref] for ref in refactorings] for file_id in data_post.keys()}
    post_df = pd.DataFrame(post_df, index=refactorings).T
    post_df.to_csv(os.path.join(output_dir, filename))
    post_df = pd.read_csv(os.path.join(output_dir, filename)).rename(columns={'Unnamed: 0': 'id'})
    post_df.to_csv(os.path.join(output_dir, filename), index=False)

def generate_latex_table(csv_path, output_dir, output_filename):
    df = pd.read_csv(csv_path)
    # sort df by Retrieved Total
    df = df.sort_values(by='Retrieved Total', ascending=False)
    
    latex_table = "\\begin{table*}\n"
    latex_table += "    \\begin{tabular}{lcccccc}\n"
    latex_table += "    \\toprule\n"
    latex_table += "    Refactoring Type & Original Total & Retrieved Total & Original Mixed & Retrieved Mixed & Original Single & Retrieved Single\\\\\n"
    latex_table += "    \\midrule\n"

    for index, row in df.iterrows():
        latex_table += f"    {row['Unnamed: 0']} & {int(row['Original Total'])} & {int(row['Retrieved Total'])} & {int(row['Original Mixed'])} & {int(row['Retrieved Mixed'])} & {int(row['Original Single'])} & {int(row['Retrieved Single'])}\\\\\n"

    latex_table += "    \\bottomrule\n"
    latex_table += "    \\end{tabular}\n"
    latex_table += "    \\caption{Table of available and retrieved data}\n"
    latex_table += "    \\label{tab:data}\n"
    latex_table += "\\end{table*}\n"

    output_path = os.path.join(output_dir, output_filename)
    with open(output_path, 'w') as file:
        file.write(latex_table)
    
    print(f"LaTeX table saved to {output_path}")

def create_overleaf_table_GS(output_path):
    param_grids = get_evaluation_variables()[0]
    param_grids_2 = alternative_grid()
    model_name_dict = {'RandomForest': 'RF', 'SVM': 'SVM', 'LogisticRegression': 'LR'}
    def underline_if_present(value, param_name, model_name):
        if param_name in param_grids_2[model_name] and value in param_grids_2[model_name][param_name]:
            return f"\\underline{{{value}}}"
        return value

    table_text = """
    \\begin{table}
        \\begin{tabular}{lll}
        \\toprule
        Model & Parameter & Values \\\\
        \\midrule
    """
    
    for model_name, params in param_grids.items():
        for param_name, values in params.items():
            values_text = ', '.join([str(underline_if_present(v, param_name, model_name)) for v in values])
            model = model_name_dict[model_name]
            param = str(param_name).replace('_', '\\_')
            table_text += f"        {model} & {param} & {values_text} \\\\\n"
    
    table_text += """
        \\bottomrule
        \\end{tabular}
        \\caption{Hyperparameter grids. Underlined values are present in the reduced parameter grid as well.}
        \\label{tab:grid_params}
    \\end{table}
    """
    
    with open(output_path, 'w') as file:
        file.write(table_text)

