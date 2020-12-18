#H
#Core Packages
import json, boto3, requests, datetime, time, urllib.request, logging, threading, sys, io, os, random, re, requests, title, tweepy, twitter, pandas as pd
from mistletoe import markdown
from html2text import HTML2Text
from fastapi import FastAPI, HTTPException, Security, Depends
# from pydantic import BaseModel, Field   
from bs4 import BeautifulSoup  as bs
from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, JSONResponse
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from mangum import Mangum
from fastapi_cloudauth.cognito import Cognito, CognitoCurrentUser, CognitoClaims
from urllib.parse import urlparse,urlsplit
from boto3.dynamodb.conditions import Key
from tweepy import OAuthHandler
from io import StringIO

# from botocore.exceptions import NoCredentialsError

#Def Vars

app = FastAPI(root_path="/prod")
#To Configure ---- root_path 
#app = FastAPI(title="Fake News Detection Pipeline", description='''Backend API for App''', version="0.0.0",openapi_prefix="/prod",openapi_url="")

#Def AWS Config
userRegion = "us-east-1"
userClientId = "5g5l767fmou68418i4l335lfsj"
userPool = "us-east-1_w6Msc6CWC"
auth = Cognito(region= userRegion, userPoolId= userPool)
getUser = CognitoCurrentUser(region= userRegion, userPoolId= userPool)
cidp = boto3.client('cognito-idp')
dynamodb = boto3.resource('dynamodb')
dynamodbClient = boto3.client("dynamodb")
comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
table = dynamodb.Table('DeidentificationTable')
loginPassword = loginName = None


def get_body(soup,tags):
    textOut = ""
    temp=""
    body = [a for a in soup.find_all(class_=tags)] #class_="g1-content-narrow g1-typography-xl entry-content"
        
    for b in body:
        for p in b.find_all("p"):
            for q in p.find_all("b"):
                temp=temp + q.text
            for r in p.find_all("a"):
                temp=temp + r.text
            temp=temp + p.text
            textOut = textOut + temp
            temp=""
    return textOut

def get_title(soup,tags):
    return soup.find(class_=tags).text #class_="g1-mega g1-mega-1st entry-title"

#API scrapeBBCNews
@app.get("/scrapeBBCNews", tags=["Scrape BBC News"])
async def scrapeBBCNews(url: str, current_user: CognitoClaims = Depends(auth)):
    article = requests.get(url)
    soup = bs(article.content, "html.parser")
    title2=get_title(soup,"css-1pl2zfy-StyledHeading e1fj1fc10")
    bodyText = get_body(soup,"css-83cqas-RichTextContainer e5tfeyi2")
    print(title2)
    title.Title = title2
    print(bodyText)
    s3 = boto3.resource('s3')
    BUCKET_NAME = "htsnewsarticlebucket"
    s3.Bucket(BUCKET_NAME).put_object(Key=title2+'.txt', Body=bodyText)
    s3.Bucket(BUCKET_NAME).put_object(Key='Article.txt', Body=bodyText)
    return title2


#scrapeHuzlersNews
@app.get("/scrapeHuzlersNews", tags=["Scrape Huzlers News"])
async def scrapeHuzlersNews(url: str, current_user: CognitoClaims = Depends(auth)):
    article = requests.get(url)
    soup = bs(article.content, "html.parser")
    title2=get_title(soup,"g1-mega g1-mega-1st entry-title")
    bodyText = get_body(soup,"g1-content-narrow g1-typography-xl entry-content")
    print(title2)
    title.Title = title2
    print(bodyText)
    s3 = boto3.resource('s3')
    BUCKET_NAME = "htsnewsarticlebucket"
    s3.Bucket(BUCKET_NAME).put_object(Key=title2+'.txt', Body=bodyText)
    s3.Bucket(BUCKET_NAME).put_object(Key='Article.txt', Body=bodyText)
    return title.Title

#scrapeTwitterNews
@app.get("/ScrapeNewsFromTwitter", tags=["ScrapeNewsFromTwitter"])
def ScrapeNewsFromTwitter(current_user: CognitoClaims = Depends(auth)):
    consumer_key = twitter.consumer_key
    consumer_secret = twitter.consumer_secret
    access_token = twitter.access_token
    access_token_secret = twitter.access_token_secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    tweets = []
    tweet2=''
    count = 1
