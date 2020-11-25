#Core Packages
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field   
from bs4 import BeautifulSoup
from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, JSONResponse
from fastapi import FastAPI
import json
import boto3
import requests,datetime
import time
from random import randint
import urllib.request
import logging
import threading
import sys
import logging
import threading
import sys
from botocore.vendored import requests
from fastapi import Security, Depends, FastAPI, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from recommendAPI import recommend_user_user, recommend_item_item, recommend_similar_user_item
from mangum import Mangum
from fastapi_cloudauth.cognito import Cognito, CognitoCurrentUser, CognitoClaims

#Authentication Flag
app = FastAPI()
#app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)     
#To Configure
# app = FastAPI(title="PII and PHI Data Scrubbing Service",
#               description='''Backend API for App''',
#               version="0.0.0",openapi_prefix="/prod",openapi_url="")

@app.get("/scrapeData")
# def scrapeData(enterurl: str,verified: str):
def scrapeData(enterurl: str):
    def grab_page(url,url_ending):
        #print("attempting to grab page: " + url)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36',
        'Connection' : 'keep-alive',
        'Content-Length' : '799',
        'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
        'accept': '/',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'accept-language': 'en-US,en-GB;q=0.9,en;q=0.8,hi;q=0.7,mr;q=0.6'
        }
        page = requests.get(url + "/", headers = headers, timeout=5)
        page_html = page.text
        soup = BeautifulSoup(page_html, 'html.parser')
        meta = soup.find("div",{'class':'a-info get-alerts'})
        content = soup.find(id="a-body")
        text = content.text
        s3 = boto3.resource('s3')
        s3.Object('inputpii', 'abc' + str(randint(0,100))+'.txt').put(Body=text)

    def process_list_page(k):
        #origin_page = "http://seekingalpha.com/earnings/earnings-call-transcripts" + "/" + str(k)
        origin_page = userurl + "/" + str(k)
        #print("getting page " + origin_page)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'}
        page = requests.get(origin_page, headers = headers)
        page_html = page.text
    #print(page_html)
        soup = BeautifulSoup(page_html, 'html.parser')
        alist = soup.find_all("li",{'class':'list-group-item article'})
        for i in range(0,len(alist)):
            url_ending = alist[i].find_all("a")[0].attrs['href']
            url = "http://seekingalpha.com" + url_ending
            #print(url)
            #print(url_ending)
            grab_page(url,url_ending)
            #print(url)
            time.sleep(.5)
            
   # if ver
    for i in range(1,1): #choose what pages of earnings to scrape
        process_list_page(i,enterurl)
    
    return {
        #'statusCode': 200,
        'body': json.dumps('Successful')}

@app.get("/viewScrapedData")
def scrapdatadisplay():
    s3 = boto3.client("s3")
    bucket = "inputpii"
    key = "abcde.txt"
    file = s3.get_object(Bucket=bucket, Key=key)
    paragraph = str(file['Body'].read())
    return {
       
        'body': json.dumps(paragraph)
    }

@app.get("/identifyEntities")
def identifyPIIEntity(verified):

    if(verified == "True"):
        s3 = boto3.client("s3")
        bucket = "inputpii"
        key = "abcde.txt"
        file = s3.get_object(Bucket=bucket, Key=key)
        paragraph = str(file['Body'].read())
        comprehend = boto3.client("comprehend")
        entities = comprehend.detect_entities(Text=paragraph, LanguageCode = "en")
        keyphrase = comprehend.detect_key_phrases(Text=paragraph, LanguageCode = "en")
        s3 = boto3.resource('s3')
        BUCKET_NAME = "outputpii"
  #Modify
        OUTPUT_NAME = f"dataKeyTest.json"
        OUTPUT_BODY = json.dumps(entities)
    #print(f"[INFO] Saving Data to S3 {BUCKET_NAME} Bucket...")
        s3.Bucket(BUCKET_NAME).put_object(Key=OUTPUT_NAME, Body=OUTPUT_BODY)
    #print(f"[INFO]Job done!!")
        return {
        
            'body': json.dumps(entities)
        }
    else:
        return{
            'body': json.dumps('Authenticate User')
        }

