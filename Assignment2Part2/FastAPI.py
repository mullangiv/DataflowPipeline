#H
#Core Packages
import json, boto, boto3, requests, datetime, time, urllib.request, logging, threading, sys, io, os, random
from fastapi import FastAPI, HTTPException, Security, Depends
from pydantic import BaseModel, Field   
from bs4 import BeautifulSoup
from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, JSONResponse
from boto.s3.connection import S3Connection
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from recommendAPI import recommend_user_user, recommend_item_item, recommend_similar_user_item
from mangum import Mangum
from fastapi_cloudauth.cognito import Cognito, CognitoCurrentUser, CognitoClaims
from urllib.parse import urlparse,urlsplit
from boto3.dynamodb.conditions import Key
#from botocore.vendored import requests
#Def Vars
app = FastAPI(root_path="/prod")
fileName = "" 
#Def AWS Config
userRegion = "us-east-1"
userClientId = "5g5l767fmou68418i4l335lfsj"
userPool = "us-east-1_w6Msc6CWC"
auth = Cognito(region= userRegion, userPoolId= userPool)
getUser = CognitoCurrentUser(region= userRegion, userPoolId= userPool)
cidp = boto3.client('cognito-idp')
dynamodb = boto3.resource('dynamodb')
dynamodbClient = boto3.client("dynamodb")
table = dynamodb.Table('DeidentificationTable')
loginPassword = loginName = None
JWT = {}
#Config for Lambda
#app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)     
#To Configure ---- root_path 
# app = FastAPI(title="PII and PHI Data Scrubbing Service",
#               description='''Backend API for App''',
#               version="0.0.0",openapi_prefix="/prod",openapi_url="")
# API 1
@app.get("/scrapeCallTranscripts", tags=["Scrape Call Transcripts"])
async def scrapeCallTranscripts(verified: bool, url: str, page: int):
    print(verified)
    if(verified == True):
        def scrapePageData(url,actualURL,actualList):
            print("attempting to grab page: " + url)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36',
            'Connection' : 'keep-alive',
            'Content-Length' : '799',
            'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
            'accept': '*/*',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'accept-language': 'en-US,en-GB;q=0.9,en;q=0.8,hi;q=0.7,mr;q=0.6'
            }
            page = requests.get(url + "/", headers = headers, timeout=5)
            page_html = page.text
            soup = BeautifulSoup(page_html, 'html.parser')
            # meta = soup.find("div",{'class':'a-info get-alerts'})
            content = soup.find(id="a-body")        
            text = content.text
            text = text[:20000]
            #AWS
            outbucket = 'scrapecalldata'
            s3 = boto3.resource('s3')
            outfile = io.StringIO(text)
            # Generate output file and close it!
            #actualURL = actualURL.replace("-","")
            actualURL = actualURL[7:]
            outobj = s3.Object(outbucket,actualURL+'.txt')
            outobj.put(Body=outfile.getvalue())
            outfile.close()

        def scrapeListLinks(url,k):
            origin_page = url + "/" + str(k)
            print("getting page " + origin_page)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'}
            page = requests.get(origin_page, headers = headers)
            page_html = page.text
            soup = BeautifulSoup(page_html, 'html.parser')
            actualList = soup.find_all("li",{'class':'list-group-item article'})
            for i in range(0,len(actualList)):
                actualURL = actualList[i].find_all("a")[0].attrs['href']
                parser = urlsplit(url)
                header = parser [0]
                base = parser [1]
                header=str(header)
                base=str(base)
                url = header + "://" + base + actualURL
                actualURL = str(actualURL.replace("/article/",""))
                print(actualURL)
                scrapePageData(url,actualURL,actualList)
                time.sleep(.5)

        for i in range(1,page): #Page Range
            scrapeListLinks(url,i)
        result = "Files Scraped Successfully!!!"
        return result
    else:
        print("I am here")
        result = "Please Authenticate User"
        return result
