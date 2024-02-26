import pickle
from pathlib import Path

import streamlit_authenticator as sa

names = ['Peter Parker','Rebecca Miller']
usernames = ['pparker','rmiller']
passwords = ['abc123','def456']


hashed_passwords = sa.Hasher(passwords).generate()

file_path = Path(__file__).parent / 'hashed_pw.pkl'
with open('hashed_pw.pkl', "wb") as file:
    pickle.dump(hashed_passwords,file)