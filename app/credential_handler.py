import hashlib
import json


CREDENTIAL_PATH = "data/credentials.json"

def register(username, password) -> bool:
    # Hash the password using a secure hash function (e.g., SHA-256)
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Save the credentials to a JSON file
    with open(CREDENTIAL_PATH, 'r') as file:
        data = json.load(file)
        
        # if username exists
        if data.get(username):
            return False
        else:
            data[username] = hashed_password

    with open(CREDENTIAL_PATH, 'w') as file:
        json.dump(data, file)
    return True

def check_credentials(username, password):
    # Load the credentials from the JSON file
    with open(CREDENTIAL_PATH, 'r') as file:
        data = json.load(file)

    # Check if the username exists
    if username in data:
        # Check if the hashed password matches
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if data[username] == hashed_password:
            return True

    return False
