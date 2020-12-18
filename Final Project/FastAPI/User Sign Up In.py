#H
import boto3,user
from fastapi import Depends, FastAPI
from mangum import Mangum

app = FastAPI(root_path="/prod")
@app.get("/sign_up", tags=["User Sign Up"])
async def sign_up(userid: str, password: str):
    
    def sign_up_cognito(ci,upi,uid,pwd):
    
        cidp = boto3.client('cognito-idp')
        
        try:
            cidp.sign_up(ClientId= ci, Username= uid, Password= pwd)
            user.Status = "UnConfirmed"
            try:
                cidp.admin_confirm_sign_up(UserPoolId= upi,Username= uid)
                user.Status = "Confirmed"
            except:
                user.Status = "UnConfirmed"
                
            try:     
                jwt = cidp.admin_initiate_auth( 
                    UserPoolId= upi,
                    ClientId= ci,
                    AuthFlow= "ADMIN_NO_SRP_AUTH",
                    AuthParameters= {
                    "USERNAME": uid,
                    "PASSWORD": pwd
                    })
                    
                    
                r = cidp.admin_initiate_auth( 
                    UserPoolId= upi,
                    ClientId= ci,
                    AuthFlow= "REFRESH_TOKEN_AUTH",
                    AuthParameters= {
                    "REFRESH_TOKEN" : jwt["AuthenticationResult"]["RefreshToken"]
                    })
                
                user.Status = (r["AuthenticationResult"]["IdToken"]) 
                login = uid+pwd
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('Users')
                response = table.put_item(
                   Item={
                        'Login': login,
                        'Username': uid,
                        'Password': pwd,
                    })
            except:
                user.Status = "Failed JWT Generation"
        except:
            errorMessage = user.Status
            
    ci = "5g5l767fmou68418i4l335lfsj"
    upi = "us-east-1_w6Msc6CWC"   
    uid = userid # take from user
    pwd = password # take from user     
   
    sign_up_cognito(ci,upi,uid,pwd)
    errorMessage = user.Status
    user.Status = "Already Exists!!!"
    return errorMessage

           
@app.get("/createUnConfirmUser", tags=["User Sign Up"])
async def createUnConfirmUser(userid: str, password: str):
    
    def unconfirm_sign_up_cognito(ci,upi,uid,pwd):
    
        cidp = boto3.client('cognito-idp')

        try:
            cidp.sign_up(ClientId= ci, Username= uid, Password= pwd)
            user.Status = "UnConfirmed"
        except:
            user.Status = "Already Exists!!!"
                
    ci = "5g5l767fmou68418i4l335lfsj"
    upi = "us-east-1_w6Msc6CWC"   
    uid = userid # take from user
    pwd = password # take from user     
   
    unconfirm_sign_up_cognito(ci,upi,uid,pwd)
    errorMessage = user.Status
    return errorMessage
           
@app.get("/confirm", tags=["User Sign Up"])
async def confirm_sign_up(userid: str, password: str):
    
    def confirm_sign_up_cognito(ci,upi,uid,pwd):
    
        cidp = boto3.client('cognito-idp')

        try:
            cidp.admin_confirm_sign_up(
                UserPoolId= upi,
                Username= uid)
            user.Status = "Confirmed"
        except:
            user.Status = "UnConfirmed"
                
    ci = "5g5l767fmou68418i4l335lfsj"
    upi = "us-east-1_w6Msc6CWC"   
    uid = userid # take from user
    pwd = password # take from user     
   
    confirm_sign_up_cognito(ci,upi,uid,pwd)
    errorMessage = user.Status
    return errorMessage

@app.get("/generateTokens", tags=["User Sign Up"])
async def generateTokens(userid: str, password: str):
    
    def generate_sign_up_cognito(ci,upi,uid,pwd):
    
        cidp = boto3.client('cognito-idp')
            
        try:     
            jwt = cidp.admin_initiate_auth( 
                UserPoolId= upi,
                ClientId= ci,
                AuthFlow= "ADMIN_NO_SRP_AUTH",
                AuthParameters= {
                "USERNAME": uid,
                "PASSWORD": pwd
                })
                
                
            r = cidp.admin_initiate_auth( 
                UserPoolId= upi,
                ClientId= ci,
                AuthFlow= "REFRESH_TOKEN_AUTH",
                AuthParameters= {
                "REFRESH_TOKEN" : jwt["AuthenticationResult"]["RefreshToken"]
                })
                
            user.Status = (jwt["AuthenticationResult"]["AccessToken"]),(jwt["AuthenticationResult"]["IdToken"]),(jwt["AuthenticationResult"]["RefreshToken"]),(r["AuthenticationResult"]["IdToken"]) 
            
        except:
            user.Status = "Failed JWT Generation"
    
    ci = "5g5l767fmou68418i4l335lfsj"
    upi = "us-east-1_w6Msc6CWC"   
    uid = userid # take from user
    pwd = password # take from user     
   
    generate_sign_up_cognito(ci,upi,uid,pwd)
    errorMessage = user.Status
    return errorMessage
    
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
    
handler = Mangum(app)
#T