@app.get("/maskEntities")
def maskIdentifiedEntity():
    client = boto3.client(service_name='comprehend', region_name='us-east-1')
    #response=comprehend.start_pii_entities_detection_job(InputDataConfig={'S3Uri':'s3://inputpii/abcde.txt','InputFormat':'ONE_DOC_PER_LINE'},OutputDataConfig={'S3Uri':'s3://outputpii/MaskOutput/',},Mode='ONLY_REDACTION',RedactionConfig={'PiiEntityTypes':['ALL'],'MaskMode':'MASK','MaskCharacter':'*'},DataAccessRoleArn='arn:aws:iam::711797752508:role/service-role/AmazonComprehendServiceRole-newestIAM',JobName='comprehend-REDACTMASKING',LanguageCode='en')
    response = client.start_pii_entities_detection_job(
    InputDataConfig={
        'S3Uri': 's3://inputpii/abcde.txt',
        'InputFormat': 'ONE_DOC_PER_LINE'
    },
    OutputDataConfig={
        'S3Uri': 's3://outputpii/MaskOutput/',
    },
    Mode='ONLY_REDACTION',
    RedactionConfig={
        'PiiEntityTypes': [
            'ALL'
        ],
        'MaskMode': 'MASK',
        'MaskCharacter': '*'
    },
    DataAccessRoleArn='arn:aws:iam::711797752508:role/service-role/AmazonComprehendServiceRole-newestIAM',
    JobName='comprehend-REDACTnew',
    LanguageCode='en'
    )
    return {
       'statusCode': 200,
        'body': json.dumps('Successfully Masked entities!!')
    }

@app.get("/maskedEntities", tags=["Masked Entities"])
def get_mask_PII_entity():
    s3 = boto3.client("s3")
    bucket = "outputpii"
    key = "abcde.txt.out"
    file = s3.get_object(Bucket=bucket, Key=key)
    paragraph = str(file['Body'].read())
    return {
        #'statusCode': 200,
        'body': json.dumps(paragraph)
    }

@app.get("/entityAnonymize", tags=["Anonymize Entities"])
def replacewithPIIEntity():
    client = boto3.client(service_name='comprehend', region_name='us-east-1')
    #response=comprehend.start_pii_entities_detection_job(InputDataConfig={'S3Uri':'s3://inputpii/abcde.txt','InputFormat':'ONE_DOC_PER_LINE'},OutputDataConfig={'S3Uri':'s3://outputpii/MaskOutput/',},Mode='ONLY_REDACTION',RedactionConfig={'PiiEntityTypes':['ALL'],'MaskMode':'MASK','MaskCharacter':'*'},DataAccessRoleArn='arn:aws:iam::711797752508:role/service-role/AmazonComprehendServiceRole-newestIAM',JobName='comprehend-REDACTMASKING',LanguageCode='en')
    response = client.start_pii_entities_detection_job(
    InputDataConfig={
        'S3Uri': 's3://inputpii/abcde.txt',
        'InputFormat': 'ONE_DOC_PER_LINE'
    },
    OutputDataConfig={
        'S3Uri': 's3://outputpii/MaskOutput/',
    },
    Mode='ONLY_REDACTION',
    RedactionConfig={
        'PiiEntityTypes': [
            'ALL'
        ],
        'MaskMode': 'REPLACE_WITH_PII_ENTITY_TYPE'
    },
    DataAccessRoleArn='arn:aws:iam::711797752508:role/service-role/AmazonComprehendServiceRole-newestIAM',
    JobName='comprehend-REDACTPIIEntities',
    LanguageCode='en'
    )    
    return {
        'statusCode': 200,
        'body': json.dumps('Successfully replaced with PII entities!!')
    }

@app.get("/displayPIIEntity", tags=["Display Identified Entities"])
def get_mask_PII_entity():
    s3 = boto3.client("s3")
    bucket = "outputpii"
    key = "replacewithPIIEntity.out"
    file = s3.get_object(Bucket=bucket, Key=key)
    paragraph = str(file['Body'].read())
    return {
        #'statusCode': 200,
        'body': json.dumps(paragraph)
    }

@app.get("/Authentication", tags=["Auth"])
async def userauthentication(usrName: str, usrPassword: str): 
    OTP = usrName+usrPassword
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Users')
    response = table.get_item(Key = {'Login': OTP})
    fullstring = str(response)
    substring = "Password"
    # check value logic here
    if fullstring.find(substring) != -1:
        verified = False
        response = "Please enter valid username/password!!"
    else:
        verified = True
        response = "Congratulations User Verified!!"
    return verified

