import pandas as pd
import joblib

# Modell laden
model_path = 'GradientBoostingRegressor.pkl'
model = joblib.load(model_path)

# Manuell definierte Daten
test_data = pd.DataFrame({
    'living_space': [70],  # Beispielwert
    'rooms': [3],          # Beispielwert
    'floor': [2]           # Beispielwert
})

# Vorhersage machen
prediction = model.predict(test_data)
print("Vorhergesagter Preis:", prediction)
