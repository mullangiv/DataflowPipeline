import boto3, json, uuid, os, boto, time
from pydantic import BaseModel
from typing import Optional
from pprint import pprint

from fastapi import Security, Depends, FastAPI, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, JSONResponse

s3 = boto3.resource(service_name='s3', region_name='us-east-1')
data = open('plantdata.csv', 'rb')
s3.Bucket('s3overwritebucketplantdata').put_object(Key='plantdata.csv', Body=data)


API_KEY = str(uuid.uuid1()) 
API_KEY_NAME = "access_token"
COOKIE_DOMAIN = "localtest.me"
print(API_KEY)
api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)


async def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
    api_key_cookie: str = Security(api_key_cookie),
):

    if api_key_query == API_KEY:
        return api_key_query
    elif api_key_header == API_KEY:
        return api_key_header
    elif api_key_cookie == API_KEY:
        return api_key_cookie
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )


app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


@app.get("/", tags=["Homepage"])
async def homepage():
    url = "http://localtest.me:8080/docs?access_token= "
    return "Oops! You are not verified. Please, verify yourself using : " + url


@app.get("/openapi.json", tags=["Documentation"])
async def get_open_api_endpoint(api_key: APIKey = Depends(get_api_key)):
    response = JSONResponse(
        get_openapi(title="FastAPI authentication security test", version=1, routes=app.routes)
    )
    return response


@app.get("/docs", tags=["Documentation"])
async def get_documentation(api_key: APIKey = Depends(get_api_key)):
    response = get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
    response.set_cookie(
        API_KEY_NAME,
        value=api_key,
        domain=COOKIE_DOMAIN,
        httponly=True,
        max_age=1800,
        expires=1800,
    )
    return response

@app.get("/secureEndpoint", tags=["Test"])
async def get_open_api_endpoint(api_key: APIKey = Depends(get_api_key)):
    response = "User already verified, Fedrated Login Redirect"
    return response
    
client = boto3.client('dynamodb',aws_access_key_id='', aws_secret_access_key='', region_name='')    
@app.get("/fetchDataFromDDB", tags=["DynamoDB"])
async def fetch_item_from_Dynamo_DB(DynamoDBTableName: str, plantTimeStampColumnIndexValue: str, experimentPlantTimeStampValue: str):
    database = get_database()
    pprint(f"Database {database}")
    item = get_item(database, plantTimeStampColumnIndexValue, experimentPlantTimeStampValue, DynamoDBTableName)
    pprint(f"Item: {item}")
    message = f"Endpoint: {DynamoDBTableName}\n Database: {database}"
    return {'connection_details': message, 'item_queried': item}

def get_database():
    database = boto3.resource('dynamodb')
    return database

def get_item(database, plantTimeStampColumnIndexValue, experimentPlantTimeStampValue, DynamoDBTableName: str):
    table_id = database.Table(DynamoDBTableName)
    result = table_id.get_item(Key = {plantTimeStampColumnIndexValue: experimentPlantTimeStampValue})
    if not result:
        return None
    item = result.get('Item')
    return item
    

@app.get("/logout", tags=["Logout"])
async def user_Logout():
    response = RedirectResponse(url="/")
    response.delete_cookie(API_KEY_NAME, domain=COOKIE_DOMAIN)
    return response

