# pylint: disable=trailing-whitespace
import streamlit as st
import streamlit_authenticator as sa

import tensorflow as tf
import matplotlib.pyplot as plt
import cv2
import os
from PIL import Image
from keras.preprocessing.image import load_img,img_to_array
import numpy as np 
from keras.models import load_model 
import re
import openai


import validate_email_address
import database as db
import pandas as pd
# import requests
# from bs4 import BeautifulSoup    
# import pickle 
# from pathlib import Path





model = load_model("PneumoNet.h5")

yes = '''Oh no!,you are  ***Infected !!***
         Please consult a doctor.'''
no = '''Relax,you are  ***Normal***
         Please consult a doctor if you feel uneasy.'''
         
def processed_img(img_path):
    testing = cv2.imread(img_path)
    # plt.imshow(testing)
    # plt.show()

    resize= tf.image.resize(testing, (256,256))
    yhat= model.predict(np.expand_dims((resize/255),0))
    # yhat
    if yhat > 0.5:
        return yes
    return no
    
def validate_username(username):
    pattern = "^[a-zA-Z0-9]*$"
    if re.match(pattern,username):
        return True
    return False


st.set_page_config(page_title = 'PneumoNet',layout="centered")

page_element="""
<style>
[data-testid="stAppViewContainer"]{
  background-image: url("https://img.freepik.com/free-vector/medical-technology-science-background-vector-blue-with-blank-space_53876-117739.jpg?size=626&ext=jpg&ga=GA1.1.386372595.1697587200&semt=ais");
  background-size: cover;
  
}
[data-testid="stHeader"]{
  background-color: rgba(0,0,0,0);
} 
</style>

<script>
[data-testid="stSidebar"]> div:first-child{
background-image: url("https://mcdn.wallpapersafari.com/medium/89/87/X7GDE5.jpg");
background-size: cover;
}
</script>
"""
st.markdown(page_element, unsafe_allow_html=True)



st.image("logo1.png", width=150)
st.title('PneumoNet')
st.subheader('Accuracy. Efficiency. Lung Wellness.')




# user authentication -------------- 
# names = ['Peter Parker','Rebecca Miller']
# usernames = ['pparker','rmiller']
# passwords = ['abc123','def456']


users = db.fetch_all_users() 
usernames = [user['key']for user in users]
names = [user['name']for user in users]
hashed_passwords = [user['password']for user in users]


credentials = {
    "usernames": {user['key']: {"name": user['name'],
    "password": user['password']} for user in users}
}

# credentials = {
#         "usernames":{
#             usernames[0]:{
#                 "name":names[0],
#                 "password":hashed_passwords[0]
#                 },
#             usernames[1]:{
#                 "name":names[1],
#                 "password":hashed_passwords[1]
#                 }            
#             }
#         }



# load hash passwords
# file_path = Path(__file__).parent / 'hashed_pw.pkl'
# with open('hashed_pw.pkl', "rb") as file:
#     hashed_passwords = pickle.load(file)




authenticator = sa.Authenticate(credentials, "Login", "auth", cookie_expiry_days=1)


    
# authenticator = sa.Authenticate(names,usernames,hashed_passwords,'Upload Here','abcdef',cookie_expiry_days = 30)
def signup():
    with st.form(key='Signup', clear_on_submit=True):
        st.subheader(":green[Sign Up]")

        name = st.text_input(":blue[Name]", placeholder="Enter Your Full Name")
        email = st.text_input(":blue[Email]", placeholder="Enter your Email")
        username = st.text_input(":blue[Username]", placeholder="Enter your Username")
        password = st.text_input(":blue[Password]", type="password", placeholder="Enter your Password")
        confirm_password = st.text_input(":blue[Confirm Password]", type="password", placeholder="Confirm your Password")

        if email:
            if not validate_email_address.validate_email(email):
                st.warning('Invalid Email. Please enter a valid email address.')
                st.stop()
        
        if username:
            if validate_username(username):
                if username not in usernames:
                    if len(username) >= 2:
                        if password == confirm_password:
                            hashed_passwords = sa.Hasher([confirm_password]).generate()
                            db.insert_user(username, name, email, hashed_passwords[0])
                            st.success("Account Successfully Created!!")
                        else:
                            st.warning("Passwords do not match.")
                    else:
                        st.warning("Username should be at least 2 characters long.")
                else:
                    st.warning('Username already exists!!')
            else:
                st.warning('Invalid Username. Please try again.')
        st.form_submit_button('Signup')

                   
authentication_status = None
if not authentication_status:
    menu = ["Log In","Sign Up"]
    abc = st.selectbox('Log In/Sign Up',menu)
    if abc == 'Log In':
        name,authentication_status,username = authenticator.login(':green[Login]','main')
    else:
        signup()

    if authentication_status == False:    
        st.error('Username/Password is incorrect')  
        
    if authentication_status == None:
        st.warning('Please enter your username and password')


