import numpy as np
import pandas as pd
from preprocess import load_and_preprocess_data, preprocess_new_data
from model import build_model, train_model, evaluate_model, predict_risk

if __name__ == "__main__":
    file_path = "data/asthma_data.csv"

    # Load and preprocess the data
    X_train, X_test, y_train, y_test, scaler, label_encoder = load_and_preprocess_data(file_path)

    # Build, train, and evaluate the model
    model = build_model(input_dim=X_train.shape[1])
    train_model(model, X_train, y_train, epochs=50, batch_size=16)
    evaluate_model(model, X_test, y_test)

    # User input for risk prediction
    print("\nEnter new data for asthma risk prediction:")
    AQI = float(input("Enter AQI: "))
    PM2_5 = float(input("Enter PM2.5: "))
    PM10 = float(input("Enter PM10: "))
    Humidity = float(input("Enter Humidity (%): "))
    Temperature = float(input("Enter Temperature (°C): "))
    Season = input("Enter Season (Winter/Spring/Summer/Autumn): ")

    # Convert user input to a DataFrame
    new_data = pd.DataFrame([[AQI, PM2_5, PM10, Humidity, Temperature, Season]], 
                            columns=["AQI", "PM2.5", "PM10", "Humidity", "Temperature", "Season"])
    
    # Preprocess and predict
    scaled_new_data = preprocess_new_data(new_data, scaler, label_encoder)
    risk = predict_risk(model, scaled_new_data)
    
    print(f"\nPredicted Asthma Risk Level: {'High' if risk[0] == 1 else 'Low'}")
