# Deploy BERT for Sentiment Analsysi with FastAPI

Deploy a pre-trained BERT model for Sentiment Analysis as a REST API using FastAPI

## Demo
The model is trained to classify sentiment (negative, neutral, and positive) on a custom dataset from app reviews on Google Play. Here's a sample request to the API:

```bash
http POST http://127.0.0.1:8000/predict text="Good basic lists, i would like to create more lists, but the annual fee for unlimited lists is too out there"
```

The response you'll get looks something like this:

```js
{
    "confidence": 0.9999083280563354,
    "probabilities": {
        "negative": 3.563107020454481e-05,
        "neutral": 0.9999083280563354,
        "positive": 5.596495248028077e-05
    },
    "sentiment": "neutral"
}
```

You can also [read the complete tutorial here](https://www.curiousily.com/posts/deploy-bert-for-sentiment-analysis-as-rest-api-using-pytorch-transformers-by-hugging-face-and-fastapi/)

## Installation

Clone this repo

Install the dependencies:

```sh
pipenv install --dev
```

Download the pre-trained model:
https://drive.google.com/uc?id=1V8itWtowCYnb2Bc9KlK9SxGff9WwmogA
save this model in assets folder in the same directory as sentiment_analyzer

## Docker

Use the Dockerfile_HT to dockerize it please make sure before you run the docker you have it tested on local as FastAPI
```sh
docker create -t ImageName . 
```
```sh
docker run -i --name ContainerName -p 8000:8000 ImageName
```
## License

MIT
