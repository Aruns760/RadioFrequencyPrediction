from pymongo import MongoClient

# MongoDB connection
client = MongoClient(
    "mongodb+srv://arun07:arun123@rf.g6j5gvm.mongodb.net/?appName=RF"
)

# Database
db = client["rf_prediction_db"]

# Collection
collection = db["predictions"]

# Save prediction
def save_prediction(data):

    collection.insert_one(data)

# Get history
def get_history(username):

    return list(
        collection.find(
            {"Username": username},
            {'_id': 0}
        )
    )