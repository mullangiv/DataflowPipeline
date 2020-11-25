import streamlit as st
import numpy as np
import pandas as pd
import time
from PIL import Image
import json,requests
#verified = "False"

def streamAction(chosenRadioButton, verified):
    if chosenRadioButton == 'Scrape Data':
        st.title('_**Scrape Data**_')
        st.markdown('**URL**')
        userUrlIP = st.text_input('Please enter the source URL below')
    if st.button('Scrap'):
            payload = json.dumps({
                "link" : sentence
                })
            response = requests.get(f"http://127.0.0.1:8000/scrap?enterurl={userUrlIP}")
            data_list = response.json()
            st.subheader("Scrapping Completed")
    st.subheader('_Click on the display button to view_')
    if st.button('Display'):
            response = requests.get(f"http://127.0.0.1:8000/displayscrapdata")
            data_list = response.json()
            st.subheader(data_list)  
                
    if chosenRadioButton == 'Identify Entities':
        st.title('_Press to identify entities_')
        if st.button('Identify Entities'):
                response = requests.get(f"http://127.0.0.1:8000/identifyEntity")
                data_list = response.json()           
                st.title(data_list)

    if chosenRadioButton == 'MaskEntities':
        st.title('_MaskEntities_')
        st.write('_Press to to MaskEntities_')
        if st.button('MaskEntities'):
                response = requests.get(f"http://127.0.0.1:8000/maskEntity")
                data_list = response.json()
                st.title(data_list)

    if chosenRadioButton == 'DeIdentifyEntities':   
        st.title('_DeIdentify Entities_')
        st.write('_Press to DeIdentifyEntities_')
        if st.button('DeIdentifyEntities'):
                response = requests.get(f"http://127.0.0.1:7777/deIdentifyEntities?JobName=abcd&verified={verified}")
                data_list = response.json()
                st.title(data_list)
                
    if chosenRadioButton == 'Authentication':    
        st.title('User Authentication')
        st.subheader('_**Please Enter Your Login Details Below**_')
        username = st.text_input('Username')
        password = st.text_input('Password')
        if st.button('Authenticate'):
                response = requests.get(f"http://127.0.0.1:7777/Authentication?usrName=username&usrPassword=password")
                data_list = response.json()
                verified = data_list
                print(verified)
                if verified == True:
                    data_list = "Authenticated Successfully"
                    st.subheader(data_list)
                else:
                    data_list = "Invalid Username/Password Combination"
                    st.subheader(data_list)
                return verified 

    if chosenRadioButton == 'ReIdentifyEntities':   
        st.title('_ReIdentify Entities_')
        st.write('_Press to ReIdentifyEntities_')
        if st.button('ReIdentifyEntities'):
                response = requests.get(f"http://127.0.0.1:8000/reIdentifyEntities")
                data_list = response.json()
                st.title(data_list)




if __name__ == "__main__":
    verified = False
    st.sidebar.markdown('**PII and PHI Data Scrubbing Service**')
    st.write('<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    chosenRadioButton = st.sidebar.radio(
        "Available Entity Services",
        ("Authentication","Scrape Data","Identify Entities","MaskEntities","DeIdentifyEntities")
    )
    st.sidebar.markdown(f"**You have selected _{chosenRadioButton}_ service!**")
    st.write('<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    st.markdown('<style>body{background-color: #3F6F9F;}</style>',unsafe_allow_html=True)
    streamAction(chosenRadioButton, verified) #calling action