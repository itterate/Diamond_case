from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from data_processing import load_data, split_data

def train_model(X_train, y_train):
    """Trains a Random Forest model."""
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """Evaluates the trained model."""
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    df, train = load_data()
    X_train, X_test, y_train, y_test = split_data(train)
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)
