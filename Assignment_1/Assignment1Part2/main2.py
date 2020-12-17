import boto3, json, uuid, os, time
from pydantic import BaseModel, Field
from typing import Optional
from pprint import pprint
from fastapi_cloudauth.cognito import Cognito, CognitoCurrentUser, CognitoClaims
from fastapi import Security, Depends, FastAPI, HTTPException
from botocore.exceptions import ClientError
from faker import Faker
from mangum import Mangum
faker = Faker()
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, JSONResponse

# s3 = boto3.resource(service_name='s3', region_name='us-east-')
# data = open('plantdata.csv', 'rb')
# s3.Bucket('s3overwritebucketplantdata').put_object(Key='plantdata.csv', Body=data)


API_KEY = str(uuid.uuid1()) 
API_KEY_NAME = "access_token"
COOKIE_DOMAIN = "localtest.me"
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

#app = FastAPI(openapi_prefix="/prod")
app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
userRegion = "us-east-2"
userClientId = "5cij5puadvuc6c52uivr3fiid7" #ur info
userPool = "us-east-2_DUsINHH06"

auth = Cognito(region= userRegion, userPoolId= userPool)
getUser = CognitoCurrentUser(region= userRegion, userPoolId= userPool)
cidp = boto3.client('cognito-idp')
loginPassword = loginName = None
JWT = {}

@app.get("/", tags=["Homepage"])
async def homepage():
    url = "http://localtest.me:8080/docs?access_token= "
    return "Oops! You are not verified. Please, verify yourself using : " + url

@app.get("/createUser", tags=["Create User"])
async def create_user_on_cognito(usrName: str, usrPassword: str):
    cidp.sign_up(ClientId= userClientId, Username= usrName, Password= usrPassword)
    OTP = API_KEY
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Sudos')
    response = table.put_item(
       Item={
            'Login': OTP,
            'Username': usrName,
            'Password': usrPassword,
        }
    )
    result = "User Created"
    return response,result,OTP
    
@app.get("/confirmUser", tags=["Confirm User"])
async def confirm_user_on_cognito(OTP: str):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Sudos')
    response = table.get_item(Key = {'Login': OTP})
    loginName = response['Item']['Username']
    loginPassword = response['Item']['Password']
    cidp.admin_confirm_sign_up(UserPoolId= userPool, Username= loginName)
    response = "User Confirmed"
    OTP = loginName+loginPassword
    table = dynamodb.Table('Users')
    result = table.put_item(
       Item={
            'Login': OTP,
            'Username': loginName,
            'Password': loginPassword,
        }
    )
    return result,response

@app.get("/generateJWTokens", tags=["JWT"])
async def generateJWToken_user_on_cognito(usrName: str, usrPassword: str):
    OTP = usrName+usrPassword
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Users')
    response = table.get_item(Key = {'Login': OTP})
    loginName = response['Item']['Username']
    loginPassword = response['Item']['Password']
    Login = loginName+loginPassword
    JWT = cidp.admin_initiate_auth(UserPoolId= userPool, ClientId= userClientId, AuthFlow= "ADMIN_NO_SRP_AUTH", AuthParameters= { "USERNAME": loginName, "PASSWORD": loginPassword })   
    refreshJWT = JWT["AuthenticationResult"]["RefreshToken"]
    accessJWT = JWT["AuthenticationResult"]["AccessToken"]
    idJWT = JWT["AuthenticationResult"]["IdToken"]
    response = table.update_item(Key = {'Login': OTP},
        UpdateExpression="set RefreshJWT=:r, AccessJWT=:s, idJWT=:t",
        ExpressionAttributeValues={
            ':r': refreshJWT,
             ':s': accessJWT,
              ':t': idJWT,
        }
    )
    return response,JWT,refreshJWT
    
@app.get("/generateRefreshToken", tags=["Refresh Token"])
async def generateRefreshToken_user_on_cognito(usrName: str, usrPassword: str): 
    OTP = usrName+usrPassword
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Users')
    response = table.get_item(Key = {'Login': OTP})
    loginName = response['Item']['Username']
    loginPassword = response['Item']['Password']
    refreshJWT = response['Item']['RefreshJWT']
    refreshTokenFull = cidp.admin_initiate_auth(UserPoolId= userPool, ClientId= userClientId, AuthFlow= "REFRESH_TOKEN_AUTH", AuthParameters= {"REFRESH_TOKEN" : refreshJWT})
    refreshToken = refreshTokenFull["AuthenticationResult"]["IdToken"]
    response = table.update_item(Key = {'Login': OTP},
        UpdateExpression="set RefreshToken=:r, RefreshTokenFull=:s",
        ExpressionAttributeValues={
            ':r': refreshToken,
             ':s': refreshTokenFull
        }
    )
    return response,refreshToken
    
@app.get("/Faker", tags=["Anonymise"])
async def anonymize_data_using_faker(sourceTableName: str, newTableName: str, currentUser: CognitoClaims = Depends(getUser)):
    dynamodb = boto3.resource('dynamodb')
    dynamodbClient = boto3.client("dynamodb")
    updateTable = dynamodb.Table(newTableName)
    resp = dynamodb.create_table(
            TableName=newTableName,
            KeySchema=[
                {
                    'AttributeName': 'Timestamp',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'Timestamp',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 3,
                'WriteCapacityUnits': 3
            }
        )
    time.sleep(9)
    Newcondition = []
    for item in scan_table(dynamodbClient, TableName=sourceTableName):
        Newcondition.append(item)

    for user in Users:
        Newcondition['A_1']['S'] = faker.random_digit() 
        Newcondition['A_2']['S'] = faker.random_digit()
        Newcondition['A_3']['S'] = faker.random_digit()
        
        response = updateTable.put_item(
           Item={'A_1': Newcondition['A_1']['S'],
                  'A_2': Newcondition['A_2']['S'],
                   'A_3': Newcondition['A_3']['S']
                    }
        )
    result = "Anonimized Data"
    return result
    
@app.get("/fetchDataFromDDB", tags=["DynamoDB"])
async def fetch_item_from_Dynamo_DB(DynamoDBTableName: str, plantTimeStampColumnIndexValue: str, experimentPlantTimeStampValue: str, currentUser: CognitoClaims = Depends(getUser)):
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
    
def scan_table(dynamodbClient, *, TableName, **kwargs):
    paginator = dynamodbClient.get_paginator("scan")
    for page in paginator.paginate(TableName=TableName, **kwargs):
        yield from page["Items"]

@app.get("/openapi.json", tags=["Cookie"])
async def get_open_api_endpoint():
    response = JSONResponse(
        get_openapi(title="FastAPI authentication security test", version=1, routes=app.routes)
    )
    return response

@app.get("/logout", tags=["Logout"])
async def user_Logout():
    response = RedirectResponse(url="/")
    response.delete_cookie(API_KEY_NAME, domain=COOKIE_DOMAIN)
    return response

#handler = Mangum(app)