# API 2
@app.get("/displayScrapedFilesList", tags=["Scrape Call Transcripts"])
def scrapdatadisplay(verified: bool):
    if(verified == True):
        conn = S3Connection() # assumes boto.cfg setup
        bucket = conn.get_bucket('scrapecalldata')
        fileList = []
        for obj in bucket.get_all_keys():
            fileList.append(obj)
        fileList = str(fileList)
        fileList = fileList.replace("<Key:","")
        fileList = fileList = fileList.replace(">","")
        return fileList
    else:
        result = "Please Authenticate User"
        return result

# API 3
@app.get("/identifyEntities", tags=["Identify"])
def identifyPIIEntity(verified: bool, fileName: str):

    if(verified == True):
        s3 = boto3.client("s3")
        bucket = "scrapecalldata"
        key = fileName + ".txt"
        file = s3.get_object(Bucket=bucket, Key=key)
        paragraph = str(file['Body'].read())
        paragraph = paragraph[:5000]
        comprehend = boto3.client("comprehend")
        entities = comprehend.detect_entities(Text=paragraph, LanguageCode = "en")
        keyphrase = comprehend.detect_key_phrases(Text=paragraph, LanguageCode = "en")
        s3 = boto3.resource('s3')
        BUCKET_NAME = "identifyentity"
        #Modify
        OUTPUT_NAME = f"{fileName}Entities.json"
        OUTPUT_BODY = json.dumps(entities)
        #print(f"[INFO] Saving Data to S3 {BUCKET_NAME} Bucket...")
        s3.Bucket(BUCKET_NAME).put_object(Key=OUTPUT_NAME, Body=OUTPUT_BODY)
        #print(f"[INFO]Job done!!")
        return entities
    else:
        result = "Please Authenticate User"
        return result
# API 4
@app.get("/identifyKeyphrases", tags=["Identify"])
def identifyPIIEntity(verified: bool, fileName: str):

    if(verified == True):
        s3 = boto3.client("s3")
        bucket = "scrapecalldata"
        key = fileName + ".txt"
        file = s3.get_object(Bucket=bucket, Key=key)
        paragraph = str(file['Body'].read())
        paragraph = paragraph[:5000]
        comprehend = boto3.client("comprehend")
        entities = comprehend.detect_entities(Text=paragraph, LanguageCode = "en")
        keyphrase = comprehend.detect_key_phrases(Text=paragraph, LanguageCode = "en")
        s3 = boto3.resource('s3')
        BUCKET_NAME = "identifyentity"
        #Modify
        OUTPUT_NAME = f"{fileName}KeyPhrases.json"
        OUTPUT_BODY = json.dumps(keyphrase)
        #print(f"[INFO] Saving Data to S3 {BUCKET_NAME} Bucket...")
        s3.Bucket(BUCKET_NAME).put_object(Key=OUTPUT_NAME, Body=OUTPUT_BODY)
        #print(f"[INFO]Job done!!")
        return keyphrase
    else:
        result = "Please Authenticate User"
        return result
# API 5
@app.get("/maskEntities", tags=["Anonymize Entities"])
def maskEntities(verified: bool, fileName:str, maskCharacter):
    if(verified == True):
        comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
        inputBucket = f"s3://scrapecalldata/{fileName}.txt"
        response = comprehend.start_pii_entities_detection_job(
        InputDataConfig={
            'S3Uri': inputBucket,
            'InputFormat': 'ONE_DOC_PER_LINE'
        },
        OutputDataConfig={
            'S3Uri': 's3://identifyentity/',
        },
        Mode='ONLY_REDACTION',
        RedactionConfig={
            'PiiEntityTypes': [
                'ALL'
            ],
            'MaskMode': 'MASK',
            'MaskCharacter': maskCharacter
        },
        DataAccessRoleArn='arn:aws:iam::198250712026:role/service-role/AmazonComprehendServiceRole-PIIRole',
        JobName='comprehend-REDACTnew',
        LanguageCode='en'  
        )
        jobID = response['JobId']
        return jobID
    else:
        result = "Please Authenticate User"
        return result
