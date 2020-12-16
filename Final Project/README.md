## Project
Fake News Detection and Sentiment Analysis Data Pipeline

## Project Proposal:

https://codelabs-preview.appspot.com/?file_id=1WZF0_4p3RpdacD9EQpeUyugntsY1PdG8-ErJOKMZ950#0

## Project Report:

https://codelabs-preview.appspot.com/?file_id=1RbHApJS1RWtCxlATIAjOV2adBGAz5flxdJdZFLeR14s#0

## Project Structure

Project
├── README.md
├── Config file
├── Data: Scripts to scrape the data and api to get stock data
│   └── Newsarticle.py
│   └── Twitter.py
│   └── sample_news_data.csv
│   └── sample_twitter_data.csv
├── requirements.txt: dependencies.
├── Fakenews
│   └── Fakenews.py
├── webapp: code for Streamlit and fastapi
│   └── streamlitapp.py
│   └── fastapiapp.py
│   └── License
├── Readme.MD

## Getting Started
## Prerequisites
Python3.5+

FastAPI

AWS

Streamlit
## Configuring the AWS CLI
You need to retrieve AWS credentials that allow your AWS CLI to access AWS resources.

Sign into the AWS console. This simply requires that you sign in with the email and password you used to create your account. If you already have an AWS account, be sure to log 

in as the root user.

Choose your account name in the navigation bar at the top right, and then choose My Security Credentials.

Expand the Access keys (access key ID and secret access key) section.

Press Create New Access Key.

Press Download Key File to download a CSV file that contains your new AccessKeyId and SecretKey. Keep this file somewhere where you can find it easily

Get AWS Key and create a config file

## Steps to get the Data
git clone the repo https://github.com/HardikThakkar94/DataflowPipeline/tree/main/Final%20Project

Newsarticle.py
Twitter.py

In "Data" folder we have file to run the api and the Scrapper function. 

This will get us the data in S3 bucket.

Now, We will have a Data in S3 bucket. Now use the AWS Lambda to extract data from S3 buckets, transform it and load it into the Dynamodb.
## Sentiment Analysis using Aws Comprehend:


## Fake News Detection(λ selenium-chromium-lambda)

How to run automated (Selenium) Headless Chromium in AWS Lambda.

Please refer the article to understand how the selenium driver is handled on aws lambda:-

Read full article by author [vittorionardone: chromium-and-selenium-in-aws-lambda](https://www.vittorionardone.it/en/2020/06/04/chromium-and-selenium-in-aws-lambda)
## SAM Deploy
Run these commands in sequence:

`make lambda-layer-build` to prepare archive for AWS Lambda Layer deploy (layer.zip)

`make lambda-function-build` to prepare archive for AWS Lambda deploy (deploy.zip)

`make BUCKET=<your_bucket_name> create-stack` to create CloudFormation stack (lambda function, layer and IAM role)

## Lambda Update
update your lambda and add remaining dependancies as layers if any:

update lambda handler to `src/main.handler`

## Credits
Inspired by : [selenium-chromium-lambda](https://github.com/vittorio-nardone/selenium-chromium-lambda),

[pychromeless](https://github.com/21Buttons/pychromeless),

And [authentikos](https://github.com/srinjoychakravarty/authentikos)

## Testing:
Streamlit : 

FastAPI : 

## Deploying the Streamlit on AWS:

## Steps to run the application:

Application is deployed on AWS.

Application Link :

## API 1:- Scraping(News Articles)

Data scrapped from given news website

Go to Scrapping page -> enter link in Link input -> Press “Scrape” button


## API 2:- Fake News Detection

Scrapped data from news website will be input to the Fake News Detection algorithm which give the results whether the news in real or fake.

## API 3:- Scraping(Comments related to scrapped news article from Twitter)

Go to Scrapping page -> Press “Scrape” button

## API 4:- Sentiment Analysis

Scrapped data from twitter will be input to the Sentiment Analysis algorithm which give the sentiments scores.

## API 5:- Analytics

1. If article is fake, how the twitter users sentiments are. Finding how the fake news is spreading among users.




## Authors
Hardik Thakkar

Rugved Gole

Vinod Kumar Mullangi

