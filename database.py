import os
import datetime
from deta import Deta
# from dotenv import load_dotenv

# load environment variables
# load_dotenv('.env')
# DETA_KEY = os.getenv('DETA_KEY')
DETA_KEY = 'd0dgr5wqkjz_9nHX6n2aidBvbikx85vUKDY1s1AXyH3S'


# initialize with a project key
# deta = Deta(DETA_KEY)
deta = Deta(DETA_KEY)

# Connect a database
db = deta.Base('authenticator')



def insert_user(username, name, email, hash_password):
    Date_joined = str(datetime.datetime.now())
    return db.put({'key': username, 'name': name, 'email': email, 'password': hash_password, 'DateJoined': Date_joined})

# insert_user('pparker','Peter Parker','abc123')

def fetch_all_users():
    res = db.fetch()
    return res.items


def get_user(username):
    return db.get(username)

def update_user(username,updates):
    return db.update(updates,username)

def delete_user(username):
    return db.delete(username)

# Function to upload an image
def upload_image(file_path, file_name):
    tdb = deta.Base('xray')
    try:
        with open(file_path, 'rb') as file:
            image_data = file.read()
        return db.put({'key': file_name, 'image_data': image_data})
    except Exception as e:
        print(f"Error uploading image: {e}")
        return None




