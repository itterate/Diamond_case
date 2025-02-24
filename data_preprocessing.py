import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import warnings

warnings.simplefilter(action="ignore")

def load_data():
    """Loads and preprocesses the dataset."""
    df = pd.read_excel("data.xlsx")
    train = pd.read_csv("train.csv").drop("Unnamed: 0", axis=1)
    
    # Randomly sample 25% for additional training data
    additional_train = df.sample(frac=0.25)
    additional_train_id = additional_train.ID
    additional_train = additional_train.drop("ID", axis=1)
    df = df.drop(additional_train.index)
    
    # Adjust diamond prices for inflation
    train["Price"] = train["Price"] * 0.76
    train["Price"] = train["Price"] / 1.78
    
    train = pd.concat([train, additional_train])
    
    return df, train

def split_data(df):
    """Splits data into training and test sets."""
    X = df.drop(columns=["Price"])
    y = df["Price"]
    return train_test_split(X, y, test_size=0.2, random_state=42)

if __name__ == "__main__":
    df, train = load_data()
    X_train, X_test, y_train, y_test = split_data(train)