# API 6
@app.get("/getMaskedEntities", tags=["Anonymize Entities"])
def getMaskedEntities(verified: bool, jobID: str, fileName: str):
    if(verified == True):
        s3 = boto3.client("s3")
        bucket = "identifyentity"
        comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
        jobStatus = comprehend.describe_pii_entities_detection_job(
        JobId= jobID
        )
        #time.sleep(36)
        key = fileName + ".txt.out"
        print(f"Job Status {jobStatus}")
        JD = jobStatus['PiiEntitiesDetectionJobProperties']['JobStatus']
        print(JD)
        JD = str(JD)
        while JD == "IN_PROGRESS":
            comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
            jobStatus = comprehend.describe_pii_entities_detection_job(
            JobId= jobID
            )
            JD = jobStatus['PiiEntitiesDetectionJobProperties']['JobStatus']
            print(JD)
            JD = str(JD)
            time.sleep(36)
        prefix = jobStatus['PiiEntitiesDetectionJobProperties']['OutputDataConfig']['S3Uri']
        prefix = prefix.replace("s3://identifyentity/","")
        print(jobStatus['PiiEntitiesDetectionJobProperties']['OutputDataConfig']['S3Uri'])
        s3_resource = boto3.resource('s3')
        my_bucket = s3_resource.Bucket('identifyentity')
        objects = my_bucket.objects.filter(Prefix=prefix)
        for obj in objects:
            path, filename = os.path.split(obj.key)
            my_bucket.download_file(obj.key, filename)
        output = "Downloaded Successfully!!!"
        return output
    else:
        result = "Please Authenticate User"
        return result
# API 7
@app.get("/replaceEntities", tags=["Anonymize Entities"])
def replaceEntities(verified: bool, fileName:str, maskCharacter):
    if(verified == True):
        comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
        inputBucket = f"s3://scrapecalldata/{fileName}.txt"
        response = comprehend.start_pii_entities_detection_job(
        InputDataConfig={
            'S3Uri': inputBucket,
            'InputFormat': 'ONE_DOC_PER_LINE'
        },
        OutputDataConfig={
            'S3Uri': 's3://identifyentity/',
        },
        Mode='ONLY_REDACTION',
        RedactionConfig={
            'PiiEntityTypes': [
                'ALL'
            ],
            'MaskMode': 'REPLACE_WITH_PII_ENTITY_TYPE',
        },
        DataAccessRoleArn='arn:aws:iam::198250712026:role/service-role/AmazonComprehendServiceRole-PIIRole',
        JobName='comprehend-REDACTnew',
        LanguageCode='en'  
        )
        jobID = response['JobId']
        return jobID
    else:
        result = "Please Authenticate User"
        return result
# API 8
@app.get("/displayEntities", tags=["Anonymize Entities"])
def displayEntities(verified: bool, jobID: str, fileName: str):
    if(verified == True):
        s3 = boto3.client("s3")
        bucket = "identifyentity"
        comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
        jobStatus = comprehend.describe_pii_entities_detection_job(
        JobId= jobID
        )
        #time.sleep(36)
        key = fileName + ".txt.out"
        print(f"Job Status {jobStatus}")
        JD = jobStatus['PiiEntitiesDetectionJobProperties']['JobStatus']
        print(JD)
        JD = str(JD)
        while JD == "IN_PROGRESS":
            comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
            jobStatus = comprehend.describe_pii_entities_detection_job(
            JobId= jobID
            )
            JD = jobStatus['PiiEntitiesDetectionJobProperties']['JobStatus']
            print(JD)
            JD = str(JD)
            time.sleep(36)
        prefix = jobStatus['PiiEntitiesDetectionJobProperties']['OutputDataConfig']['S3Uri']
        prefix = prefix.replace("s3://identifyentity/","")
        print(jobStatus['PiiEntitiesDetectionJobProperties']['OutputDataConfig']['S3Uri'])
        s3_resource = boto3.resource('s3')
        my_bucket = s3_resource.Bucket('identifyentity')
        objects = my_bucket.objects.filter(Prefix=prefix)
        for obj in objects:
            path, filename = os.path.split(obj.key)
            my_bucket.download_file(obj.key, filename)
        output = "Downloaded Successfully!!!"
        return output
    else:
        result = "Please Authenticate User"
        return result
