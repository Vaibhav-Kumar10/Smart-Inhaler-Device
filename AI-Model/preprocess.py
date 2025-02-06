import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

def load_and_preprocess_data(file_path):
    df = pd.read_csv(file_path)

    # Encode categorical 'Season' column
    label_encoder = LabelEncoder()
    df["Season"] = label_encoder.fit_transform(df["Season"])

    # Define features and labels
    X = df.drop(columns=["Risk_Score"])
    y = df["Risk_Score"]

    # Normalize feature data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Split into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test, scaler, label_encoder

def preprocess_new_data(new_data, scaler, label_encoder):
    # Encode categorical 'Season' column
    new_data["Season"] = label_encoder.transform(new_data["Season"])

    # Normalize the data using the existing scaler
    return scaler.transform(new_data)