#Deidentification generate HashMessage
@app.get("/deIdentifyEntities", tags=["Deidentify"])
async def deIdentifyEntities(JobName: str, verified: bool): 
    print(verified)
    STATE_MACHINE_ARN = 'arn:aws:states:us-east-1:198250712026:stateMachine:DeIdentifyEntitites'
    #The name of the execution
    EXECUTION_NAME = JobName
    #The string that contains the JSON input data for the execution -- replace with S3 input and make a Dict/Json of it. #ht
    inputJSON = {  "body": {    "message": " Good morning, everybody. My name is Van Bokhorst Serdar, and today I feel like sharing a whole lot of personal information with you. Let's start with my Email address SerdarvanBokhorst@dayrep.com. My address is 2657 Koontz Lane, Los Angeles, CA. My phone number is 818-828-6231. My Social security number is 548-95-6370. My Bank account number is 940517528812 and routing number 195991012. My credit card number is 5534816011668430, Expiration Date 6/1/2022, my C V V code is 121, and my pin 123456. Well, I think that's it. You know a whole lot about me. And I hope that Amazon comprehend is doing a good job at identifying PII entities so you can redact my personal information away from this document. Let's check." , "anonymizeOrDeidentify": "deidentify"}}
    INPUT = json.dumps(inputJSON)
    sfn = boto3.client('stepfunctions')
    response = sfn.start_execution(
        stateMachineArn=STATE_MACHINE_ARN,
        name=EXECUTION_NAME,
        input=INPUT
    )
    #display the arn that identifies the execution
    #executionARN = response.get('executionArn')
    executionARN = response.get('executionArn')
    print(executionARN)
    print("running")
    #waiting
    time.sleep(1)
    print("please wait for execution")
    time.sleep(5)
    print("Execution Completed")
    time.sleep(4)
    return {
        'body': json.dumps("Successfully Deidentified")
    }

@app.get("/reIdentifyEntities", tags=["Reidentify"])
async def reIdentifyEntities(Hash): 
    dynamodb = boto3.resource('dynamodb')
    dynamodbClient = boto3.client("dynamodb")
    table = dynamodb.Table('DeidentificationTable')
    #Hash = 'a7a8a696aa3c3fcca24462f56221d73a5058d9a31dfb53e82b1be4f1589fd519'
    fileName = str(Hash)
    #Query as per user hashhtsl
    # #getting user deidentified_message from s3
    s3 = boto3.client("s3")
    bucket = "dereidbucket"
    key = fileName + ".txt"
    file = s3.get_object(Bucket=bucket, Key=key)
    paragraph = str(file['Body'].read())
    #paragraph = str(file['Body']['deidentified_message'].read()) // to use this if the file is jSON
    #cleaning input file using cheap thrills
    # message = str(paragraph)
    print("******************Before********************")
    print(paragraph)
    #paragraph = json.dumps(paragraph)
    Query = table.query(
        IndexName = 'MessageHash-index',
        KeyConditionExpression = Key('MessageHash').eq(Hash)
    )
    # message = "Good morning, everyody. My name is 2c9128030504701edc16914de231d68f763f3815fe6414647678a0131545fa4, and today I feel like sharing a whole lot of personal information with you. Let's start with my Email address e937d3c279a947ad702aaf38c74510e93fa0394a13e4d89d0dfcef3f809.com. My address is 46fef4ce65ef72693f7c8748fda309e4cd2667977e2311fdd63968e3c, CA. My phone numer is 06559e1e922c2a4c9804cdd6018a4d01c896550f8da713198cc6012e8c3cc. My Social security numer is 40fcfd205559d58146fed63e7f56c810210e8e2ae9a8868a7427fd23322fe47. My Bank account numer is 38d07d021793837a06298662470a7cecfa2d8e3f2cf09d58e676928527c and routing numer 323cc64d1ea5374d7acc8a731222a281803c974c9a63815c481799487f99675. My credit card numer is f8536c70595fcafc43fc3c727d2dc28cd48fa07481a4c3de86a4cc3, Expiration Date 2737067aa34537cf63c12e0dea260d815acf37e4a97e78f6f8e526a7c91, my C V V code is 121, and my pin 6cf0a992320492346a0881597e3a91e4f21a9818a42d8de5210385531df7195. Well, I think that's it. You know a whole lot aout me. And I hope that f4088903685e44f60185a7ad7a795891ee8394118a7970694fd1a571e823 comprehend is doing a good jo at identifying PII entities so you can redact my personal information away from this document. Let's check."
    tableList = Query.get('Items')
    # print (tableList)
    lengthList = len(tableList)
    # print(lengthList)
    entityValues = ""
    entityHash = ""
    print(paragraph)
    for tableItem in tableList:
        entityValues = tableItem.get("Entity")
        entityHash =  tableItem.get("EntityHash")
        # message = message.replace(entityHash,entityValues)
        paragraph = paragraph.replace(entityHash,entityValues)

    # print (paragraph)
    paragraph = paragraph.replace("b","")
    paragraph = paragraph.replace('" ','')
    paragraph = paragraph.replace('"','')
    print("******************After********************")
    print (paragraph)
    print("Thanks Giving!!!")
    return {
        'body': json.dumps("Successfully Reidentified")
    }
