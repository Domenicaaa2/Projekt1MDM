from pymongo import MongoClient

def get_documents(mongo_uri, db_name, collection_name):
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]
    documents = list(collection.find())
    return documents

if __name__ == '__main__':
    mongo_uri = 'mongodb+srv://user:pw!@mdm-project.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000'
    db_name = 'mdm-project'
    collection_name = 'listings'

    documents = get_documents(mongo_uri, db_name, collection_name)
    for document in documents:
        print(document)
