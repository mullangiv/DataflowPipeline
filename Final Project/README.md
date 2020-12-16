# λ selenium-chromium-lambda

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

## Project
Fake News Detection and Sentiment Analysis Data Pipeline
## Project Proposal:

https://codelabs-preview.appspot.com/?file_id=1WZF0_4p3RpdacD9EQpeUyugntsY1PdG8-ErJOKMZ950#0

## Project Report:

https://codelabs-preview.appspot.com/?file_id=1RbHApJS1RWtCxlATIAjOV2adBGAz5flxdJdZFLeR14s#0

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





## Getting Started
Prerequisites
Python3.5+
Docker
FastAPI
AWS
Streamlit


## Authors
Hardik Thakkar

Rugved Gole

Vinod Kumar Mullangi

