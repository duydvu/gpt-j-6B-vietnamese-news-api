# API service for GPT-J 6B on Vietnamese News

This Python code run an API service to make inference with [GPT-J 6B on Vietnamese News](https://huggingface.co/VietAI/gpt-j-6B-vietnamese-news).

Although the model is gigantic, I have managed to run it on a 16GB node with 2 x NVIDIA T4 on GKE. Using spot node decreases the cost down to about $180/month or $0.25/hour, which is a relatively cheap price if we want to run it occasionally.

## Build Docker

First, you need to download the model to local.
1. Install git-lfs
2. Run `git clone https://huggingface.co/VietAI/gpt-j-6B-vietnamese-news`

Next, move the model folder into this repository folder:
```
mv ./gpt-j-6B-vietnamese-news ./gpt-j-6B-vietnamese-news-api
```

And build Docker image:
```
docker build -t gpt-j .
```

## Run API service

Run with Docker:
```
docker run -it --rm -p 5000:5000 gpt-j
```

Deploy with Helm:
```
helm install --set namespace=default --set image=gpt-j --set version=latest gpt-j ./k8s/chart
```

## Test API

To make inference, call HTTP POST method to `/predict` with JSON body, for example:
```
{
    "text": "GPT là gì?"
}
```

Beside `text` param, there are 3 more params:
1. `n_samples`: number of samples to return.
2. `top_k`: filter k most likely next words.
3. `top_p`: chooses from the smallest possible set of words whose cumulative probability exceeds the probability p.

The method of generating texts is sampling the next words from a probability distribution from the output of the model. So everytime the API is called, it will generate different results.

See [https://huggingface.co/blog/how-to-generate](https://huggingface.co/blog/how-to-generate) to understand about `top_k` and `top_p`.
