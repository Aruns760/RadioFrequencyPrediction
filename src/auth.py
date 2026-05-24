from pymongo import MongoClient
import bcrypt

# MongoDB connection
client = MongoClient(
    "mongodb+srv://arun07:arun123@rf.g6j5gvm.mongodb.net/?appName=RF"
)

db = client["rf_prediction_db"]

users_collection = db["users"]

# Register user
def register_user(username, password):

    # Check existing user
    existing_user = users_collection.find_one({
        "username": username
    })

    if existing_user:
        return False

    # Hash password
    hashed_password = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    )

    # Save user
    users_collection.insert_one({
        "username": username,
        "password": hashed_password
    })

    return True

# Login user
def login_user(username, password):

    user = users_collection.find_one({
        "username": username
    })

    if user:

        if bcrypt.checkpw(
            password.encode('utf-8'),
            user["password"]
        ):

            return True

    return False