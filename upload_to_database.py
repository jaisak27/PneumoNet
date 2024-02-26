import streamlit_authenticator as sa

import database as db

names = ['Peter Parker','Rebecca Miller','Jai Sakalle','Jatin Ahuja']
usernames = ['pparker','rmiller','jsakalle','jahuja']
passwords = ['abc123','def456','hello123','bye456']




hashed_passwords = sa.Hasher(passwords).generate()

for (username,name,hashed_passwords) in zip(usernames,names,hashed_passwords):
    db.insert_user(username,name,hashed_passwords) 
    