#Twitter will automatically sample the last 7 days of data. Depending on how many total tweets there are with the specific hashtag, keyword, handle, or key phrase that you are looking for, you can set the date back further by adding since= as one of the parameters. You can also manually add in the number of tweets you want to get back in the items() section.
    filename = title.Title
    
    gadhedoChe = False
    if ":" in filename:
        gadhedoChe = True
    #make a if condition here !
    if gadhedoChe == True:
        for tweet in tweepy.Cursor(api.search, q=(filename[:filename.index(':')]),lang="en", count=450, since='2020-02-28').items(963):
            count = count + 1
            try:
                temp=(tweet.text).replace(',','')
                temp=temp.replace('RT','')
                temp=re.sub('(?:\s)@[^, ]*', '', temp)
                temp=re.sub('(?:\s)http[^, ]*', '', temp)
                temp=re.sub(r'[^A-Za-z0-9 ]+', '', temp)
                s=(comprehend.detect_sentiment(Text=temp, LanguageCode='en'))
                loc = (tweet.user.location)
                loc = str(loc)
                locList = ["Afghanistan","Albania","Algeria","America","Argentina","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Belgium","Brazil","Bulgaria","Cambodia","Canada","China","Colombia","Costa Rica","Croatia","Cuba","Czech","Denmark","Egypt","England","Finland","France","Germany","Ghana","Great Britain","Greece","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Israel","Italy","Jamaica","Japan","Kenya","Korea","Kuwait","Malaysia","Mexico","Netherlands","New Zealand","Pakistan","Philippines","Portugal","Russia","Saudi Arabia","scotland","Singapore","Spain","Sri Lanka","Sweden","Switzerland","Thailand","United Kingdom","United States"]
                loc = random.choice(locList)
                data = [tweet.created_at, tweet.id, temp, tweet.retweet_count,re.sub(r'[^A-Za-z0-9 ]+', '', loc.replace(',','')),s['SentimentScore']['Positive'],s['SentimentScore']['Negative'],s['SentimentScore']['Neutral'],s['SentimentScore']['Mixed'],s['Sentiment']]
                data = tuple(data)
                tweet2=tweet2 + temp
                tweets.append(data)
            except tweepy.TweepError as e:
                print(e.reason)
                continue
            except StopIteration:
                break
    else:
        filename = filename.replace(";","")
        filename = filename.replace(",","")
        filename = filename.replace("'","")
        filename = filename.replace('"',"")
        for tweet in tweepy.Cursor(api.search, q=(filename[:filename.index(' ')+3]),lang="en", count=450, since='2020-02-28').items(963):
            count = count + 1
            try:
                temp=(tweet.text).replace(',','')
                temp=temp.replace('RT','')
                temp=re.sub('(?:\s)@[^, ]*', '', temp)
                temp=re.sub('(?:\s)http[^, ]*', '', temp)
                temp=re.sub(r'[^A-Za-z0-9 ]+', '', temp)
                s=(comprehend.detect_sentiment(Text=temp, LanguageCode='en'))
                loc = (tweet.user.location)
                loc = str(loc)
                locList = ["Afghanistan","Albania","Algeria","America","Argentina","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Belgium","Brazil","Bulgaria","Cambodia","Canada","China","Colombia","Costa Rica","Croatia","Cuba","Czech","Denmark","Egypt","England","Finland","France","Germany","Ghana","Great Britain","Greece","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Israel","Italy","Jamaica","Japan","Kenya","Korea","Kuwait","Malaysia","Mexico","Netherlands","New Zealand","Pakistan","Philippines","Portugal","Russia","Saudi Arabia","scotland","Singapore","Spain","Sri Lanka","Sweden","Switzerland","Thailand","United Kingdom","United States"]
                loc = random.choice(locList)
                data = [tweet.created_at, tweet.id, temp, tweet.retweet_count,re.sub(r'[^A-Za-z ]+', '', loc.replace(',','')),s['SentimentScore']['Positive'],s['SentimentScore']['Negative'],s['SentimentScore']['Neutral'],s['SentimentScore']['Mixed'],s['Sentiment']]
                data = tuple(data)
                tweet2=tweet2 + temp
                tweets.append(data)
            except tweepy.TweepError as e:
                print(e.reason)
                continue
            except StopIteration:
                break
    df = pd.DataFrame(tweets, columns = ['created_at','tweet_id', 'tweet_text','retweet_count','location','Positive','Negative','Neutral','Mixed','Sentiment'])
    bucket = 'htstwitterarticlebucket' # already created on S3
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, header=False)
    s3_resource = boto3.resource('s3')
    s3_resource.Bucket(bucket).put_object(Key='tweets.txt', Body=tweet2)
    s3_resource.Object(bucket, 'df.csv').put(Body=csv_buffer.getvalue()) 
    return tweet2

handler = Mangum(app)

#T