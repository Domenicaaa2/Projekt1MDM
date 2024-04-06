# new terminal
# cd model
# python model.py -u 'mongodb+srv://user:pw@mdm-project.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000'

import jsonlines
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
import joblib
import seaborn as sns
import matplotlib.pyplot as plt
import os

database_uri = os.getenv('MONGO_DB_URI')

# Funktion zum Laden und Bereinigen der Daten
def load_and_clean_data(file_path):
    data = []
    with jsonlines.open(file_path) as reader:
        for obj in reader:
            data.append(obj)
    df = pd.DataFrame(data)
    
    # Datenbereinigung
    df['rent'] = df['rent'].str.replace(r'[^\d.]', '', regex=True).astype(float)
    df['living_space'] = pd.to_numeric(df['living_space'], errors='coerce')
    df['rooms'] = pd.to_numeric(df['rooms'], errors='coerce')
    
    # Behandlung von 'GF' in der 'floor'-Spalte, ersetze 'GF' durch 0 und konvertiere den Rest in Zahlen
    df['floor'] = df['floor'].replace('GF', 0)
    df['floor'] = pd.to_numeric(df['floor'], errors='coerce')
    
    df.dropna(inplace=True)
    
    return df

# Funktion zum Erstellen der Korrelationsmatrix
def create_correlation_matrix(df):
    plt.figure(figsize=(10, 8))
    corr = df.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.show()

# Hauptfunktion
def main():
    current_directory = os.path.dirname(__file__)
    file_path = os.path.join(current_directory, '..', 'spider', 'file.jl')
    df = load_and_clean_data(file_path)
    
    # Korrelationsmatrix
    create_correlation_matrix(df[['rent', 'living_space', 'rooms']])
    
    # Modelltraining
    X = df[['living_space', 'rooms', 'floor']]  # Füge 'floor' hinzu
    y = df['rent']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = GradientBoostingRegressor(random_state=42)
    model.fit(X_train, y_train)

     

    # Modellbewertung
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")
    

    r2 = model.score(X_test, y_test)
    print(f"R-squared (R²) Score: {r2}")


    # Modell speichern
    joblib.dump(model, 'GradientBoostingRegressor.pkl')
    
    print("Modell wurde erfolgreich gespeichert.")

if __name__ == "__main__":
    main()