if authentication_status:
    st.success(f"Hi!, Welcome to PneumoNet!")
    # run main code
    # Navigation bar
    st.sidebar.title(f"Welcome {name}")
    selected_option = "Home"
    selected_option = st.sidebar.radio("", ["Home","About Us","Contact Us"])
    authenticator.logout("Log Out","sidebar") 

    if selected_option == "Home":
        st.subheader("Upload Your Image")

        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

        # if uploaded_file is not None:
        # idhar se integration ka code....................
        if uploaded_file is not None:    
            # st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            img = Image.open(uploaded_file).resize((255,255))
            st.image(img,use_column_width=False)
            save_image_path = './upload_images/' + uploaded_file.name
            with open(save_image_path,'wb') as f:
                f.write(uploaded_file.getbuffer())
                
        # if uploaded_file is not None:
        #     st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        #     bytes_data = uploaded_file.getvalue()
        #     img_fn = uploaded_file.name
        #     db.upload_image(bytes_data,img_fn)
             
            if uploaded_file is not None:
                result = processed_img(save_image_path)
                if result == yes:
                    st.error(result)
                    multiline_markdown = '''
                    Pneumonia is an inflammatory lung condition that primarily affects the air sacs in one or both lungs. It can be caused by various microorganisms, including bacteria, viruses, fungi, or other pathogens. Here's a brief overview:

                    1. *Causes*: 
                    - *Bacterial Pneumonia*: Typically caused by bacteria like Streptococcus pneumoniae.
                    - *Viral Pneumonia*: Commonly caused by influenza (flu) viruses or respiratory syncytial virus (RSV).
                    - *Fungal Pneumonia*: Less common, often seen in people with weakened immune systems.
                    - *Aspiration Pneumonia*: Occurs when foreign substances are inhaled into the lungs, like stomach contents or food.

                    2. *Symptoms*: Common symptoms include fever, cough with phlegm, difficulty breathing, chest pain, fatigue, and confusion, especially in older adults.

                    3. *Prevention*:
                    - *Vaccination*: Getting vaccinated against common pathogens like S. pneumoniae and influenza can reduce the risk.
                    - *Hand Hygiene*: Regular handwashing helps prevent the spread of infections.
                    - *Avoid Smoking*: Smoking damages the lungs and makes you more susceptible.
                    - *Good Respiratory Hygiene*: Covering your mouth and nose when sneezing or coughing helps prevent the spread of respiratory infections.
                    - *Stay Healthy*: Maintaining overall health through a balanced diet and regular exercise can bolster your immune system.

                    4. *Medications*:
                    - *Antibiotics*: Bacterial pneumonia is treated with antibiotics prescribed by a doctor.
                    - *Antiviral Medications*: If the cause is viral (e.g., influenza), antiviral drugs may be used.
                    - *Antifungal Medications*: For fungal pneumonia, antifungal drugs are prescribed.
                    - *Supportive Care*: Over-the-counter medications for fever and pain, along with plenty of rest and fluids, can help manage symptoms.

                    It's crucial to consult a healthcare professional for a proper diagnosis and treatment plan if you suspect pneumonia. In severe cases, hospitalization may be necessary, especially for older adults, young children, or individuals with weakened immune systems.'''
                    st.markdown(multiline_markdown)  
                else:
                    st.success(result)
            st.button("Print Report")
        
                
    elif selected_option == "About Us":
        st.write("Use the navigation bar on the left to upload an image.")
        multiline_markdown = """
            #### About Us - PneumoNet: Your Trusted Pneumonia Detection Resource

        Welcome to PneumoNet, your premier destination for cutting-edge pneumonia detection and information. Founded by a passionate team of interns interning at Infosys, PneumoNet was born out of a shared commitment to harness technology for the betterment of healthcare and to make a positive impact on people's lives.

        ##### Our Journey:

        PneumoNet was conceived during our internship at Infosys, where we realized the immense potential of artificial intelligence and machine learning in revolutionizing healthcare diagnostics. Witnessing the global impact of pneumonia and its toll on individuals and healthcare systems, we embarked on a mission to create a user-friendly, accessible, and accurate platform for pneumonia detection.

        ##### Our Vision:

        At PneumoNet, we envision a world where early pneumonia detection is as easy as a click of a button. Our goal is to provide individuals and healthcare professionals with a powerful tool to swiftly identify and manage pneumonia cases, ultimately improving patient outcomes and reducing the burden on healthcare systems.

        ##### What Sets Us Apart:

        1. **Advanced AI Technology:** PneumoNet utilizes state-of-the-art artificial intelligence and machine learning algorithms to analyze chest X-rays and CT scans with unparalleled accuracy. Our innovative approach ensures reliable results for both healthcare professionals and individuals.

        2. **User-Friendly Interface:** We understand the importance of simplicity and accessibility. Our website is designed with user-friendliness in mind, making it easy for anyone to upload images and receive prompt results.

        3. **Educational Resources:** PneumoNet is not just a diagnostic tool; it's also a valuable resource hub. We provide comprehensive information about pneumonia, its causes, symptoms, and prevention, empowering individuals to take charge of their health.

        4. **Data Security:** Your privacy and data security are paramount to us. PneumoNet adheres to stringent data protection measures to ensure your information remains confidential and secure.

        ##### Join Us in the Fight Against Pneumonia:

        PneumoNet is more than just a website; it's a community-driven initiative aimed at combating pneumonia worldwide. We invite healthcare professionals, researchers, and individuals to partner with us in this noble cause. Together, we can raise awareness, promote early detection, and contribute to a healthier future for all.

        """
            
        st.markdown(multiline_markdown) 

    elif selected_option == "Contact Us":
        multiline_markdown = """
        #### Contact us

        Have questions, suggestions, or feedback? Feel free to reach out to us anytime. We value your input and look forward to collaborating with you.

        Thank you for choosing PneumoNet as your trusted pneumonia detection resource. Together, we can make a difference in the fight against pneumonia and improve healthcare outcomes for everyone.

        PneumoNet - Pioneering Pneumonia Detection for a Healthier Tomorrow!


        - Jai Sakalle
        - Jatin Ahuja
        - Akash Kacchaway
        - Nikhil Chakravarthy
        
        """

        st.markdown(multiline_markdown)
    
