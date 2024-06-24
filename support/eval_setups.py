import pickle
from support.support_functions import prepare_data, run_experiments, print_summary, prepare_data_sequences
from support.eval_varaiables import get_evaluation_variables, create_path, alternative_grid


def setup_count(folder_path, refactoring_df, data_split, data_use):
    param_grids, test_splits, models, refactorings, all_present_actions = get_evaluation_variables()
    merged_df = prepare_data(folder_path, refactoring_df, refactorings, all_present_actions)
    data = merged_df, refactorings, models, param_grids, test_splits
    _, cms, accs, summary = run_experiments(data, 'count', data_split, data_use, all_present_actions, minimal=6, random_state=17)
    
    path_acc, path_pick = create_path('count', data_split, data_use, path='results/clustering_results')

    with open(path_pick, 'wb') as f:
        pickle.dump(summary, f)
    with open(path_acc, 'w') as f:
        f.write(str(accs))

    print_summary(accs, cms)

def setup_count_short(folder_path, refactoring_df, data_split, data_use):
    param_grids, test_splits, models, refactorings, all_present_actions = get_evaluation_variables()
    merged_df = prepare_data(folder_path, refactoring_df, refactorings, all_present_actions)
    param_grids = alternative_grid()
    data = merged_df, refactorings, models, param_grids, test_splits
    _, cms, accs, summary = run_experiments(data, 'count', data_split, data_use, all_present_actions, minimal=6, random_state=17)
    
    path_acc, path_pick = create_path('count', data_split, data_use, path='results/clustering_results')

    with open(path_pick, 'wb') as f:
        pickle.dump(summary, f)
    with open(path_acc, 'w') as f:
        f.write(str(accs))

    print_summary(accs, cms)

def setup_countplus(folder_path, refactoring_df, data_split, data_use):
    param_grids, test_splits, models, refactorings, all_present_actions = get_evaluation_variables()
    merged_df = prepare_data(folder_path, refactoring_df, refactorings, all_present_actions)
    data = merged_df, refactorings, models, param_grids, test_splits
    _, cms, accs, summary = run_experiments(data, 'count+', data_split, data_use, all_present_actions, minimal=6, random_state=17)
    
    path_acc, path_pick = create_path('countplus', data_split, data_use, path='results/clustering_results')

    with open(path_pick, 'wb') as f:
        pickle.dump(summary, f)
    with open(path_acc, 'w') as f:
        f.write(str(accs))

    print_summary(accs, cms)

def setup_countplus_short(folder_path, refactoring_df, data_split, data_use):
    param_grids, test_splits, models, refactorings, all_present_actions = get_evaluation_variables()
    merged_df = prepare_data(folder_path, refactoring_df, refactorings, all_present_actions)
    param_grids = alternative_grid()
    data = merged_df, refactorings, models, param_grids, test_splits
    _, cms, accs, summary = run_experiments(data, 'count+', data_split, data_use, all_present_actions, minimal=6, random_state=17)
    
    path_acc, path_pick = create_path('countplus', data_split, data_use, path='results/clustering_results')

    with open(path_pick, 'wb') as f:
        pickle.dump(summary, f)
    with open(path_acc, 'w') as f:
        f.write(str(accs))

    print_summary(accs, cms)

def setup_ratio(folder_path, refactoring_df, data_split, data_use):
    param_grids, test_splits, models, refactorings, all_present_actions = get_evaluation_variables()
    merged_df = prepare_data_sequences(folder_path, refactoring_df, refactorings)
    data = merged_df, refactorings, models, param_grids, test_splits
    _, cms, accs, summary = run_experiments(data, 'ratio', data_split, data_use, all_present_actions, minimal=6, random_state=17)
    path_acc, path_pick = create_path('ratio', data_split, data_use, path='results/clustering_results')

    with open(path_pick, 'wb') as f:
        pickle.dump(summary, f)
    with open(path_acc, 'w') as f:
        f.write(str(accs))

    print_summary(accs, cms)

def setup_ngram(folder_path, refactoring_df, data_split, data_use):
    param_grids, test_splits, models, refactorings, all_present_actions = get_evaluation_variables()
    merged_df = prepare_data_sequences(folder_path, refactoring_df, refactorings)
    data = merged_df, refactorings, models, param_grids, test_splits
    _, cms, accs, summary = run_experiments(data, 'n-gram', data_split, data_use, all_present_actions, minimal=6, random_state=17)
    path_acc, path_pick = create_path('ngram', data_split, data_use, path='results/clustering_results')

    with open(path_pick, 'wb') as f:
        pickle.dump(summary, f)
    with open(path_acc, 'w') as f:
        f.write(str(accs))

    print_summary(accs, cms)