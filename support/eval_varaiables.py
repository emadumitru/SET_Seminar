from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression

def get_evaluation_variables():
    param_grids = {
        'RandomForest': {
            'n_estimators': [50, 100, 200, 300],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'bootstrap': [True, False]
        },
        'SVM': {
            'C': [0.1, 1, 10, 100],
            'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
            'gamma': ['scale', 'auto']
        },
        'LogisticRegression': {
            'C': [0.01, 0.1, 1, 10, 100],
            'penalty': ['l2'],
            'max_iter': [100, 200, 300],
            'solver': ['lbfgs']
        }
    }

    test_splits = [0.2, 0.3, 0.4, 0.5]   

    models = {
        'RandomForest': RandomForestClassifier(random_state=17),
        'SVM': SVC(random_state=17),
        'LogisticRegression': LogisticRegression(random_state=17)
    }

    refactorings = ['Inline Method', 'Extract Method', 'Move Class', 'Extract Interface',
                    'Rename Package', 'Pull Up Method', 'Pull Up Attribute', 'Move Attribute',
                    'Move Method', 'Extract Superclass', 'Push Down Attribute', 'Push Down Method']
    
    all_present_actions = ['delete-tree', 'insert-node', 'move-tree', 'delete-node', 'update-node', 'insert-tree']

    return param_grids, test_splits, models, refactorings, all_present_actions

def alternative_grid():
    param_grids = {
        'RandomForest': {'n_estimators': [100, 200], 'max_depth': [None, 10, 20], 'min_samples_split': [2, 5, 10], 'min_samples_leaf': [1, 2, 4]},
        'SVM': {'C': [0.1, 1, 10], 'kernel': ['linear', 'rbf']},
        'LogisticRegression': {'C': [0.1, 1, 10], 'max_iter': [100, 200, 300]}
    }
    return param_grids

def create_path(approach, data_split, data_use, path='results/clustering_results'):
    acc = f'{path}/classification_accuracy_{approach}_{data_split}_{data_use}.txt'
    pick = f'{path}/classification_summary_{approach}_{data_split}_{data_use}.pkl'
    return acc, pick