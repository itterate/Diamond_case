from sklearn.ensemble import RandomForestClassifier
from data_processing import load_data, split_data
from utils import analyze_values
from optimize import tune_model  


def train_model(X_train, y_train, best_params=None):
    """Trains a Random Forest model using the best hyperparameters."""
    if best_params is None:
        best_params = {
            "n_estimators": 100,
            "max_depth": None,
            "min_samples_split": 2,
            "min_samples_leaf": 1,
            "max_features": "sqrt",
            "bootstrap": True
        }

    model = RandomForestClassifier(**best_params, random_state=42)
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test):
    """Evaluates the trained model."""
    y_pred = model.predict(X_test)
    

    results = analyze_values(y_test, y_pred)
    print("Results (Percent Lower, Index):", results[:10]) 

if __name__ == "__main__":
   
    df, train = load_data()
    X_train, X_test, y_train, y_test = split_data(train)

    print("\nRunning Optuna hyperparameter tuning...")
    best_params = tune_model(X_train, X_test, y_train, y_test, n_trials=50) 
    print("\nBest hyperparameters found:", best_params)

    print("\nTraining the final model with optimized hyperparameters...")
    model = train_model(X_train, y_train, best_params)  

    print("\nEvaluating the final model...")
    evaluate_model(model, X_test, y_test) 