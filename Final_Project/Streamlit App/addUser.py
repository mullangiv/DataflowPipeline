#H
#Core Packages
import json, boto, boto3, requests, datetime, time, logging, threading, sys, io, os, random
#urllib.request, logging, threading, sys, io, os, random
from fastapi import FastAPI, HTTPException, Security, Depends
from pydantic import BaseModel, Field   
from bs4 import BeautifulSoup
from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, JSONResponse
from boto.s3.connection import S3Connection
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
#from recommendAPI import recommend_user_user, recommend_item_item, recommend_similar_user_item
from mangum import Mangum
from fastapi_cloudauth.cognito import Cognito, CognitoCurrentUser, CognitoClaims
#from urllib.parse import urlparse,urlsplit
from boto3.dynamodb.conditions import Key
#from botocore.vendored import requests
#Def Vars
app = FastAPI()
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

@app.get("/displayScrapedFilesList", tags=["Scrape Call Transcripts"])
def scrapdatadisplay(verified: bool, current_user: CognitoClaims = Depends(auth)):
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
#T