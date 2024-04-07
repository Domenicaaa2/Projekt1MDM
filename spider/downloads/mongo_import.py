# new terminal
# cd spider/downloads
# python .\mongo_import.py -c tracks -i ../file.jl -u 'mongodb+srv://user:pw@mdm-project.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000'

import jsonlines
import os
from pymongo import MongoClient

def clean_data(item):
    # Prüft, ob die erforderlichen Felder vorhanden sind
    required_fields = ['rent', 'floor', 'rooms', 'living_space']
    if not all(field in item for field in required_fields):
        return None

    # Bereinige die Daten
    item['rent'] = float(item['rent'].replace(',', '').replace('–', '').strip())
    item['living_space'] = int(item['living_space'])
    item['rooms'] = float(item['rooms'])
    if item['floor'] == 'GF':
        item['floor'] = 0
    else:
        try:
            item['floor'] = int(item['floor'])
        except ValueError:
            item['floor'] = None  

    return item

def save_to_mongodb(file_path, mongo_uri, db_name, collection_name):
    mongo_uri = os.getenv('MONGO_DB_URI')
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]
    documents = []

    with jsonlines.open(file_path) as reader:
        for item in reader:
            cleaned_item = clean_data(item)
            if cleaned_item:
                documents.append(cleaned_item)

    if documents:
        collection.insert_many(documents)
        print(f"{len(documents)} Dokumente wurden in {db_name}.{collection_name} gespeichert.")
    else:
        print("Keine Dokumente zum Speichern gefunden.")

if __name__ == '__main__':
    current_directory = os.path.dirname(__file__)
    file_path = os.path.join(current_directory, '..', 'spider', 'file.jl')
    mongo_uri = os.getenv('MONGO_DB_URI')  # Stellt sicher, dass dies der korrekte Schlüsselname in deinen GitHub Secrets ist
    db_name = 'mdm-project'
    collection_name = 'listings'

    # Richtig: Die Reihenfolge der Argumente muss wie in der Funktionsdefinition sein
    save_to_mongodb(file_path, mongo_uri, db_name, collection_name)

