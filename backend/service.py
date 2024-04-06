#cd backend
# python -m flask --debug --app service run
import os
import pickle
from pathlib import Path
import pandas as pd
from azure.storage.blob import BlobServiceClient
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from pymongo import MongoClient

model = None

def load_model():
    current_directory = os.path.dirname(__file__)
    model_path = os.path.join(current_directory, '..', 'model', 'GradientBoostingRegressor.pkl')
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    print(f"Model loaded: {type(model)}")
    return model

model = load_model()

# MongoDB-Verbindung herstellen
mongo_uri = os.getenv('MONGO_DB_URI', 'DEIN_STANDARD_MONGODB_URI_HIER')
client = MongoClient(mongo_uri)
db = client['DEIN_DB_NAME_HIER']  # Dein DB-Name
collection = db['DEINE_COLLECTION_NAME_HIER']  # Deine Collection

# Azure Blob Storage Verbindung
AZURE_STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING', 'DEIN_STANDARD_AZURE_STORAGE_CONNECTION_STRING_HIER')
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)


print("*** Init Flask App ***")
app = Flask(__name__)
cors = CORS(app)
app = Flask(__name__, static_url_path='/', static_folder='../frontend/build')


@app.route("/")
def indexPage():
    return send_file("../frontend/build/index.html")
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/api/predict")
def predict():
    global model
    living_space = request.args.get('living_space', type=float)
    floor = request.args.get('floor', type=int)
    rooms = request.args.get('rooms', type=float)

    if model is None:
        return jsonify({"error": "Model not loaded"}), 500

    # Validiere die Eingabeparameter
    if living_space is None or floor is None or rooms is None:
        return jsonify({"error": "Missing parameters"}), 400

    input_data = pd.DataFrame({
        'living_space': [living_space],
        'floor': [floor],
        'rooms': [rooms]
    })

    # Mache eine Vorhersage
    prediction = model.predict(input_data)

    return jsonify({'prediction': prediction})
    

if __name__ == '__main__':
    app.run(debug=True)


    