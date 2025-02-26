import numpy as np
import optuna
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

def objective(trial, X_train, X_test, y_train, y_test):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 50, 200),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'min_samples_split': trial.suggest_int('min_samples_split', 2, 20),
        'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 20),
        'max_features': trial.suggest_categorical('max_features', ['auto', 'sqrt', 'log2']),
        'bootstrap': trial.suggest_categorical('bootstrap', [True, False]),
        'max_leaf_nodes': trial.suggest_int('max_leaf_nodes', 10, 1000, step=10)
    }
    
    model = RandomForestRegressor(**params)
    model.fit(X_train, y_train)
    
    pred = model.predict(X_test)
    return np.sqrt(mean_squared_error(y_test, pred))

# Example usage
def tune_model(X_train, X_test, y_train, y_test, n_trials=50):
    study = optuna.create_study(direction='minimize')
    study.optimize(lambda trial: objective(trial, X_train, X_test, y_train, y_test), n_trials=n_trials)
    
    print("Best hyperparameters:", study.best_params)
    return study.best_params
