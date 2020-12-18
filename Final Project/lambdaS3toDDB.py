import boto3

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
        
def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    obj = s3.get_object(Bucket = bucket, Key = key)
    
    rows = obj['Body'].read().split('\n')
       
    table = dynamodb.Table('Twitter')   
    
    with table.batch_writer() as batch:
        for row in rows:
            batch.put_item(Item={
                'serial' :row.split(',')[0],
                'created_at' :row.split(',')[1],
                'tweet_id' :row.split(',')[2],
                'tweet_text' :row.split(',')[3],
                'retweet_count' :row.split(',')[4],
                'location' :row.split(',')[5],
                'Positive' :row.split(',')[6],
                'Negative' :row.split(',')[7],
                'Neutral' :row.split(',')[8],
                'Mixed' :row.split(',')[9],
                'Sentiment' :row.split(',')[10]
            })
