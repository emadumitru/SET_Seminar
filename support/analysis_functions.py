import pandas as pd
import pickle
import os
import matplotlib.pyplot as plt

def load_summaries(file_paths):
    summaries = []
    for path in file_paths:
        if not os.path.exists(path):
            print(f'File {path} does not exist')
            continue
        with open(path, 'rb') as f:
            summaries.append((path, pickle.load(f)))
    return summaries

def extract_all_results(summaries):
    data = []
    for path, summary in summaries:
        file = path.split('classification_summary_')[1].split('.pkl')[0]
        for ref_type, metrics in summary.items():
            accuracy, tn, tp, fn, fp = metrics
            split = ref_type.split('_', 1)
            ref_type, model_params = split[0], split[1]
            model, split, pos_train, neg_train = model_params.split('_')[:4]
            model_params = model_params.split('_')[4:]
            data.append([ref_type, file, model, split, pos_train, neg_train, accuracy, tn, tp, fn, fp, model_params])

    df_data = pd.DataFrame(data, columns=['Refactoring Type', 'Source File', 'Model', 'Split', 'Pos Train', 'Neg Train', 'Accuracy', 'TN', 'TP', 'FN', 'FP', 'Model Params'])
    df_data['Approach'] = df_data['Source File'].apply(lambda x: x.split('_')[0])
    df_data['Type Split'] = df_data['Source File'].apply(lambda x: x.split('_')[1])
    df_data['Type File'] = df_data['Source File'].apply(lambda x: x.split('_')[2])
    return df_data

def get_next_best_value(df, group_cols, metric_col):
    df_sorted = df.sort_values(by=metric_col, ascending=False)
    for _, row in df_sorted.iterrows():
        if abs(row['TN'] - row['TP']) <= 100:
            return row
    return df_sorted.iloc[0]  # Return the best value if no value meets the condition

def get_max_performance(df):
    best_accuracy_list = []
    best_tn_list = []
    best_tp_list = []

    grouped = df.groupby(['Source File', 'Refactoring Type'])
    for name, group in grouped:
        best_accuracy = get_next_best_value(group, ['Source File', 'Refactoring Type'], 'Accuracy')
        best_tn = get_next_best_value(group, ['Source File', 'Refactoring Type'], 'TN')
        best_tp = get_next_best_value(group, ['Source File', 'Refactoring Type'], 'TP')

        best_accuracy["metric"] = "Accuracy"
        best_tn["metric"] = "TN"
        best_tp["metric"] = "TP"

        best_accuracy_list.append(best_accuracy)
        best_tn_list.append(best_tn)
        best_tp_list.append(best_tp)

    best_accuracy_df = pd.DataFrame(best_accuracy_list)
    best_tn_df = pd.DataFrame(best_tn_list)
    best_tp_df = pd.DataFrame(best_tp_list)

    return best_accuracy_df, best_tn_df, best_tp_df

def round_all_values(df):
    for col in df.columns:
        if col in ['Accuracy', 'TN', 'TP', 'FN', 'FP']:
            df[col] = df[col].round(3)
    return df

def create_aggregate_table(summary_df):
    # Comprehensive Best Results Table
    best_results = get_max_performance(summary_df)
    best_results = pd.concat(best_results).sort_values(['Source File', 'Refactoring Type']).reset_index(drop=True)
    best_results = round_all_values(best_results)
    return best_results

def make_overleaf_table(df, output_file='results\\overleaf_max_table.txt'):
    best_accuracy_data = {}

    # Iterate over the DataFrame to find the best accuracy for each refactoring type
    for _, row in df.iterrows():
        ref_type = row['Refactoring Type']
        source_file = row['Source File']
        source_file = str(source_file).replace('_', ' ')
        metric = row['metric']
        accuracy = row['Accuracy']
        tn = row['TN']
        tp = row['TP']
        model = row['Model']
        
        if metric == 'Accuracy':
            if ref_type not in best_accuracy_data or accuracy > best_accuracy_data[ref_type]['BA']:
                best_accuracy_data[ref_type] = {
                    'Source File': source_file,
                    'BA': accuracy,
                    'TN': tn,
                    'TP': tp,
                    'Model': model
                }

    # Generate LaTeX table content
    table_content = """\\begin{table*}
    \\begin{tabular}{lcccc}
    \\toprule
    Refactoring Type & Approach & BA (\%) & TN (\%) & TP (\%) \\\\
    \\midrule
    """
    models = []

    for ref_type, values in best_accuracy_data.items():
        table_content += f"    {ref_type} & {values['Source File']} & {round(values['BA']*100)} & {values['TN']} & {values['TP']} \\\\\n"
        models.append((ref_type, values['Model']))

    table_content += """    \\bottomrule
    \\end{tabular}
    \\caption{Table of best balanced accuracy (BA), true negative (TN), and true positive (TP) percentages for each refactoring type}
    \\label{tab:refactoring_best_accuracy}\n\\end{table*}
    """

    # Save the table content to a text file
    with open(output_file, 'w') as f:
        f.write(table_content)

    print("LaTeX table content has been written to", output_file)
    print("Models used for best results:", models)

