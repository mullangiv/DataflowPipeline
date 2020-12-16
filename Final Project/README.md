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
Stock Prediction using Financial News Sentiment Analysis and Time Series Forecasting
Project Proposal:
https://codelabs-preview.appspot.com/?file_id=1TyFR1jlvE59nKuilDi-f81CGV9NqJZscQYVdNB1wxhE#0

## Project Report:
https://codelabs-preview.appspot.com/?file_id=1mx82bA7TVTtCWliCPi2ZfzDeMAPvKqDgOvrzML4R3DE#0

## Web Application:
https://stock-prediction-analysis.herokuapp.com/

## Project Structure
Project
├─- README.md
├── Config file
├── Company Keywords
│   └── keywords to categorize the articles
├── Data: Scripts to scrape the data and api to get stock data
│   └── StockAPI_Alphavantage.py
│   └── WSJScrapper_Headline.py
│   └── WSJScrapper_Content.py
│   └── sentiment_analysis.py
│   └── test_data.csv
├── Dockerfile: instruction for docker image construction.
├── requirements.txt: dependencies.
├── GlueScripts: Scripts for AWS Gule 
│   └── Pyspark scripts for each pipeline
├── webapp: code for flask webapp
│   └── templates: html and css templates for web app
│   └── app.py
│   └── Procfile
│   └── runtime.txt
│   └── License
├── Readme.MD
## Getting Started
## Prerequisites
Python3.5+
Docker
Flask
AWS
Heroku
## Configuring the AWS CLI
You need to retrieve AWS credentials that allow your AWS CLI to access AWS resources.

Sign into the AWS console. This simply requires that you sign in with the email and password you used to create your account. If you already have an AWS account, be sure to log in as the root user.
Choose your account name in the navigation bar at the top right, and then choose My Security Credentials.
Expand the Access keys (access key ID and secret access key) section.
Press Create New Access Key.
Press Download Key File to download a CSV file that contains your new AccessKeyId and SecretKey. Keep this file somewhere where you can find it easily
Get AWS Key and create a config file
Go to https://www.alphavantage.co and get API key to retrive the stock data and paste it in a config file.
## Steps to get the Data
git clone the repo https://github.com/jayeshpatil130/CSYE7245_BDIA/tree/master/Final_Project
In "Data" folder we have file to run the api and the Scrapper function. This is also scheduled with AWS Lambda in AWS console to run daily and can be modified as per the need.
This will get us the data in S3 bucket.
Now, We will have a Data in S3 bucket. Now use the AWS glue scripts to build Glue jobs to extract data from S3 buckets, transform it and load it into the Redshift Data Warehouse.
## Aws Comprehend:
In this repo we have python script for sentiment_analaysis we need to run that in order to get sentiment score of the scrapped data which will trigger the aws gule workflow to run the gule jobs which add the data in redshift data warehouse.
## AWS Forecast Setup:
Sign in to the AWS Management Console and open the Amazon Forecast console.
On the Amazon Forecast home page, choose Create dataset group.
On the Create dataset group page, for Dataset group details, provide the Dataset group name and Forecasting domain – From the drop-down menu, choose Custom.
On the Create target time series dataset page, for Dataset details, provide the following information:
Dataset name – Enter a name for your dataset.
Frequency of your data – In our case, it was daily.
On the Import target time series data page, for Dataset import job details, provide the following information:
Dataset import job name – Enter a name for your dataset.
Timestamp format – We chose (yyyy-MM-dd). The format must be consistent with the input time series data.
IAM role – Keep the default Enter a custom IAM role ARN.
Data Location - se the following format to enter the location of your .csv file on Amazon S3: s3:////<filename.csv>
Import Dataset we created, Train the Predictor by choosing the algorithm(ARIMA in our case) and generate the forecast.
## Deploying the webapp on heroku:
Download heroku toolbelt from https://toolbelt.heroku.com/
Creating requirements.txt in which the dependencies for the package are listed on each line in the same folder as app.py. We can list the following: Flask, gunicorn
Creating runtime.txt which tells Heroku which Python version to use. We have used python-3.5.1
Create a Procfile. It is a text file in the root directory of the application that defines process types and explicitly declares what command should be executed to start our app. It can contain: web: gunicorn app:app --log-file=-
We need to create a GitHub repository with app.py and these essential files along with.gitignore(Although it is not necessary it is recommended to include it)
Now our Flask app folder contains the this file structure
 ├── .gitignore
 ├── Procfile
 ├── app.py
 ├── requirements.txt
 │── runtime.txt
Go on Heroku website and after logging in click on New → Create New App. Enter ”App name” and select the region and click on Create App and in the Deploy tab, select GitHub in Deployment method then Select the repository name and click Connect
Select Enable Automatic Deploys so that whenever we push changes to our GitHub it reflects on our app and Click Deploy Branch which will deploy the current state of the branch. If everything is successful it shows an Open App button. We can now open the app deployed on Heroku
## Docker setup for app:
git clone the repo https://github.com/jayeshpatil130/CSYE7245_BDIA/tree/master/Final_Project
docker build -t stock_app:1.0 . -- this references the Dockerfile at . (current directory) to build our Docker image & tags the docker image with stock_app:1.0
Run docker images & find the image id of the newly built Docker image, OR run docker images | grep stock_app:1.0 | awk '{print $3}'
docker run -it --rm -p 5000:5000 {image_id} stock_app:1.0 -- this refers to the image we built to run a Docker container.
## Tests:
Heroku- Once App is deployed, you can spin the app from your browser, to see if its working or not.
Docker- You test it on 0.0.0.0:5000 or using docker-machine ip (eg : http://192.168.99.100:5000/)
## Authors
Sharvari Karnik

Kunal Jaiswal

Jayesh Patil

## License
This project is licensed under the MIT License - see the LICENSE.md file for details
