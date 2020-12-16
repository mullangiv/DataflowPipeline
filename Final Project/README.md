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