def make_overleaf_plots(df, output_folder='results\\'):
    # Process the data
    def preprocess_data(data):
        data = data[data['metric'] == 'Accuracy']
        return data

    processed_data = preprocess_data(df)
    refactoring_types = processed_data['Refactoring Type'].unique()

    text_folder = output_folder + 'text_summary\\'
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(text_folder, exist_ok=True)

    for refactoring_type in refactoring_types:
        plot_data_by_something(processed_data, 'split', refactoring_type, output_folder)
        plot_data_by_something(processed_data, 'file', refactoring_type, output_folder)
        log_data_by_something(processed_data, 'split', refactoring_type, text_folder)
        log_data_by_something(processed_data, 'file', refactoring_type, text_folder)


def plot_data_by_something(data, type1, refactoring_type, save_path):
    filtered_data = data[data['Refactoring Type'] == refactoring_type]
    n_approach = filtered_data['Approach'].nunique()
    n_type = filtered_data['Type File'].nunique()
    fig, ax = plt.subplots(figsize=(n_approach * n_type, 5))
    x_labels = []

    for i, (_, row) in enumerate(filtered_data.iterrows()):
        approach = row['Approach']
        if approach == 'ratiocount':
            approach = 'count+'
        if approach == 'MEA':
            approach = 'n-gram'
        type_split = row['Type Split']
        type_file = row['Type File']

        if type1 == 'file':
            color = 'orange' if type_file == 'single' else 'blue'
            offset = 0.1 if color == 'orange' else -0.1
        if type1 == 'split':
            color = 'orange' if type_split == 'PBS' else 'blue'
            color = 'pink' if type_split == 'SMOTE' else color
            offset = 0.1 if color == 'orange' else -0.1
            offset = 0.3 if color == 'pink' else offset
        
        tp = row['TP']
        tn = row['TN']
        ba = (row['Accuracy']*100)
        
        # Check condition for transparency or empty circle
        condition_met = abs(tn - tp) == 100
        
        # Plot TP, TN, and Balanced Accuracy (BA) with slight offset for colors
        if type1 == 'file':
            label_pos = f"{approach} {type_split}"
        if type1 == 'split':
            label_pos = f"{approach} {type_file}"
        
        if label_pos not in x_labels:
            x_labels.append(label_pos)
        
        pos = x_labels.index(label_pos)

        ax.plot(pos + offset, tp, '+', markersize=10, color=color)
        ax.plot(pos + offset, tn, '_', markersize=10, color=color)
        
        if condition_met:
            ax.plot(pos + offset, ba, 'o', markersize=10, color=color, markerfacecolor='none')
        else:
            ax.plot(pos + offset, ba, 'o', markersize=10, color=color)
        
        ax.vlines(pos + offset, tp, ba, colors=color, linestyles='dashed', alpha=0.2 if not condition_met else 0.1)
        ax.vlines(pos + offset, tn, ba, colors=color, linestyles='dashed', alpha=0.2 if not condition_met else 0.1)
    
    # Set x-ticks
    ax.set_xticks(range(len(x_labels)))
    ax.set_xticklabels(x_labels, rotation=45, ha='right', fontsize=10)
    
    # Customize the plot
    ax.set_xlabel('Approach')
    ax.set_ylabel('Values')
    ax.set_title(f'{refactoring_type}', fontsize=15)
    plt.tight_layout()

    # Alternating background colors
    for i in range(len(x_labels)):
        if i % 2 == 0:
            ax.axvspan(i - 0.5, i + 0.5, facecolor='lightgrey', alpha=0.2)
        else:
            ax.axvspan(i - 0.5, i + 0.5, facecolor='white', alpha=0.5)

    # Remove grid lines
    ax.grid(False)

    # Transparent background
    fig.patch.set_alpha(0)
    
    # Save the plot
    file_name = f"{type1}_type_{refactoring_type}.png"
    plt.savefig(os.path.join(save_path, file_name))
    plt.close()


def log_data_by_something(data, type1, refactoring_type, save_path):
    filtered_data = data[data['Refactoring Type'] == refactoring_type]
    
    log_lines = []
    x_labels = []

    for i, (_, row) in enumerate(filtered_data.iterrows()):
        approach = row['Approach']
        if approach == 'ratiocount':
            approach = 'count+'
        if approach == 'MEA':
            approach = 'n-gram'
        type_split = row['Type Split']
        type_file = row['Type File']

        if type1 == 'file':
            type_indicator = 'single' if type_file == 'single' else 'all'
        if type1 == 'split':
            type_indicator = 'PBS' if type_split == 'PBS' else 'SMOTE' if type_split == 'SMOTE' else 'normal'

        tp = row['TP']
        tn = row['TN']
        ba = round((row['Accuracy'] * 100))
        
        condition_met = abs(tn - tp) == 100

        if type1 == 'file':
            label_pos = f"{approach} {type_split}"
        if type1 == 'split':
            label_pos = f"{approach} {type_file}"

        if label_pos not in x_labels:
            x_labels.append(label_pos)
        
        pos = x_labels.index(label_pos)

        if condition_met:
            log_line = f"Position: {pos + 1}, Approach: {approach}, Type File: {type_file}, Type Split: {type_split}, TP: {tp}, TN: {tn}, BA: {ba} (all models predict only 1 label)"
        else:
            log_line = f"Position: {pos + 1}, Approach: {approach}, Type File: {type_file}, Type Split: {type_split}, TP: {tp}, TN: {tn}, BA: {ba}"
        
        log_lines.append(log_line)
    
    file_name = f"{type1}_type_{refactoring_type}.txt"
    with open(os.path.join(save_path, file_name), 'w') as file:
        file.write("\n".join(log_lines))