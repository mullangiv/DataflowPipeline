#H
#Core Packages
import json,requests, random, time, streamlit as st, numpy as np, pandas as pd
from PIL import Image
# import streamlit as st
# import numpy as np
# import pandas as pd
#Def Vars
global authValue
authValue = False
jobID = ""
st.set_page_config(page_title='HTworks', page_icon=None, layout='centered', initial_sidebar_state='auto')
st.sidebar.markdown('**PII and PHI Data Scrubbing Service**')
st.write('<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
#Radio Condtion
chosenRadioButton = st.sidebar.radio(
    "Available Entity Services",
    ("HomePage","Authentication","ScrapeData","IdentifyEntities","Anonymize","De/Re-Identify")
)
st.sidebar.markdown(f"**You have selected _{chosenRadioButton}_ service!**")
st.write('<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
st.markdown('<style>body{background-color: #A3A6A9;}</style>',unsafe_allow_html=True)
#Radio Button Condition 0
if chosenRadioButton == 'HomePage':
    st.title("Welcome!!!")
    st.info("Please press FastAPI Button to view FastAPI Documentation Page Landing")
    docs = st.button('FastAPI')
    st.info("Please press Documentation Button to view FastAPI Re-Documentation Page")
    redoc = st.button('Documentation')
    while docs:
        st.write(f'<iframe src="http://localhost:8000/docs", width=900, height=600  , scrolling=True></iframe>', unsafe_allow_html=True)
        break
    while redoc:
        st.write(f'<iframe src="http://localhost:8000/redoc", width=900, height=600  , scrolling=True></iframe>', unsafe_allow_html=True)
        break
#Radio Button Condition 1
if chosenRadioButton == 'ScrapeData':
    f = open("AuthenticationValue.txt", "a")
    f = open("AuthenticationValue.txt", "r")
    authValueFlag = (f.read())
    print(authValueFlag) 
    authValueFlag = str(authValueFlag)
    if authValueFlag == "True":
        authValue = True
    else:
        st.warning('Seems you are not authenticated')
    st.title('Scraping')
    st.subheader('_Please enter link to be scraped_')
    URL = st.text_input("Input URL")
    st.info('Please input the number of pages you would like to scrape')
    Page = st.number_input ("Pages", min_value=1, max_value=3)
    
    if st.button('Scrape Data'):
        payload = json.dumps({
            "link" : URL
            })
        response = requests.get(f"http://127.0.0.1:8000/scrapeCallTranscripts?verified={authValue}&url={URL}&page={Page}")
        data_list = response.json()            
        st.subheader(data_list)

    st.subheader('_View Scrapped File List_')
    if st.button('Display Scraped File List'):
        response = requests.get(f"http://127.0.0.1:8000/displayScrapedFilesList?verified={authValue}")
        data_list = response.json()
        #scrapeList=data_list['body']
        st.header(data_list)  
#Radio Button Condition 2
if chosenRadioButton == 'IdentifyEntities':
    #
    f = open("AuthenticationValue.txt", "a")
    f = open("AuthenticationValue.txt", "r")
    # while st.button('Read Documentation'):
    authValue = False
    authValueFlag = (f.read())
    print(authValueFlag) 
    authValueFlag = str(authValueFlag)
    if authValueFlag == "True":
        authValue = True
    else:
        st.warning('Seems you are not authenticated')
    #
    st.header('What would you like to identify in Data?')
    box = st.selectbox('Please select the identification service',('Entities', 'Keyphrases'))
    st.write('You selected:', box)
    if box == "Entities":
        st.title('Identify Entities')
        st.subheader('_Please click the button to Identify PII entities_')
        fileName = st.text_input("File Name")
        if st.button('Identify Entities'):
            response = requests.get(f"http://127.0.0.1:8000/identifyEntities?verified={authValue}&fileName={fileName}")
            data_list = response.json()
            st.header(data_list)
    else:
        st.title('Identify Keyphrases')
        st.subheader('_Please click the button to Identify PII entities_')
        fileName = st.text_input("File Name")
        if st.button('Identify Keyphrases'):
            response = requests.get(f"http://127.0.0.1:8000/identifyKeyphrases?verified={authValue}&fileName={fileName}")
            data_list = response.json()
            st.header(data_list)
#Radio Button Condition 3
if chosenRadioButton == 'Anonymize':
    #
    f = open("AuthenticationValue.txt", "a")
    f = open("AuthenticationValue.txt", "r")
    # while st.button('Read Documentation'):
    authValue = False
    authValueFlag = (f.read())
    print(authValueFlag) 
    authValueFlag = str(authValueFlag)
    if authValueFlag == "True":
        authValue = True
    else:
        st.warning('Seems you are not authenticated')
    #
    st.title('How would you like to anonymize data?')
    box = st.selectbox('Please select anonymization service',('Masking', 'Replace with Entities'))
    st.write('You selected:', box)
    if box == 'Masking':
        st.header('Mask Entities')
        st.info('Please enter Input File Name for Anonymization Job')
        fileName = st.text_input("File Name")
        st.info('Please enter Input File Name for Anonymization Job')
        drop = st.selectbox('Please select Entities for Anonymization',('ALL', 'Select'))
        st.write('You selected:', drop)
        entityList = ""
        if drop == 'ALL':
            ALL = st.checkbox("ALL", value=False, key=None) #use ur brain bro make this a drop
            if ALL:
                entityList = "ALL"
               # entityList = '"'+entityList+'"'
        else:
            st.info('Please select the Entity List for Masking') #use this info for the drop and select option
            # rest in the drop select
            CREDIT_DEBIT_NUMBER = st.checkbox("CREDIT_DEBIT_NUMBER", value=False, key=None)
            if CREDIT_DEBIT_NUMBER:
                entityList = entityList+"CREDIT_DEBIT_NUMBER"+","
            AWS_ACCESS_KEY = st.checkbox("AWS_ACCESS_KEY", value=False, key=None) 
            if AWS_ACCESS_KEY:
                entityList = entityList+"AWS_ACCESS_KEY"+","
            BANK_ROUTING = st.checkbox("BANK_ROUTING", value=False, key=None) 
            if BANK_ROUTING:
                entityList = entityList+"BANK_ROUTING"+","
            MAC_ADDRESS = st.checkbox("MAC_ADDRESS", value=False, key=None) 
            if MAC_ADDRESS:
                entityList = entityList+"MAC_ADDRESS"+","
            DRIVER_ID = st.checkbox("DRIVER_ID", value=False, key=None) 
            if DRIVER_ID:
                entityList = entityList+"DRIVER_ID"+","
            CREDIT_DEBIT_CVV = st.checkbox("CREDIT_DEBIT_CVV", value=False, key=None) 
            if CREDIT_DEBIT_CVV:
                entityList = entityList+"CREDIT_DEBIT_CVV"+","
            IP_ADDRESS = st.checkbox("IP_ADDRESS", value=False, key=None) 
            if IP_ADDRESS:
                entityList = entityList+"IP_ADDRESS"+","
            ADDRESS = st.checkbox("ADDRESS", value=False, key=None) 
            if ADDRESS:
                entityList = entityList+"ADDRESS"+","
            NAME = st.checkbox("NAME", value=False, key=None) 
            if NAME:
                entityList = entityList+"NAME"+","
            CREDIT_DEBIT_EXPIRY = st.checkbox("CREDIT_DEBIT_EXPIRY", value=False, key=None) 
            if CREDIT_DEBIT_EXPIRY:
                entityList = entityList+"CREDIT_DEBIT_EXPIRY"+","
            SSN = st.checkbox("SSN", value=False, key=None)
            if SSN:
                entityList = entityList+"SSN"+","
            PHONE = st.checkbox("PHONE", value=False, key=None) 
            if PHONE:
                entityList = entityList+"PHONE"+","
            DATE_TIME = st.checkbox("DATE_TIME", value=False, key=None) 
            if DATE_TIME:
                entityList = entityList+"DATE_TIME"+","
            PIN = st.checkbox("PIN", value=False, key=None) 
            if PIN:
                entityList = entityList+"PIN"+","
            PASSPORT_NUMBER = st.checkbox("PASSPORT_NUMBER", value=False, key=None) 
            if PASSPORT_NUMBER:
                entityList = entityList+"PASSPORT_NUMBER"+","
            URL = st.checkbox("URL", value=False, key=None) 
            if URL:
                entityList = entityList+"URL"+","
            USERNAME = st.checkbox("USERNAME", value=False, key=None) 
            if USERNAME:
                entityList = entityList+"USERNAME"+","
            PASSWORD = st.checkbox("PASSWORD", value=False, key=None) 
            if PASSWORD:
                entityList = entityList+"PASSWORD"+","
            EMAIL = st.checkbox("EMAIL", value=False, key=None) 
            if EMAIL:
                entityList = entityList+"EMAIL"+","
            AWS_SECRET_KEY = st.checkbox("AWS_SECRET_KEY", value=False, key=None) 
            if AWS_SECRET_KEY:
                entityList = entityList+"AWS_SECRET_KEY"+","
            BANK_ACCOUNT_NUMBER = st.checkbox("BANK_ACCOUNT_NUMBER", value=False, key=None) 
            if BANK_ACCOUNT_NUMBER:
                entityList = entityList+"BANK_ACCOUNT_NUMBER"+","
            AGE = st.checkbox("AGE", value=False, key=None) 
            if AGE:
                entityList = entityList+"AGE"
            entityList = entityList.replace(',','","')
            entityList = '"'+entityList+'"'
            entityList = entityList.replace(',""','')
            print(entityList)
            #entityList = #st.text_input("Entity List") #gonnaappendu
        #st.info('Please input the Entity List as : ALL or like this > "CREDIT_DEBIT_NUMBER","BANK_ROUTING","MAC_ADDRESS","AWS_ACCESS_KEY","CREDIT_DEBIT_CVV","NAME","CREDIT_DEBIT_EXPIRY","SSN","PHONE","URL","AWS_SECRET_KEY","DRIVER_ID","ADDRESS","PIN","USERNAME","PASSPORT_NUMBER","PASSWORD","IP_ADDRESS","EMAIL","DATE_TIME","BANK_ACCOUNT_NUMBER","AGE"')
        st.info('Please input the Mask Character select :  ! or # or $ or % or & or * or @  ')
        maskCharacter = st.text_input("Mask Character")
        st.subheader('_Please click the button to Mask Entities_')
        if st.button('Masking'):
            response = requests.get(f"http://127.0.0.1:8000/maskEntities?verified={authValue}&fileName={fileName}&entityList={entityList}&maskCharacter={maskCharacter}")
            data_list = response.json()
            jobID = data_list
            st.header(data_list)
            st.success("Job Initated please use the job id to download the Masked File")  
        jobID = st.text_input("Job ID")
        if st.button('View Masked Entities'):
            response = requests.get(f"http://127.0.0.1:8000/getMaskedEntities?verified={authValue}&jobID={jobID}&fileName={fileName}")
            data_list = response.json()
            prog = str(data_list)
            st.spinner(text='In progress...')
            st.success(data_list)
    else:
        st.header('Replace with EntityType')
        st.info('Please enter Input File Name for Anonymization Job')
        fileName = st.text_input("File Name")
        entityList = ""
        drop = st.selectbox('Please select Entities for Anonymization',('ALL', 'Select'))
        st.write('You selected:', drop)
        entityList = ""
        if drop == 'ALL':
            ALL = st.checkbox("ALL", value=False, key=None) #use ur brain bro make this a drop
            if ALL:
                entityList = "ALL"
                entityList = '"'+entityList+'"'
        else:
            st.info('Please select the Entity List for Masking') #use this info for the drop and select option
            # rest in the drop select
            CREDIT_DEBIT_NUMBER = st.checkbox("CREDIT_DEBIT_NUMBER", value=False, key=None)
            if CREDIT_DEBIT_NUMBER:
                entityList = entityList+"CREDIT_DEBIT_NUMBER"+","
            AWS_ACCESS_KEY = st.checkbox("AWS_ACCESS_KEY", value=False, key=None) 
            if AWS_ACCESS_KEY:
                entityList = entityList+"AWS_ACCESS_KEY"+","
            BANK_ROUTING = st.checkbox("BANK_ROUTING", value=False, key=None) 
            if BANK_ROUTING:
                entityList = entityList+"BANK_ROUTING"+","
            MAC_ADDRESS = st.checkbox("MAC_ADDRESS", value=False, key=None) 
            if MAC_ADDRESS:
                entityList = entityList+"MAC_ADDRESS"+","
            DRIVER_ID = st.checkbox("DRIVER_ID", value=False, key=None) 
            if DRIVER_ID:
                entityList = entityList+"DRIVER_ID"+","
            CREDIT_DEBIT_CVV = st.checkbox("CREDIT_DEBIT_CVV", value=False, key=None) 
            if CREDIT_DEBIT_CVV:
                entityList = entityList+"CREDIT_DEBIT_CVV"+","
            IP_ADDRESS = st.checkbox("IP_ADDRESS", value=False, key=None) 
            if IP_ADDRESS:
                entityList = entityList+"IP_ADDRESS"+","
            ADDRESS = st.checkbox("ADDRESS", value=False, key=None) 
            if ADDRESS:
                entityList = entityList+"ADDRESS"+","
            NAME = st.checkbox("NAME", value=False, key=None) 
            if NAME:
                entityList = entityList+"NAME"+","
            CREDIT_DEBIT_EXPIRY = st.checkbox("CREDIT_DEBIT_EXPIRY", value=False, key=None) 
            if CREDIT_DEBIT_EXPIRY:
                entityList = entityList+"CREDIT_DEBIT_EXPIRY"+","
            SSN = st.checkbox("SSN", value=False, key=None)
            if SSN:
                entityList = entityList+"SSN"+","
            PHONE = st.checkbox("PHONE", value=False, key=None) 
            if PHONE:
                entityList = entityList+"PHONE"+","
            DATE_TIME = st.checkbox("DATE_TIME", value=False, key=None) 
            if DATE_TIME:
                entityList = entityList+"DATE_TIME"+","
            PIN = st.checkbox("PIN", value=False, key=None) 
            if PIN:
                entityList = entityList+"PIN"+","
            PASSPORT_NUMBER = st.checkbox("PASSPORT_NUMBER", value=False, key=None) 
            if PASSPORT_NUMBER:
                entityList = entityList+"PASSPORT_NUMBER"+","
            URL = st.checkbox("URL", value=False, key=None) 
            if URL:
                entityList = entityList+"URL"+","
            USERNAME = st.checkbox("USERNAME", value=False, key=None) 
            if USERNAME:
                entityList = entityList+"USERNAME"+","
            PASSWORD = st.checkbox("PASSWORD", value=False, key=None) 
            if PASSWORD:
                entityList = entityList+"PASSWORD"+","
            EMAIL = st.checkbox("EMAIL", value=False, key=None) 
            if EMAIL:
                entityList = entityList+"EMAIL"+","
            AWS_SECRET_KEY = st.checkbox("AWS_SECRET_KEY", value=False, key=None) 
            if AWS_SECRET_KEY:
                entityList = entityList+"AWS_SECRET_KEY"+","
            BANK_ACCOUNT_NUMBER = st.checkbox("BANK_ACCOUNT_NUMBER", value=False, key=None) 
            if BANK_ACCOUNT_NUMBER:
                entityList = entityList+"BANK_ACCOUNT_NUMBER"+","
            AGE = st.checkbox("AGE", value=False, key=None) 
            if AGE:
                entityList = entityList+"AGE"
            entityList = entityList.replace(',','","')
            entityList = '"'+entityList+'"'
            entityList = entityList.replace(',""','')
            print(entityList)
        st.subheader('_Please click the button to Replace with EntityType_')
        if st.button('Replace with EntityType'):
            response = requests.get(f"http://127.0.0.1:8000/replaceEntities?verified={authValue}&fileName={fileName}&entityList={entityList}")
            data_list = response.json()
            jobID = data_list
            st.header(data_list)
            st.success("Job Initated please use the job id to download the Masked File")  
        jobID = st.text_input("Job ID")
        if st.button('View data Replaced with EntityType'):
            response = requests.get(f"http://127.0.0.1:8000/displayEntities?verified={authValue}&jobID={jobID}&fileName={fileName}")
            data_list = response.json()
            prog = str(data_list)
            st.spinner(text='In progress...')
            st.success(data_list)
#Radio Button Condition 4
if chosenRadioButton == 'De/Re-Identify':
    #
    f = open("AuthenticationValue.txt", "a")
    f = open("AuthenticationValue.txt", "r")
    # while st.button('Read Documentation'):
    authValue = False
    authValueFlag = (f.read())
    print(authValueFlag) 
    authValueFlag = str(authValueFlag)
   
    if authValueFlag == "True":
        authValue = True
    else:
        st.warning('Seems you are not authenticated')
    #
    st.title('De/Re-IdentifyEntities')
    box = st.selectbox('Please select Anonymization service',('De-Identify', 'Re-Identify'))
    st.write('You selected:', box)
    
    if box == 'De-Identify':
        st.header('De-Identify Entities')
        fileName = st.text_input("File Name")
        st.info('Please enter Job Name for De/Re-Identification Step Function')
        jobName = st.text_input("Enter Job Name")
        ranInt = random.randint(999999, 99999999) 
        ranInt = str(ranInt)
        jobName = jobName + ranInt
        st.subheader('_Click button to De-Identify Entities_')
        if st.button('De-Identify'):
            st.info('Please enter Input File Name for De-Identification Job')
            response = requests.get(f"http://127.0.0.1:8000/deIdentifyEntities?verified={authValue}&fileName={fileName}&JobName={jobName}")
            data_list = response.json()
            #b=data_list['body']
            st.header(data_list)
            
    else:
        st.header('Re-Identify Entities')
        st.info('Please enter the Hash for Re-Identification Job')
        Hash = st.text_input("Hash")
        st.subheader('_Click button to Re-Identify Entities_')
        if st.button('Re-Identify'):
            response = requests.get(f"http://127.0.0.1:8000/reIdentifyEntities?verified={authValue}&Hash={Hash}")
            data_list = response.json()
            #b=data_list['body']
            st.header(data_list)
#Radio Button Condition 5
if chosenRadioButton == 'Authentication':
    f = open('AuthenticationValue.txt', 'a')
    f.truncate(0)
    st.title('**_User Authentication_**')
    #image = Image.open('img-2.png')
    #st.image(image, caption='',use_column_width=True)
    #st.header('User Authentication')
    st.subheader('_Please enter valid username and password_')
    username = st.text_input('Username')
    password = st.text_input('Password')
    if st.button('Authenticate'):
        response = requests.get(f"http://127.0.0.1:8000/Authentication?usrName={username}&usrPassword={password}")
        data_list = response.json()
        print(f"value is : {data_list}")
        verified = data_list
        #print(verified)
        #st.progress(verified)
        if verified == True:
            data_list = "Authenticated Successfully"
            st.success(data_list) 
            authValue = True
            st.balloons()
        else:
        #global authValue
            data_list = "Invalid Username/Password Combination"
            #st.subheader(data_list)
            st.error(data_list)
            st.info("Please retry with valid Username and Password Combination")
            authValue = False  
        print(authValue)    
        f = open('AuthenticationValue.txt', 'a')
        f.truncate(0)
        f.write(str(authValue))
        f.close()  
        print(authValue)
#T