# API 9
@app.get("/Authentication", tags=["Auth"])
async def userauthentication(usrName: str, usrPassword: str): 
    OTP = usrName+usrPassword
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Users')
    response = table.get_item(Key = {'Login': OTP})
    print(response)
    fullstring = str(response)
    print(fullstring)
    substring = "Password"
    verified = False
    # check value logic here
    if substring in fullstring:
        verified = True
        print("came here")
        response = "Congratulations User Verified!!"
    else:
        verified = False
        response = "Please enter valid username/password!!"
    print(verified)
    return verified
# API 10
#Deidentification generate HashMessage
@app.get("/deIdentifyEntities", tags=["De/Re-Identify"])
#async def deIdentifyEntities(JobName: str, verified: bool): 
async def deIdentifyEntities(verified: bool,fileName: str,JobName: str): 
    if(verified == True):
        STATE_MACHINE_ARN = 'arn:aws:states:us-east-1:198250712026:stateMachine:DeIdentifyEntitites'
        #The name of the execution user input
        EXECUTION_NAME = JobName
        key = fileName + ".txt"
        s3 = boto3.client("s3")
        fileobj = s3.get_object(Bucket='scrapecalldata',Key=key) 
        filedata = fileobj['Body'].read()
        text = filedata.decode('utf-8') 
        #The string that contains the JSON input data for the execution
        inputJSON = { "message": text[:20000]}
        INPUT = json.dumps(inputJSON)
        sfn = boto3.client('stepfunctions')
        response = sfn.start_execution(
            stateMachineArn=STATE_MACHINE_ARN,
            name=EXECUTION_NAME,
            input=INPUT
        )
        #display the arn that identifies the execution
        executionARN = response.get('executionArn')
        time.sleep(1)
        print("Forgot Mask")
        #waiting
        time.sleep(2)
        print("Rushing with Mask on")
        time.sleep(3)
        print("Wooooaaah!!!! Please keep 6 Ft. Distance")
        time.sleep(4)
        print("Stay Home, Stay Safe!!! DUH -_-")
        time.sleep(5)
        #getting actual response
        response = sfn.get_execution_history(
            executionArn=executionARN,
            maxResults=1,
            reverseOrder=True,
            includeExecutionData=True
        )
        print(response)
        outputString = response.get('events')[0].get('executionSucceededEventDetails').get('output')
        dictOutput = json.loads(outputString)
        hash_message = dictOutput.get('hashed_message')
        hash = str(hash_message).replace('hashed_message','')
        print(hash)
        print("************************")
        deid_message = dictOutput.get('deid_message')
        message = str(deid_message).replace('deid_message','')
        print(message)
        return hash
    else:
        result = "Please Authenticate User"
        return result
# API 11
@app.get("/reIdentifyEntities", tags=["De/Re-Identify"])
async def reIdentifyEntities(verified: bool, Hash: str): 
    if(verified == True):
        fileName = Hash
        #Query as per user hashhtsl
        #getting user deidentified_message from s3
        s3 = boto3.client("s3")
        bucket = "dereidbucket"
        key = fileName + ".txt"
        Hash = Hash
        file = s3.get_object(Bucket=bucket, Key=key)
        paragraph = str(file['Body'].read())
        #paragraph = str(file['Body']['deidentified_message'].read()) // to use this if the file is jSON
        #cleaning input file using cheap thrills
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
            paragraph = paragraph.replace(entityHash,entityValues)

        for tableItem in tableList:
            entityValues = tableItem.get("Entity")
            entityHash =  tableItem.get("EntityHash")
            paragraph = paragraph.replace(entityHash,entityValues)

        for tableItem in tableList:
            entityValues = tableItem.get("Entity")
            entityHash =  tableItem.get("EntityHash")
            paragraph = paragraph.replace(entityHash,entityValues)

        paragraph = paragraph.replace("b","")
        paragraph = paragraph.replace("'","")
        paragraph = paragraph.replace('" ','')
        paragraph = paragraph.replace('"','')
        paragraph = paragraph.replace("b","")
        paragraph = paragraph.replace("\\n", " ")
        print("******************After********************")
        print (paragraph)
        return paragraph
    else:
        result = "Please Authenticate User"
        return result
#T