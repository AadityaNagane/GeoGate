import streamlit as st
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import auth
import json
import requests
import folium
from streamlit_folium import folium_static

cred = credentials.Certificate("D:/SPIT/SEM 4/microproject/miniprojectfrontend/Basic Program/Key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
collection_name = ''
document_id = ''


def app():
    st.title(':violet[GeoGate]')

    if "signedout" not in st.session_state:
        st.session_state["signedout"] = False
    if 'signout' not in st.session_state:
        st.session_state['signout'] = False

    if not st.session_state["signedout"]:
        choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])

        if choice == 'Sign up':
            signup_page()
        else:
           login_page()
            


if __name__ == "__main__":
    app()

            
def signup_page():
    
    optionstates = [
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
        "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
        "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
        "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
        "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"
    ]

    # Input fields for user registration
    username_signup = st.text_input("Username", placeholder="Enter your username",key="username_signup")
    name= st.text_input("Name",key="name")
    state = st.selectbox('Select an Option', optionstates, key='og')
    email = st.text_input("Email", placeholder="Enter your email")
    numberplate= st.text_input("Number Plate")
    rcnum =st.text_input("RC Number")
    password_signup = st.text_input("Password", type="password", placeholder="Enter your password",key="password_signup")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password", key="con_password_signup")

    # Center align the input fields and the button
    st.markdown(
        """
        <style>
        .stTextInput {
            text-align: center;
        }
        .stButton>button {
            width: 100%;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Sign up button
    if st.button("Sign Up"):
        if password_signup == confirm_password:
            # You can perform signup logic here, such as adding the user to a database
            st.success("You have successfully signed up!")
            st.write(f"Username: {username_signup}")
            st.write("You can now login.")
            db.collection(username_signup).document("signup"). set({'Name':name, 'Numberplate':numberplate,'RC Number':rcnum, 'State':state, 'Password':password_signup})
            db.collection(username_signup).document("geopoint"). set({'latitude': '23', 'longitude': '72'})
        else:
            st.error("Passwords do not match.")

def login_page():
    # Center align the input fields and the button
    st.markdown(
        """
        <style>
        .stTextInput {
            text-align: center;
        }
        .stButton>button {
            width: 100%;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    collections = db.collections()

    #Get all collections in the Firestore database
    collections = [collection.id for collection in db.collections()]

    # Print the names of all collections
    username_login = st.text_input("Username", placeholder="Enter your username", key="username_login")
    password_login = st.text_input("Password", type="password", placeholder="Enter your password", key="password_login")

    if st.button("Login"):
        if username_login in collections:  # Check if the username exists in collections
            # Reference to the specific document
            doc_ref = db.collection(username_login).document("signup")
            doc = doc_ref.get()
            if doc.exists:
                data = doc.to_dict()
                stored_password = data.get("Password")
                if stored_password == password_login:
                    st.success('Logged in successfully')
                else:
                    st.error('Incorrect Password')
            else:
                st.error("User not found. Please sign up.")
        else:
            st.error("Username not found. Please sign up.")
